from src.constructs.mips_program.node.node import Node
from src.constructs.mips_program.node.reg import Reg
from src.constructs.mips_program.node.instr.comment import Comment


class Instruction(Node):
    """Base node representing a MIPS instruction"""

    text: str
    "Inline comment for the instruction"

    def __init__(self, text: str | Comment = "") -> None:
        super().__init__()
        self.text = text

    def __str__(self) -> str:
        if isinstance(self.text, Comment):
            return f"  {self.text}"
        else:
            return f"  #{self.text}" if self.text else ""



class UnOpMixin:
    """Mixin that adds an `operand` attribute to the class"""

    operand: Reg
    "Register containing operand value"

    def __init__(self, operand: Reg) -> None:
        self.operand = operand


class BinOpMixin:
    """Mixin that adds `operand1` and `operand2` attributes to the class"""

    operand1: Reg
    "Register containing left operand value"

    operand2: Reg
    "Register containing right operand value"

    def __init__(self, operand1: Reg, operand2: Reg) -> None:
        self.operand1 = operand1
        self.operand2 = operand2
