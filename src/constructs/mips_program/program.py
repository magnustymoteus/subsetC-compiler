from src.constructs.mips_program.node import LabeledBlock


class MipsProgram:
    blocks: list[LabeledBlock]

    def __init__(self) -> None:
        self.blocks = []

    def add_block(self, block: LabeledBlock):
        self.blocks.append(block)

    def to_asm(self) -> str:
        globl = ".globl main"
        # convert all blocks in the program to asm and join them with a newline
        blocks = "\n".join([f"{b}" for b in self.blocks])
        return f"{globl}\n\n{blocks}"
