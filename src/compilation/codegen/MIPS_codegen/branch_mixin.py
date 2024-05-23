import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase
from src.constructs.mips_program.node.label import Label


class MVHandleBranchMixin(MVBase):
    def handle_branch(self, instr: ir.Branch):
        block: ir.Block = instr.operands[0]
        assert isinstance(block, ir.Block)
        self.last_block.add_instr(
            mips_inst.J(Label(f"{self.function.name}.{block.name}"), mips_inst.IrComment(f"{instr}")),
        )
