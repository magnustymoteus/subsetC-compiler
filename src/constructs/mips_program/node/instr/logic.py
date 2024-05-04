"""
All logic MIPS instructions.
"""

from src.constructs.mips_program.node.instr.arith import ArithBinOp
from src.constructs.mips_program.node.reg import Reg


class And(ArithBinOp):
    """
    MIPS `and` instruction.
    Store result of bitwise AND of :operand1: and :operand2: registers and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: Reg) -> None:
        super().__init__("and", dest, operand1, operand2)


class Andi(ArithBinOp):
    """
    MIPS `andi` (and immediate) instruction.
    Store result of bitwise AND of :operand1: register and :operand2: immediate and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: int) -> None:
        super().__init__("andi", dest, operand1, operand2)


class Or(ArithBinOp):
    """
    MIPS `or` instruction.
    Store result of bitwise OR of :operand1: and :operand2: registers and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: Reg) -> None:
        super().__init__("or", dest, operand1, operand2)


class Ori(ArithBinOp):
    """
    MIPS `ori` (or immediate) instruction.
    Store result of bitwise OR of :operand1: register and :operand2: immediate and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: int) -> None:
        super().__init__("ori", dest, operand1, operand2)


class Ssl(ArithBinOp):
    """
    MIPS `ssl` (shift left logical) instruction.
    Shift :operand1: by :operand2: bits left and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: int) -> None:
        super().__init__("ssl", dest, operand1, operand2)


class Srl(ArithBinOp):
    """
    MIPS `srl` (shift right logical) instruction.
    Shift :operand1: by :operand2: bits right and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: int) -> None:
        super().__init__("srl", dest, operand1, operand2)
