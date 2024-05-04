"""
All comparison MIPS instructions.
"""

from src.constructs.mips_program.node.instr.instruction import Instruction
from src.constructs.mips_program.node.reg import Reg


class SlInstruction(Instruction):
    """
    Base class for MIPS set less than
    """

    dest: Reg
    "Destination register to set result in"

    operand1: Reg
    "First operand to compare"

    def __init__(self, dest: Reg, operand1: Reg) -> None:
        super().__init__()
        self.dest = dest
        self.operand1 = operand1


class Slt(SlInstruction):
    """
    MIPS `slt` (set less than) instruction.
    Set :dest: register to 1 if :operand1: register is less than contents of :operand2: register and 0 otherwise.
    """

    operand2: Reg
    "Second operand to compare"

    def __init__(self, dest: Reg, operand1: Reg, operand2: Reg) -> None:
        super().__init__(dest, operand1)
        self.operand2 = operand2

    def __str__(self) -> str:
        return f"slt {self.dest}, {self.operand1}, {self.operand2}"


class Slti(SlInstruction):
    """
    MIPS `slti` (set less than immediate) instruction.
    Set :dest: register to 1 if :operand1: register is less than :operand2: immediate and 0 otherwise.
    """

    operand2: int
    "Second operand to compare"

    def __init__(self, dest: Reg, operand1: Reg, operand2: int) -> None:
        super().__init__(dest, operand1)
        self.operand2 = operand2

    def __str__(self) -> str:
        return f"slti {self.dest}, {self.operand1}, {self.operand2}"
