import math
import struct

from llvmlite import ir
from src.constructs.mips_program.node import instr as mips_inst
from src.constructs.mips_program.node.reg import Reg, Regf
from src.constructs.mips_program.program import MipsProgram
from src.constructs.mips_program.variable import Variables


def assert_type(value, typename):
    assert type(value).__name__ == typename, f"type '{type(value).__name__}' not implemented"


def get_type_size(type: ir.Type) -> int:
    """Get the size of the type in bytes."""
    match type:
        case ir.IntType():
            res = math.ceil(type.width / 8)
        case ir.PointerType():
            res = get_type_size(type.pointee)
        case ir.FloatType():
            res = 4
        case ir.ArrayType():
            res = type.count * get_type_size(type.element)
        case _:
            assert False
    assert res > 0
    return res


def get_args_size(args) -> int:
    """Get the size of the provided arguments in bytes."""
    return sum(get_type_size(arg.type) for arg in args)


class MVBase:
    tree: MipsProgram
    "Tree of the mips program blocks with instructions."

    @property
    def last_block(self):
        """Current block being visited."""
        return self.tree.blocks[-1]

    variables: Variables
    "List of passed variables in current function scope"

    stack_offset: int
    "Largest stack offset used"

    new_function_started: bool
    "True if a new function has just started. Used to indicate to the block visit a new stack frame should be created."

    def align_to(self, alignment: int):
        """Align the stack to the given alignment in bytes"""
        shift_bits = int(math.log2(alignment))
        self.stack_offset = math.floor(self.stack_offset / alignment) * alignment
        self.last_block.add_instr(
            mips_inst.Srl(Reg.sp, Reg.sp, shift_bits),
            mips_inst.Sll(Reg.sp, Reg.sp, shift_bits),
        )

    def load_float(
        self, i: ir.Instruction | tuple[ir.Argument, ir.Function], r: Regf, text: str | mips_inst.Comment = ""
    ) -> mips_inst.Instruction:
        """Load a value from an instruction or a constant into the register."""
        assert isinstance(i.type, ir.FloatType)

        if isinstance(i, ir.Constant):  # if loading instruction is a constant
            assert isinstance(i.type, ir.FloatType)
            h = hex(struct.unpack("<I", struct.pack("<f", i.constant))[0])
            return (mips_inst.Li(Reg.t1, h, text), mips_inst.Mtc1(Reg.t1, r))
        elif isinstance(i, ir.Argument):  # if loading instruction is a function argument
            func: ir.Function = self.function
            arg_index: int = func.args.index(i)
            offset = get_args_size(
                func.args[arg_index:]
            )  # offset is size of argument to load and all following arguments
            return mips_inst.L_s(r, Reg.fp, offset, text)  # lw $r, offset($fp)
        else:  # all other instructions
            return mips_inst.L_s(r, Reg.fp, self.variables[i.name].offset, text)  # lw $r, offset($fp)

    def load_int(
        self, i: ir.Instruction | tuple[ir.Argument, ir.Function], r: Reg, text: str | mips_inst.Comment = ""
    ) -> mips_inst.Instruction:
        """Load a value from an instruction or a constant into the register."""
        assert isinstance(i.type, (ir.IntType, ir.PointerType))

        load_instr = None
        # decide what load instruction to use based on the size of the type
        match get_type_size(i.type):
            case 4:
                load_instr = mips_inst.Lw
            case 2:
                load_instr = mips_inst.Lh
            case 1:
                load_instr = mips_inst.Lb
            case _:
                assert False

        if isinstance(i, ir.Constant):  # if loading instruction is a constant
            return mips_inst.Li(r, i.constant, text)
        elif isinstance(i, ir.Argument):  # if loading instruction is a function argument
            func: ir.Function = self.function
            arg_index: int = func.args.index(i)
            offset = get_args_size(func.args[arg_index:])
            return load_instr(r, Reg.fp, offset, text)  # lw $r, offset($fp)
        else:  # all other instructions
            return load_instr(r, Reg.fp, self.variables[i.name].offset, text)  # lw $r, offset($fp)

    def load_value(
        self, i: ir.Instruction | tuple[ir.Argument, ir.Function], r: Reg | Regf, text: str | mips_inst.Comment = ""
    ) -> mips_inst.Instruction:
        """
        Load an instruction result or constant into the normal/float register.
        For normal registers the size of the type is used to determine the load type.
        Eg. a type of 1 byte uses `lb` instead of `lw`.
        """
        # decide to load float or int based on the register type to load into
        if isinstance(r, Regf):
            return self.load_float(i, r, text)
        return self.load_int(i, r, text)

    def load_address(self, i: ir.Instruction | tuple[ir.Argument, ir.Function], value, r: Reg) -> mips_inst.Instruction:
        """
        Load the address of a pointer into the register.
        """
        if isinstance(i, ir.Argument):
            func: ir.Function = self.function
            arg_index: int = func.args.index(i)
            offset = get_args_size(func.args[arg_index:])
            return mips_inst.Addiu(r, Reg.fp, offset, mips_inst.Comment(f"Load address of argument {i.name}"))

        # Ensure the value is a variable with an allocated memory space
        assert value.name in self.variables, f"Variable {value.name} not found in allocated variables."

        # Retrieve the variable's offset
        var_offset = self.variables[value.name].offset

        # TODO: add support for function

        # Load the address into the register by adding the variable's offset to the frame pointer
        return mips_inst.Addiu(r, Reg.fp, var_offset, mips_inst.Comment(f"Store address of {value.name}"))

    def store_float(self, r: Regf, offset: int, text: str | mips_inst.Comment = "") -> mips_inst.Instruction:
        """Store a float in register ``r`` at ``offset`` from the frame pointer."""
        return mips_inst.S_s(r, Reg.fp, offset, text)

    def store_int(
        self, i: ir.Instruction, r: Reg, offset: int, text: str | mips_inst.Comment = ""
    ) -> mips_inst.Instruction:
        """Store an int in register ``r`` at ``offset`` from the frame pointer."""
        # decide what store instruction to use based on the size of the type
        match get_type_size(i.type):
            case 4 | 8:
                return mips_inst.Sw(r, Reg.fp, offset, text)
            case 2:
                return mips_inst.Sh(r, Reg.fp, offset, text)
            case 1:
                return mips_inst.Sb(r, Reg.fp, offset, text)
        assert False, "unsupported type size"

    def store_value(
        self, i: ir.Instruction, r: Reg | Regf, offset: int, text: str | mips_inst.Comment = ""
    ) -> mips_inst.Instruction:
        """Store content of a normal/float register ``r`` at ``offset`` from the frame pointer."""
        if isinstance(r, Regf):
            return self.store_float(r, offset, text)
        return self.store_int(i, r, offset, text)

    def visit(self, module: ir.Module):
        """Visit a module. Top level visit function."""
        print(type(module).__name__)
        for glob in module.global_values:
            if isinstance(glob, ir.GlobalVariable):
                self.visit_Global(glob)
            elif isinstance(glob, ir.Function):
                self.visit_Function(glob)
            else:
                print("unhandled glob")
