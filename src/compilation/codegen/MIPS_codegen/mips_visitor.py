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
