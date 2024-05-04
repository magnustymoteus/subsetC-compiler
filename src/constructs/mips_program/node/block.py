from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.node import Node
from src.constructs.mips_program.node.instr.instruction import Instruction


class LabeledBlock(Node):
    """
    Node representing a MIPS labeled block.
    The block has a label and a list of instructions.
    """

    label: Label
    "Block label"

    instructions: list[Instruction]
    "List of instructions in the block"

    def __init__(self, label: Label) -> None:
        self.label = label
        self.instructions = []
        super().__init__()

    def __str__(self) -> str:
        instructions = "".join([f"    {i}\n" for i in self.instructions])
        return f"{self.label}\n{instructions}"

    def append_inst(self, instr: Instruction):
        """Add an instruction to the block"""
        self.instructions.append(instr)

    def extend_inst(self, instrs: list[Instruction]):
        """Add a list of instructions to the block"""
        self.instructions.extend(instrs)
