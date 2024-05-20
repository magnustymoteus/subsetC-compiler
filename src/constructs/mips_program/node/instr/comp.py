"""
All comparison MIPS instructions.
"""

from src.constructs.mips_program.node.instr.instruction import Instruction
from src.constructs.mips_program.node.reg import Reg
from src.constructs.mips_program.node.instr.arith import Addi, Subu
from src.constructs.mips_program.node.instr.logic import Ori
from src.constructs.mips_program.node.instr.comment import Comment


class SlInstruction(Instruction):
    """
    Base class for MIPS set less than
    """

    dest: Reg
    "Destination register to set result in"

    operand1: Reg
    "First operand to compare"

    def __init__(self, dest: Reg, operand1: Reg, text: str | Comment = "") -> None:
        super().__init__(text)
        self.dest = dest
        self.operand1 = operand1


class Slt(SlInstruction):
    """
    MIPS `slt` (set less than) instruction.
    Set :dest: register to 1 if :operand1: register is less than contents of :operand2: register and 0 otherwise.
    """

    operand2: Reg
    "Second operand to compare"

    def __init__(self, dest: Reg, operand1: Reg, operand2: Reg, text: str | Comment = "") -> None:
        super().__init__(dest, operand1, text)
        self.operand2 = operand2

    def __str__(self) -> str:
        return f"slt {self.dest}, {self.operand1}, {self.operand2}{super().__str__()}"


class Slti(SlInstruction):
    """
    MIPS `slti` (set less than immediate) instruction.
    Set :dest: register to 1 if :operand1: register is less than :operand2: immediate and 0 otherwise.
    """

    operand2: int
    "Second operand to compare"

    def __init__(self, dest: Reg, operand1: Reg, operand2: int, text: str | Comment = "") -> None:
        super().__init__(dest, operand1, text)
        self.operand2 = operand2

    def __str__(self) -> str:
        return f"slti {self.dest}, {self.operand1}, {self.operand2}{super().__str__()}"


class Sltu(SlInstruction):
    """
    MIPS `sltu` (set less than unsigned) instruction.
    Set :dest: register to 1 if :operand1: register is less than contents of :operand2: register and 0 otherwise.
    """

    operand2: int
    "Second operand to compare"

    def __init__(self, dest: Reg, operand1: Reg, operand2: int | Reg, text: str | Comment = "") -> None:
        super().__init__(dest, operand1, text)
        self.operand2 = operand2

    def __str__(self) -> str:
        return f"sltu {self.dest}, {self.operand1}, {self.operand2}{super().__str__()}"


class Sle(Instruction):
    """
    MIPS `sle` (set less than or equal) instruction.
    Set :dest: register to 1 if :operand1: register is less than or equal to contents of :operand2: register and 0 otherwise.
    """

    def __new__(
        cls, dest: Reg, lhs: Reg, rhs: Reg | int, text: str | Comment = ""
    ) -> tuple[Slt, Ori, Subu] | tuple[Addi, Slt, Ori, Subu]:
        """
        example: sle $t1, $t2, $t3
        :param dest: $t1
        :param lhs: $t2
        :param rhs: $t3 (if register) or 5 (for example if immediate)
        """
        if isinstance(rhs, Reg):
            return Slt(dest, rhs, lhs, text), Ori(Reg.t0, Reg.zero, 1), Subu(dest, Reg.t0, dest)
        if isinstance(rhs, int):
            return (
                Addi(Reg.t0, Reg.zero, rhs, text),
                Slt(dest, Reg.t0, lhs),
                Ori(Reg.t0, Reg.zero, 1),
                Subu(dest, Reg.t0, dest),
            )


class Sne(Instruction):
    """
    MIPS `sne` (set not equal) instruction.
    Set :dest: register to 1 if :operand1: register is not equal to contents of :operand2: register and 0 otherwise.
    """

    def __new__(
        cls, dest: Reg, lhs: Reg, rhs: Reg | int, text: str | Comment = ""
    ) -> tuple[Subu, Sltu] | tuple[Addi, Subu, Sltu]:
        """
        example: sne $t1, $t2, $t3
        :param dest: $t1
        :param lhs: $t2
        :param rhs: $t3 (if register) or 5 (for example if immediate)
        """
        if isinstance(rhs, Reg):
            return Subu(dest, lhs, rhs, text), Sltu(dest, Reg.zero, dest)
        if isinstance(rhs, int):
            return Addi(Reg.t0, Reg.zero, rhs, text), Subu(dest, lhs, Reg.t0), Sltu(dest, Reg.zero, dest)


class Seq(Instruction):
    """
    MIPS `seq` (set equal) instruction.
    """

    def __new__(
        cls, dest: Reg, lhs: Reg, rhs: Reg | int, text: str | Comment = ""
    ) -> tuple[Subu, Ori, Sltu] | tuple[Addi, Subu, Ori, Sltu]:
        """
        example: seq $t1, $t2, $t3
        :param dest: $t1
        :param lhs: $t2
        :param rhs: $t3 (if register) or 5 (for example if immediate)
        """
        if isinstance(rhs, Reg):
            return Subu(dest, lhs, rhs, text), Ori(Reg.t0, Reg.zero, 1), Sltu(dest, dest, Reg.t0)
        if isinstance(rhs, int):
            return (
                Addi(Reg.t0, Reg.zero, rhs, text),
                Subu(dest, lhs, Reg.t0),
                Ori(Reg.t0, Reg.zero, 1),
                Sltu(dest, dest, Reg.t0),
            )
