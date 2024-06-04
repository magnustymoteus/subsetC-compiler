import struct

from llvmlite import ir
from src.constructs.mips_program.node import instr as mips_inst
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg, Regf
from src.constructs.mips_program.program import MipsProgram
from src.constructs.mips_program.variable import Variables, Global


PTR_SIZE = 4


def assert_type(value, typename):
    assert type(value).__name__ == typename, f"type '{type(value).__name__}' not implemented"


def get_type_size(t: ir.Type) -> int:
    """Get the size of the type in bytes."""
    match t:
        case ir.IntType():
            # res = math.ceil(t.width / 8)
            res = 4
        case ir.PointerType():
            res = PTR_SIZE
        case ir.FloatType() | ir.DoubleType():
            res = 4
        case ir.VoidType():
            return 0
        case ir.ArrayType():
            res = t.count * get_type_size(t.element)
        case ir.IdentifiedStructType():
            res = sum(get_type_size(field) for field in t.elements)
        case _:
            assert False
    assert res > 0
    return res


class _ArgOffset():
    def __init__(self, instr: ir.Instruction, offset: int, size: int) -> None:
        self.instr = instr
        self.offset = offset
        self.size = size

    def __iter__(self):  # needed to allow unpacking
        return iter((self.instr, self.offset, self.size))

    def __repr__(self) -> str:
        return f"<_ArgOffset({self.instr.__repr__()}, {self.offset}, {self.size})>"


class MVBase:
    tree: MipsProgram
    "Tree of the mips program blocks with instructions."

    @property
    def last_block(self):
        """Current block being visited."""
        if len(self.tree.blocks) == 0:
            return None
        return self.tree.blocks[-1]

    variables: Variables
    "List of passed variables in current function scope"

    stack_offset: int | None
    "Largest stack offset used"

    new_function_started: bool
    "True if a new function has just started. Used to indicate to the block visit a new stack frame should be created."

    def load_float(
        self,
        i: ir.Instruction | ir.GlobalVariable,
        r: Regf,
        text: str | mips_inst.Comment = "",
        mem_base: Reg = Reg.fp,
    ) -> mips_inst.Instruction:
        """Load a value from an instruction or a constant into the register."""
        assert isinstance(i.type, (ir.FloatType, ir.DoubleType))

        if isinstance(i, ir.Constant):  # if loading instruction is a constant
            assert isinstance(i.type, (ir.FloatType, ir.DoubleType))
            h = hex(struct.unpack("<I", struct.pack("<f", i.constant))[0])
            return mips_inst.Li(Reg.t1, h, text), mips_inst.Mtc1(Reg.t1, r)
        else:  # all other instructions
            return mips_inst.L_s(r, mem_base, self.variables[i.name].offset, text)  # lw $r, offset($fp)

    def load_int(
        self,
        i: ir.Instruction | ir.GlobalVariable,
        r: Reg,
        text: str | mips_inst.Comment = "",
        mem_base: Reg = Reg.fp,
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
        if isinstance(i, ir.FormattedConstant):
            # assuming it is a string
            formatted_str = "$G" + [elem for elem in i.constant.split() if elem[0] == "@"][0][2:-2]
            var = self.variables[formatted_str]
            if isinstance(var, Global) and var.type in ["ascii", "asciiz"]:
                return mips_inst.La(r, var.label)
            return mips_inst.Lw(r, formatted_str, None, text)
        elif isinstance(i, ir.Constant):  # if loading instruction is a constant
            return mips_inst.Li(r, i.constant, text)
        elif isinstance(i, ir.GlobalVariable):
            assert i.type.is_pointer
            result = mips_inst.La(r, Label(i.name), text)
            return result
        else:  # all other instructions
            return load_instr(r, mem_base, self.variables[i.name].offset, text)  # lw $r, offset($fp)

    def load_value(
        self,
        i: ir.Instruction | ir.GlobalVariable,
        r: Reg | Regf,
        text: str | mips_inst.Comment = "",
        mem_base: Reg = Reg.fp,
    ) -> mips_inst.Instruction:
        """
        Load an instruction result or constant into the normal/float register.
        For normal registers the size of the type is used to determine the load type.
        Eg. a type of 1 byte uses `lb` instead of `lw`.
        """
        # decide to load float or int based on the register type to load into
        if isinstance(r, Regf):
            return self.load_float(i, r, text, mem_base)
        return self.load_int(i, r, text, mem_base)

    def load_address(
        self, i: ir.Instruction | ir.GlobalVariable, value, r: Reg
    ) -> mips_inst.Instruction:
        """
        Load the address of a pointer into the register.
        """
        # Ensure the value is a variable with an allocated memory space
        assert value.name in self.variables, f"Variable {value.name} not found in allocated variables."

        # Retrieve the variable's offset
        var_offset = self.variables[value.name].offset

        # TODO: add support for function

        # Load the address into the register by adding the variable's offset to the frame pointer
        return mips_inst.Addiu(r, Reg.fp, var_offset, mips_inst.Comment(f"Store address of {value.name}"))

    def store_float(
        self, i: ir.Instruction, r: Regf, offset: int, text: str | mips_inst.Comment = "", mem_base: Reg = Reg.fp
    ) -> mips_inst.Instruction:
        """
        Store a float in register ``r`` at ``offset`` from the frame pointer.

        :param r: The register to store the float in.
        :param offset: The offset to store the float at.
        :param text: The comment to add to the instruction.
        :param mem_base: The base register to use for the store instruction.
        """
        dest = mem_base if not isinstance(i, ir.GlobalVariable) else i.name

        return mips_inst.S_s(r, dest, offset, text)

    def store_int(
        self, i: ir.Instruction, r: Reg, offset: int | None, text: str | mips_inst.Comment = "", mem_base: Reg = Reg.fp
    ) -> mips_inst.Instruction:
        """
        Store an int in register ``r`` at ``offset`` from the frame pointer.

        :param i: The of which the result is stored. Needed for the size of it's type.
        :param r: The register to store the int in.
        :param offset: The offset to store the int at.
        :param text: The comment to add to the instruction.
        :param mem_base: The base register to use for the store instruction.
        """
        dest = mem_base if not isinstance(i, ir.GlobalVariable) else i.name
        # decide what store instruction to use based on the size of the type
        match get_type_size(i.type):
            case 4 | 8:
                return mips_inst.Sw(r, dest, offset, text)
            case 2:
                return mips_inst.Sh(r, dest, offset, text)
            case 1:
                return mips_inst.Sb(r, dest, offset, text)
        assert False, "unsupported type size"

    def store_value(
        self,
        i: ir.Instruction,
        r: Reg | Regf,
        offset: int | None,
        text: str | mips_inst.Comment = "",
        mem_base: Reg = Reg.fp,
    ) -> mips_inst.Instruction:
        """
        Store content of a normal/float register ``r`` at ``offset`` from the frame pointer.

        :param i: The of which the result is stored. Needed for the size of it's type.
        :param r: The register to store the value in.
        :param offset: The offset to store the value at.
        :param text: The comment to add to the instruction.
        """
        if isinstance(r, Regf):
            return self.store_float(i, r, offset, text, mem_base)
        return self.store_int(i, r, offset, text, mem_base)

    def copy_data(
        self,
        src_reg: Reg,
        src_ofst: int,
        dst_reg: Reg,
        dst_ofst: int,
        len: int,
    ) -> mips_inst.Instruction:
        """
        Copy ``len`` bytes of data from ``src_ofst``(``src_reg``) to ``dst_ofst``(``dst_reg``).
        """

        if len == 0:
            return []
        assert src_reg != Reg.t7, dst_reg != Reg.t7

        move_instrs: list[mips_inst.Instruction] = []
        done = 0
        todo = len

        # copy data
        while todo > 0:
            move_instrs.extend(
                (
                    mips_inst.Lw(
                        Reg.t7,
                        src_reg,
                        src_ofst - done,
                        mips_inst.Comment(f"load 4 at -{done} from src start"),
                    ),
                    mips_inst.Sw(
                        Reg.t7,
                        dst_reg,
                        dst_ofst - done,
                        mips_inst.Comment(f"store 4 at -{done} from dest start"),
                    ),
                )
            )
            todo -= 4
            done += 4
        return move_instrs

    def calc_arg_offsets(self, args: list[ir.Instruction], base: int) -> list[_ArgOffset]:
        """
        Calculate the offsets of the provided arguments.
        
        :param args: The arguments to calculate the offsets for.
        :param base: The base offset.
        """
        args_with_offset: list[_ArgOffset] = []
        for arg in args:
            # get typesize of arg
            arg_size: int = get_type_size(arg.type)

            # create arg
            args_with_offset.append(_ArgOffset(arg, base, arg_size))

            # offset stack
            base -= arg_size
        return args_with_offset
