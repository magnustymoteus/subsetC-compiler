from __future__ import annotations
from copy import deepcopy

from src.constructs.mips_program.node.node import Node
from src.constructs.mips_program.node.reg import Reg

# from src.constructs.mips_program.node.instr.comment import Comment
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from src.constructs.mips_program.node.instr.comment import Comment


class Instruction(Node):
    """Base node representing a MIPS instruction"""

    text: str
    "Inline comment for the instruction"

    def __init__(self, text: Union[str, "Comment"] = "") -> None:
        super().__init__()
        self.text = text

    def __str__(self) -> str:
        from src.constructs.mips_program.node.instr.comment import Comment

        if isinstance(self.text, Comment):
            return f"  {self.text}"
        else:
            return f"  #{self.text}" if self.text else ""

    def replace_placeholder(self, name: str, replacement: Any) -> Instruction:
        for attr in self.__dict__.keys():
            if isinstance(self.__dict__[attr], Placeholder) and name == self.__dict__[attr].name:
                self.__dict__[attr] = replacement
        return self


class Placeholder(Instruction):
    """
    Node representing a placeholder instruction
    """

    name: str
    "Name of the placeholder"

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def __str__(self) -> str:
        # assert False, "placeholders have no string representation"
        return f"{self.name}"

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Placeholder):
            return self.name == value.name
        elif isinstance(value, str):
            return self.name == value
        return super().__eq__(value)

class BinOpMixin:
    """Mixin that adds `operand1` and `operand2` attributes to the class"""

    operand1: Reg
    "Register containing left operand value"

    operand2: Reg
    "Register containing right operand value"

    def __init__(self, operand1: Reg, operand2: Reg) -> None:
        self.operand1 = operand1
        self.operand2 = operand2
