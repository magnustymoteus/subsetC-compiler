import llvmlite.ir as ir
import llvmlite.ir.instructions as ir_inst

from src.constructs.mips_program import MipsProgram
from src.constructs.mips_program.node import LabeledBlock, Reg, instr as mips_inst


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


class MipsVisitor(ir.Visitor):
    tree: MipsProgram
    "Tree of the mips program blocks with instructions."

    mips_block: LabeledBlock | None
    "Current block being visited."

    def __init__(self) -> None:
        self.tree = MipsProgram()
        self.mips_block = None
        super().__init__()

    def visit(self, module: ir.Module):
        """Visit a module. Top level visit function."""
        print(type(module).__name__)
        super().visit(module)

    def visit_Function(self, func: ir_inst.Function):
        """Visit a function."""
        print(f"- {type(func).__name__}")

        super().visit_Function(func)

    def visit_BasicBlock(self, bb: ir_inst.Block):
        """Visit a basic block."""
        print(f"  - {type(bb).__name__}")

        self.mips_block = LabeledBlock(bb.name)
        super().visit_BasicBlock(bb)
        self.mips_block = None

    def visit_Instruction(self, instr: ir_inst.Instruction):
        from src.constructs.mips_program.node import Reg

        """Visit an instruction."""
        match instr:
            case ir_inst.AllocaInstr():
                """
                :count: array size
                :size: size of array content, in bytes
                advance sp by :count: * :size:
                save stack offset of array start

                subu $sp, $sp, :count:*:size:
                # save variable offset from $fp
                """
                # self.mips_block.append_inst(node.Subu(Reg.sp, Reg.sp, count * size))
                pass
            case ir_inst.Branch():
                pass
            case ir_inst.CallInstr():
                """
                # MIPS code:
                sw  $fp, 0($sp)         # store frame pointer at top of stack
                move    $fp, $sp        # set frame pointer
                subiu   $sp, $sp, 8     # move stack pointer down
                sw  $ra, -4($fp)        # store return address on stack
                """
                pass
            case ir_inst.ConditionalBranch():
                pass
            case ir_inst.Comment():
                self.mips_block.add_instr(mips_inst.Comment(instr.text))
            case ir_inst.GEPInstr():
                pass
            case ir_inst.LoadInstr():
                pass
            case ir_inst.Ret():
                """
                # MIPS code:
                lw  $ra, -4($fp)    # restore return register
                move    $sp, $fp    # move stack pointer to start of frame
                lw  $fp, 0($sp)     # restore previous frame pointer
                jr  $ra             # jump back
                """
                self.mips_block.add_instr(
                    mips_inst.Lw(Reg.ra, Reg.fp, -4),
                    mips_inst.Move(Reg.sp, Reg.fp),
                    mips_inst.Lw(Reg.fp, Reg.sp),
                    mips_inst.Jr(Reg.ra),
                )
            case ir_inst.StoreInstr():
                pass
            case ir_inst.SwitchInstr():
                pass
            case ir_inst.Instruction():
                pass
            case _:
                raise ValueError(f"Unsupported instruction: {type(instr).__name__}")
        print(f"    - {type(instr).__name__}")
