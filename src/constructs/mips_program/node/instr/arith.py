"""
All arithmetic MIPS instructions.
"""

from src.constructs.mips_program.node.instr.instruction import BinOpMixin, Instruction, UnOpMixin
from src.constructs.mips_program.node.reg import Reg


class ArithOp(Instruction):
    """
    Base class for all MIPS arithmetic operations.
    """

    op: str
    "Operation to perform"

    dest: Reg
    "Destination register to write operation result to"

    def __init__(self, op: str, dest: Reg) -> None:
        super().__init__()
        self.op = op
        self.dest = dest


class ArithUnOp(ArithOp, UnOpMixin):
    """
    Base class for all MIPS arithmetic unary operations
    """

    def __init__(self, op: str, dest: Reg, operand: Reg) -> None:
        ArithOp.__init__(self, op, dest)
        UnOpMixin.__init__(self, operand)

    def __str__(self) -> str:
        return f"{self.op} {self.dest}, {self.operand}"


class ArithBinOp(ArithOp, BinOpMixin):
    """
    Base class for all MIPS arithmetic binary operations
    """

    def __init__(self, op: str, dest: Reg, operand1: Reg, operand2: Reg) -> None:
        ArithOp.__init__(self, op, dest)
        BinOpMixin.__init__(self, operand1, operand2)

    def __str__(self) -> str:
        return f"{self.op} {self.dest}, {self.operand1}, {self.operand2}"


class Add(ArithBinOp):
    """
    MIPS `add` instruction.
    Add contents of :operand1: and :operand2: registers and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: Reg) -> None:
        super().__init__("add", dest, operand1, operand2)


class Addi(ArithBinOp):
    """
    MIPS `addi` (add immediate) instruction.
    Add :operand2: immediate to the contents of the :operand1: register and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: int) -> None:
        super().__init__("addi", dest, operand1, operand2)


class Addiu(ArithBinOp):
    """
    MIPS `addiu` (add immediate unsigned) instruction.
    Add :operand2: immediate to the contents of the :operand1: register and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: int) -> None:
        super().__init__("addiu", dest, operand1, operand2)


class Addu(ArithBinOp):
    """
    MIPS `addu` (add unsigned) instruction.
    Add contents of :operand1: and :operand2: registers and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: Reg) -> None:
        super().__init__("addu", dest, operand1, operand2)


class Div(BinOpMixin):
    """
    MIPS `div` (divide) instruction.
    Divide contents of :operand1: register by :operand2: register.
    Store the result into `hi` register and remainder into `lo` register.
    """

    def __init__(self, operand1: Reg, operand2: Reg) -> None:
        super().__init__(operand1, operand2)

    def __str__(self) -> str:
        return f"div {self.operand1}, {self.operand2}"


class Divu(BinOpMixin):
    """
    MIPS `divu` (divide unsigned) instruction.
    Divide contents of :operand1: register by :operand2: register.
    Store the result into `hi` register and remainder into `lo` register.
    """

    def __init__(self, operand1: Reg, operand2: Reg) -> None:
        super().__init__(operand1, operand2)

    def __str__(self) -> str:
        return f"divu {self.operand1}, {self.operand2}"


class Mul(ArithBinOp):
    """
    MIPS `mul` (multiply (without overflow)) instruction.
    Multiply contents of :operand1: and :operand2: registers and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: Reg) -> None:
        super().__init__("mul", dest, operand1, operand2)


class Mult(ArithBinOp):
    """
    MIPS `mult` (multiply (with overflow)) instruction.
    Multiply contents of :operand1: and :operand2: registers and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: Reg) -> None:
        super().__init__("mult", dest, operand1, operand2)


class Sub(ArithBinOp):
    """
    MIPS `sub` instruction.
    Subtract contents of :operand2: register from contents of :operand1: register and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: Reg) -> None:
        super().__init__("sub", dest, operand1, operand2)


class Subu(ArithBinOp):
    """
    MIPS `subu` (subtract unsigned) instruction.
    Subtract contents of :operand2: register from contents of :operand1: register and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: Reg) -> None:
        super().__init__("subu", dest, operand1, operand2)
