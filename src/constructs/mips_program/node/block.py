from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.node import Node
from src.constructs.mips_program.node.instr.instruction import Instruction

flatten = lambda x: [y for l in x for y in flatten(l)] if type(x) is list else [x]

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

    def add_instr(self, *instr: Instruction | list):
        """Add an instruction to the block"""
        self.instructions.append(flatten(instr))