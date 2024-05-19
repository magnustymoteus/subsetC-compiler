"""
All comparison MIPS instructions.
"""

from src.constructs.mips_program.node.instr.instruction import Instruction
from src.constructs.mips_program.node.reg import Reg
from src.constructs.mips_program.node.instr.arith import Addi, Subu
from src.constructs.mips_program.node.instr.logic import Ori


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

class Sltu(SlInstruction):
    """
    MIPS `sltu` (set less than unsigned) instruction.
    Set :dest: register to 1 if :operand1: register is less than contents of :operand2: register and 0 otherwise.
    """
    operand2: int
    "Second operand to compare"

    def __init__(self, dest: Reg, operand1: Reg, operand2: int | Reg) -> None:
        super().__init__(dest, operand1)
        self.operand2 = operand2

    def __str__(self) -> str:
        return f"sltu {self.dest}, {self.operand1}, {self.operand2}"


class Sle(SlInstruction):
    """
    MIPS `sle` (set less than or equal) instruction.
    Set :dest: register to 1 if :operand1: register is less than or equal to contents of :operand2: register and 0 otherwise.
    """

    def __new__(cls, dest: Reg, lhs: Reg, rhs: Reg | int) -> tuple[Slt, Ori, Subu] | tuple[Addi, Slt, Ori, Subu]:
        """
        example: sle $t1, $t2, $t3
        :param dest: $t1
        :param lhs: $t2
        :param rhs: $t3 (if register) or 5 (for example if immediate)
        """
        if isinstance(rhs, Reg):
            return Slt(dest, rhs, lhs), Ori(Reg.t0, Reg.zero, 1), Subu(dest, Reg.t0, dest)
        if isinstance(rhs, int):
            return Addi(Reg.t0, Reg.zero, rhs), Slt(dest, Reg.t0, lhs), Ori(Reg.t0, Reg.zero, 1), Subu(dest, Reg.t0,
                                                                                                         dest)

    def __str__(self) -> str:
        return f"sle {self.dest}, {self.operand1}, {self.operand2}"


class Sne(SlInstruction):
    """
    MIPS `sne` (set not equal) instruction.
    Set :dest: register to 1 if :operand1: register is not equal to contents of :operand2: register and 0 otherwise.
    """

    def __new__(cls, dest: Reg, lhs: Reg, rhs: Reg | int) -> tuple[Subu, Sltu] | tuple[Addi, Subu, Sltu]:
        """
        example: sne $t1, $t2, $t3
        :param dest: $t1
        :param lhs: $t2
        :param rhs: $t3 (if register) or 5 (for example if immediate)
        """
        if isinstance(rhs, Reg):
            return Subu(dest, lhs, rhs), Sltu(dest, Reg.zero, dest)
        if isinstance(rhs, int):
            return Addi(Reg.t0, Reg.zero, rhs), Subu(dest, lhs, Reg.t0), Sltu(dest, Reg.zero, dest)

    def __str__(self) -> str:
        return f"sle {self.dest}, {self.operand1}, {self.operand2}"


# TODO : add sge
