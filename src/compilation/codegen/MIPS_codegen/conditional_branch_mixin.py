import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg


class MVHandleConditionalBranchMixin(MVBase):
    def handle_conditional_branch(self, instr: ir.ConditionalBranch):
        condition, true_block, false_block = instr.operands

        self.last_block.add_instr(
            # Load the condition value into a register
            self.load_int(condition, Reg.t1),
            # Branch if the condition is true
            mips_inst.Bne(
                Reg.t1,
                Reg.zero,
                Label(f"{self.function.name}.{true_block.name}"),
                mips_inst.Comment(f"{instr} condition true"),
            ),
            # Branch to the false block if the condition is zero
            mips_inst.J(
                Label(f"{self.function.name}.{false_block.name}"), mips_inst.Comment(f"{instr} condition false")
            ),
        )
