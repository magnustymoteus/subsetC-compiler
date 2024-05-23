import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg


class MVHandleSwitchMixin(MVBase):
    def handle_switch(self, instr: ir.SwitchInstr):
        # Load the switch variable value into a register
        assert isinstance(instr.operands[0], ir.LoadInstr)
        self.last_block.add_instr(self.load_value(instr.operands[0], Reg.t0))

        # Placeholder for jump instructions to case labels
        jump_instructions = []

        # Generate labels for each case and compare with the switch variable
        for case_value, case_block in instr.cases:
            case_label = Label(f"{self.function.name}.{case_block.name}")
            # Compare and jump if equal
            jump_instructions.append(
                mips_inst.Beq(Reg.t0, case_value.constant, case_label, mips_inst.Comment(f"Case {case_value}"))
            )

        # Default case
        if instr.default is not None:
            default_label = Label(f"{self.function.name}.{instr.default.name}")
            jump_instructions.append(mips_inst.J(default_label, mips_inst.Comment("Default case")))

        # Add jump instructions to the block
        for jump_instr in jump_instructions:
            self.last_block.add_instr(jump_instr)

        # Add a label at the end of the switch for exiting
        exit_label = Label(f"{self.function.name}.switch.end")
        self.last_block.add_instr(mips_inst.J(exit_label, mips_inst.Comment("Default case")))

        # Note: Actual case and default block instructions should be handled in their respective visit methods
