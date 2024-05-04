"""
All conditional MIPS instructions.
"""

from src.constructs.mips_program.node.instr.instruction import Instruction
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg


class Branch(Instruction):
    """
    Base class for all MIPS branch instructions.
    """

    type: str
    "Type of branch instruction"

    label: Label
    "Destination address to branch to"

    lhs: Reg

    rhs: Reg | int

    def __init__(self, type: str, lhs: Reg, rhs: Reg | int, label: Label) -> None:
        super().__init__()
        self.type = type
        self.lhs = lhs
        self.rhs = rhs
        self.label = label

    def __str__(self) -> str:
        return f"{self.type} {self.lhs}, {self.rhs}, {self.label.label}"


class Beq(Branch):
    """
    MIPS `beq` (branch equal) instruction.
    """

    def __init__(self, lhs: Reg, rhs: Reg | int, label: Label) -> None:
        super().__init__("beq", lhs, rhs, label)


class Bge(Branch):
    """
    MIPS `bge` (branch greater than or equal) instruction.
    """

    def __init__(self, lhs: Reg, rhs: Reg | int, label: Label) -> None:
        super().__init__("bge", lhs, rhs, label)


class Bgt(Branch):
    """
    MIPS `bgt` (branch greater than) instruction.
    """

    def __init__(self, lhs: Reg, rhs: Reg | int, label: Label) -> None:
        super().__init__("bgt", lhs, rhs, label)


class Ble(Branch):
    """
    MIPS `ble` (branch less than or equal) instruction.
    """

    def __init__(self, lhs: Reg, rhs: Reg | int, label: Label) -> None:
        super().__init__("ble", lhs, rhs, label)


class Blt(Branch):
    """
    MIPS `blt` (branch less than) instruction.
    """

    def __init__(self, lhs: Reg, rhs: Reg | int, label: Label) -> None:
        super().__init__("blt", lhs, rhs, label)


class Bne(Branch):
    """
    MIPS `bne` (branch not equal) instruction.
    """

    def __init__(self, lhs: Reg, rhs: Reg | int, label: Label) -> None:
        super().__init__("bne", lhs, rhs, label)
