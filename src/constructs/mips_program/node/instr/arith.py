"""
All arithmetic MIPS instructions.
"""

from src.constructs.mips_program.node.instr.instruction import BinOpMixin, Instruction, UnOpMixin
from src.constructs.mips_program.node.reg import Reg
from src.constructs.mips_program.node.instr.comment import Comment


class ArithOp(Instruction):
    """
    Base class for all MIPS arithmetic operations.
    """

    op: str
    "Operation to perform"

    dest: Reg
    "Destination register to write operation result to"

    def __init__(self, op: str, dest: Reg, text: str | Comment = "") -> None:
        super().__init__(text)
        self.op = op
        self.dest = dest


class ArithUnOp(ArithOp, UnOpMixin):
    """
    Base class for all MIPS arithmetic unary operations
    """

    def __init__(self, op: str, dest: Reg, operand: Reg, text: str | Comment = "") -> None:
        ArithOp.__init__(self, op, dest, text)
        UnOpMixin.__init__(self, operand)

    def __str__(self) -> str:
        return f"{self.op} {self.dest}, {self.operand} {super().__str__()}"


class ArithBinOp(ArithOp, BinOpMixin):
    """
    Base class for all MIPS arithmetic binary operations
    """

    def __init__(self, op: str, dest: Reg, operand1: Reg, operand2: Reg | int, text: str | Comment = "") -> None:
        ArithOp.__init__(self, op, dest, text)
        BinOpMixin.__init__(self, operand1, operand2)

    def __str__(self) -> str:
        return f"{self.op} {self.dest}, {self.operand1}, {self.operand2} {super().__str__()}"


class Add(ArithBinOp):
    """
    MIPS `add` instruction.
    Add contents of :operand1: and :operand2: registers and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: Reg, text: str | Comment = "") -> None:
        super().__init__("add", dest, operand1, operand2, text)


class Addi(ArithBinOp):
    """
    MIPS `addi` (add immediate) instruction.
    Add :operand2: immediate to the contents of the :operand1: register and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: int, text: str | Comment = "") -> None:
        super().__init__("addi", dest, operand1, operand2, text)


class Addiu(ArithBinOp):
    """
    MIPS `addiu` (add immediate unsigned) instruction.
    Add :operand2: immediate to the contents of the :operand1: register and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: int, text: str | Comment = "") -> None:
        super().__init__("addiu", dest, operand1, operand2, text)


class Addu(ArithBinOp):
    """
    MIPS `addu` (add unsigned) instruction.
    Add contents of :operand1: and :operand2: registers and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: Reg, text: str | Comment = "") -> None:
        super().__init__("addu", dest, operand1, operand2, text)


class Div(BinOpMixin, Instruction):
    """
    MIPS `div` (divide) instruction.
    Divide contents of :operand1: register by :operand2: register.
    Store the result into `hi` register and remainder into `lo` register.
    """

    def __init__(self, operand1: Reg, operand2: Reg, text: str | Comment = "") -> None:
        BinOpMixin.__init__(self, operand1, operand2)
        Instruction.__init__(self, text)

    def __str__(self) -> str:
        return f"div {self.operand1}, {self.operand2} {super().__str__()}"


class Divu(BinOpMixin, Instruction):
    """
    MIPS `divu` (divide unsigned) instruction.
    Divide contents of :operand1: register by :operand2: register.
    Store the result into `hi` register and remainder into `lo` register.
    """

    def __init__(self, operand1: Reg, operand2: Reg, text: str | Comment = "") -> None:
        BinOpMixin.__init__(self, operand1, operand2)
        Instruction.__init__(self, text)

    def __str__(self) -> str:
        return f"divu {self.operand1}, {self.operand2} {super().__str__()}"


class Mul(ArithBinOp):
    """
    MIPS `mul` (multiply (without overflow)) instruction.
    Multiply contents of :operand1: and :operand2: registers and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: Reg, text: str | Comment = "") -> None:
        super().__init__("mul", dest, operand1, operand2, text)


class Mult(ArithBinOp):
    """
    MIPS `mult` (multiply (with overflow)) instruction.
    Multiply contents of :operand1: and :operand2: registers and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: Reg, text: str | Comment = "") -> None:
        super().__init__("mult", dest, operand1, operand2, text)


class Sub(ArithBinOp):
    """
    MIPS `sub` instruction.
    Subtract contents of :operand2: register from contents of :operand1: register and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: Reg, text: str | Comment = "") -> None:
        super().__init__("sub", dest, operand1, operand2, text)


class Subu(ArithBinOp):
    """
    MIPS `subu` (subtract unsigned) instruction.
    Subtract contents of :operand2: register from contents of :operand1: register and store result into :dest: register.
    """

    def __init__(self, dest: Reg, operand1: Reg, operand2: Reg, text: str | Comment = "") -> None:
        super().__init__("subu", dest, operand1, operand2, text)
