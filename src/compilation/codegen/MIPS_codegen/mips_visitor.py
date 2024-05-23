import math
import struct

import llvmlite.ir as ir
import llvmlite.ir.instructions as ir_inst
from src.constructs.mips_program import Global, MipsProgram, Variables
from src.constructs.mips_program.node import Label, LabeledBlock, Reg, Regf
from src.constructs.mips_program.node import instr as mips_inst

from .alloca_mixin import MVHandleAllocaMixin
from .base import assert_type, get_args_size, get_type_size
from .branch_mixin import MVHandleBranchMixin
from .call_mixin import MVHandleCallMixin
from .cast_mixin import MVHandleCastMixin
from .conditional_branch_mixin import MVHandleConditionalBranchMixin
from .fcmp_mixin import MVHandleFCMPMixin
from .gep_mixin import MVHandleGEPMixin
from .icmp_mixin import MVHandleICMPMixin
from .instruction_mixin import MVHandleInstructionMixin
from .load_mixin import MVHandleLoadMixin
from .ret_mixin import MVHandleRetMixin
from .store_mixin import MVHandleStoreMixin
from .switch_mixin import MVHandleSwitchMixin

"""
MIPS code layout:
- module name
- data (static vars)
- text (code)
  - labels
  - instructions


LLVM structure:
Module
- Function
  - Block
    - Instruction
    - Instruction
  - Block
    - Instruction
    - Instruction
- Function
- ...
"""

# TODO:
#  -printf
#  -scanf
#

# pseudo instructions may only use $t0 !!!


class MipsVisitor(
    ir.Visitor,
    MVHandleAllocaMixin,
    MVHandleBranchMixin,
    MVHandleCallMixin,
    MVHandleConditionalBranchMixin,
    MVHandleGEPMixin,
    MVHandleLoadMixin,
    MVHandleRetMixin,
    MVHandleStoreMixin,
    MVHandleSwitchMixin,
    MVHandleICMPMixin,
    MVHandleFCMPMixin,
    MVHandleCastMixin,
    MVHandleInstructionMixin,
):
    def __init__(self) -> None:
        self.tree = MipsProgram()
        self.variables = Variables()
        self.stack_offset = 0
        super().__init__()

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

    def get_glob_type(self, glob_initializer, glob_type: ir.Type) -> str:
        if glob_initializer is not None:
            if isinstance(glob_initializer.constant, bytearray):
                return "ascii"
            else:
                match glob_type:
                    case ir.FloatType():
                        return "float"
                    case ir.IntType():
                        return "word" if get_type_size(glob_type) == 4 else "byte"
                    case ir.PointerType():
                        return "space"
                    case ir.ArrayType():
                        return self.get_glob_type(glob_initializer, glob_type.element)
                    case _:
                        assert False
        return "space"

    def get_glob_values(self, initializer, glob_type: ir.Type) -> list[str]:
        match initializer:
            case ir.Constant():
                if isinstance(initializer.constant, bytearray):
                    return [f'"{initializer.constant.decode("utf8").encode("unicode_escape").decode("utf8")}"']
                match initializer.type:
                    case ir.PointerType():
                        if initializer.constant.startswith("getelementptr"):
                            for elem in initializer.constant.split():
                                if elem[0] == "@":
                                    return ["$LC" + elem[2:-2]]
                        return [str(get_type_size(glob_type))]
                    case ir.ArrayType():
                        res = []
                        for element in initializer.constant:
                            res += self.get_glob_values(element, glob_type)
                        return res
                    case _:
                        return [initializer.constant]
            case None:
                return [str(get_type_size(glob_type))]
            case _:
                assert False

    def visit_Global(self, variable: ir.GlobalVariable):
        print(f"- {type(variable).__name__}")
        name = variable.name
        glob_type: str = self.get_glob_type(variable.initializer, variable.type.pointee)
        glob_values: list[str] = self.get_glob_values(variable.initializer, variable.type.pointee)
        # type of glob is string
        if glob_type == "ascii":
            name = "$LC" + name
        # glob value is a GEP to a string
        for glob_value in glob_values:
            if len(str(glob_value)) >= 3 and "$LC" == glob_value[:3]:
                glob_type = "word"
                break
        glob = Global(name, glob_type, glob_values)
        self.tree.data.append(glob)

    def visit_Function(self, func: ir_inst.Function):
        """Visit a function."""
        print(f"- {type(func).__name__}")

        self.variables.clear()
        self.stack_offset = 0
        self.new_function_started = True
        match func.name:
            case "printf":
                pass
            case "scanf":
                pass
            case _:
                super().visit_Function(func)

    def visit_BasicBlock(self, bb: ir_inst.Block):
        """Visit a basic block."""
        print(f"  - {type(bb).__name__}")

        self.tree.add_block(LabeledBlock(Label(f"{self.function.name}.{bb.name}")))

        # if new function started, start by creating new stack frame
        if self.new_function_started:
            self.last_block.add_instr(
                # store frame pointer at top of stack
                mips_inst.Sw(Reg.fp, Reg.sp, 0, "new stack frame"),  # sw  $fp, 0($sp)
                # set frame pointer
                mips_inst.Move(Reg.fp, Reg.sp),  # move    $fp, $sp
                # store return address on stack
                mips_inst.Sw(Reg.ra, Reg.fp, -4),  # sw  $ra, -4($fp)
                # move stack pointer down
                mips_inst.Addiu(Reg.sp, Reg.sp, -8),  # subiu   $sp, $sp, 8
                mips_inst.Blank(),
            )
            self.new_function_started = False
            self.stack_offset -= 8  # offset stack by 2 words (fp, ra)
        super().visit_BasicBlock(bb)

    def visit_Instruction(self, instr: ir_inst.Instruction):
        """Visit an instruction."""
        print(f"    - {type(instr).__name__}")

        match instr:
            case ir_inst.AllocaInstr():
                super().handle_alloca(instr)

            case ir_inst.Branch():
                super().handle_branch(instr)

            case ir_inst.CallInstr():
                super().handle_call(instr)

            case ir_inst.ConditionalBranch():
                super().handle_conditional_branch(instr)

            case ir_inst.Comment():
                self.last_block.add_instr(mips_inst.CComment(instr.text))

            case ir_inst.GEPInstr():
                super().handle_gep(instr)

            case ir_inst.LoadInstr():
                super().handle_load(instr)

            case ir_inst.Ret():
                super().handle_ret(instr)

            case ir_inst.StoreInstr():
                super().handle_store(instr)

            case ir_inst.SwitchInstr():
                super().handle_switch(instr)

            case ir_inst.ICMPInstr():
                super().handle_icmp(instr)

            case ir_inst.FCMPInstr():
                super().handle_fcmp(instr)

            case ir_inst.CompareInstr():
                print("unhandled!")

            case ir_inst.CastInstr():
                super().handle_cast(instr)

            case ir_inst.Instruction():
                assert_type(instr, "Instruction")
                super().handle_instruction(instr)

            case _:
                raise ValueError(f"Unsupported type: '{type(instr).__name__}'")
