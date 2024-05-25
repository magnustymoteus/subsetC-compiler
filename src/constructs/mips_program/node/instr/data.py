"""
All data manipulation MIPS instructions.
"""

from src.constructs.mips_program.node.instr.instruction import Instruction
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg, Regf
from src.constructs.mips_program.node.instr.comment import Comment


class La(Instruction):
    """
    MIPS `la` (load address) instruction.
    Load address of :label: label into :dest: register.
    """

    dest: Reg
    "Destination register to load into"

    label: Label
    "Value to load into register"

    def __init__(self, dest: Reg, label: Label, text: str | Comment = "") -> None:
        super().__init__(text)
        self.dest = dest
        self.label = label

    def __str__(self) -> str:
        return f"la {self.dest}, {self.label.label}{super().__str__()}"


class Li(Instruction):
    """
    MIPS `li` (load immediate) instruction.
    Load :value: immediate into lower 16 bits of :dest: register.
    """

    dest: Reg
    "Destination register to load into"

    value: int | str
    "Value to load into register"

    def __init__(self, dest: Reg, value: int | str, text: str | Comment = "") -> None:
        super().__init__(text)
        self.dest = dest
        self.value = value

    def __str__(self) -> str:
        return f"li {self.dest}, {self.value}{super().__str__()}"


class Lui(Li):
    """
    MIPS `lui` (load upper immediate) instruction.
    Load :value: immediate into upper 16 bits of :dest: register.
    """

    def __str__(self) -> str:
        return f"lui {self.dest}, {self.value}{Instruction.__str__(self)}"


class LoadInstruction(Instruction):
    """
    Base class for all load instructions.
    """

    op: str
    "Load instruction name"

    dest: Reg
    "Destination register to load into"

    src: Reg
    "Register containing source address to load from"

    offset: int
    "Offset from the source address"

    def __init__(self, op: str, dest: Reg, src: Reg | str, offset: int | None = 0, text: str | Comment = "") -> None:
        if offset is not None:
            assert -32768 <= offset <= 32767  # ? TODO exception

        super().__init__(text)
        self.op = op
        self.dest = dest
        self.src = src
        self.offset = offset
    
    def __str__(self) -> str:
        if self.offset is None:
            # global variable load
            return f"{self.op} {self.dest}, {self.src}{super().__str__()}"
        return f"{self.op} {self.dest}, {self.offset}({self.src}){super().__str__()}"


class Lw(LoadInstruction):
    """
    MIPS `lw` (load word) instruction.
    Load data at address in :src: register with offset :offset: into :dest: register.
    """

    def __init__(self, dest: Reg, src: Reg | str, offset: int | None = 0, text: str | Comment = "") -> None:
        super().__init__("lw", dest, src, offset, text)


class Lb(LoadInstruction):
    """
    MIPS `lb` (load byte) instruction.
    Load byte at address in :src: register with offset :offset: into :dest: register.
    """

    def __init__(self, dest: Reg, src: Reg, offset: int = 0, text: str | Comment = "") -> None:
        super().__init__("lb", dest, src, offset, text)


class Lbu(LoadInstruction):
    """
    MIPS `lbu` (load byte unsigned) instruction.
    Load byte at address in :src: register with offset :offset: into :dest: register.
    """

    def __init__(self, dest: Reg, src: Reg, offset: int = 0, text: str | Comment = "") -> None:
        super().__init__("lbu", dest, src, offset, text)

    
class Lh(LoadInstruction):
    """
    MIPS `lh` (load halfword) instruction.
    Load halfword at address in :src: register with offset :offset: into :dest: register.
    """

    def __init__(self, dest: Reg, src: Reg, offset: int = 0, text: str | Comment = "") -> None:
        super().__init__("lh", dest, src, offset, text)


class Lhu(LoadInstruction):
    """
    MIPS `lhu` (load halfword unsigned) instruction.
    Load halfword at address in :src: register with offset :offset: into :dest: register.
    """

    def __init__(self, dest: Reg, src: Reg, offset: int = 0, text: str | Comment = "") -> None:
        super().__init__("lhu", dest, src, offset, text)


class MfInstruction(Instruction):
    """
    Base class for MIPS `mfhi` and `mflo` instructions.
    """

    src: str
    "Special register to load from, can be `hi` or `lo`"

    dest: Reg
    "Destination register to move into"

    def __init__(self, src: str, dest: Reg, text: str | Comment = "") -> None:
        super().__init__(text)
        self.src = src
        self.dest = dest

    def __str__(self) -> str:
        return f"mf{self.src} {self.dest}{super().__str__()}"


class Mfhi(MfInstruction):
    """
    MIPS `lfhi` (load from hi) instruction.
    Load contents of the special `hi` register into :dest: register.
    """

    def __init__(self, dest: Reg, text: str | Comment = "") -> None:
        super().__init__("hi", dest, text)


class Mflo(MfInstruction):
    """
    MIPS `lflo` (load from lo) instruction.
    Load contents of the special `lo` register into :dest: register.
    """

    def __init__(self, dest: Reg, text: str | Comment = "") -> None:
        super().__init__("lo", dest, text)


class Move(Instruction):
    """
    MIPS `move` instruction.
    Move :src: register into :dest: register.
    """

    dest: Reg
    "Destination register to load into"

    src: Reg
    "Register containing source address to load from"

    def __init__(self, dest: Reg, src: Reg, text: str | Comment = "") -> None:
        super().__init__(text)
        self.dest = dest
        self.src = src

    def __str__(self) -> str:
        return f"move {self.dest}, {self.src}{super().__str__()}"


class StoreInstruction(Instruction):
    """
    Base class for MIPS `sw` and `sb` instructions.
    """

    op: str
    "Operation to perform"

    dest: Reg
    "Destination register to load into"

    src: Reg
    "Register containing source address to load from"

    offset: int
    "Offset from the source address"

    def __init__(self, op: str, src: Reg, dest: Reg, offset: int | None = 0, text: str | Comment = "") -> None:
        if offset is not None:
            assert -32768 <= offset <= 32767  # ? TODO exception
        super().__init__(text)
        self.op = op
        self.src = src
        self.dest = dest
        self.offset = offset

    def __str__(self) -> str:
        if self.offset is None:
            return f"{self.op} {self.src}, {self.dest}{super().__str__()}"
        return f"{self.op} {self.src}, {self.offset}({self.dest}){super().__str__()}"


class Sw(StoreInstruction):
    """
    MIPS `sw` (store word) instruction.
    Store data in the ``src`` register with at address ``dest`` with an offset ``offset`` in memory.
    """

    dest: Reg
    "Destination register to load into"

    src: Reg
    "Register containing source address to load from"

    offset: int
    "Offset from the source address"

    def __init__(self, src: Reg, dest: Reg, offset: int = 0, text: str | Comment = "") -> None:
        super().__init__("sw", src, dest, offset, text)


class Sb(StoreInstruction):
    """
    MIPS `sb` (store byte) instruction.
    Store data in the ``src`` register with at address ``dest`` with an offset ``offset`` in memory.
    """

    def __init__(self, src: Reg, dest: Reg, offset: int = 0, text: str | Comment = "") -> None:
        super().__init__("sb", src, dest, offset, text)

class Sbu(StoreInstruction):
    """
    MIPS `sbu` (store byte unsigned) instruction.
    Store data in the ``src`` register with at address ``dest`` with an offset ``offset`` in memory.
    """

    def __init__(self, src: Reg, dest: Reg, offset: int = 0, text: str | Comment = "") -> None:
        super().__init__("sbu", src, dest, offset, text)


class Sh(StoreInstruction):
    """
    MIPS `sh` (store halfword) instruction.
    Store data in the ``src`` register with at address ``dest`` with an offset ``offset`` in memory.
    """

    def __init__(self, src: Reg, dest: Reg, offset: int = 0, text: str | Comment = "") -> None:
        super().__init__("sh", src, dest, offset, text)


class Shu(StoreInstruction):
    """
    MIPS `shu` (store halfword unsigned) instruction.
    Store data in the ``src`` register with at address ``dest`` with an offset ``offset`` in memory.
    """

    def __init__(self, src: Reg, dest: Reg, offset: int = 0, text: str | Comment = "") -> None:
        super().__init__("shu", src, dest, offset, text)



class FpDataOp(Instruction):
    """
    Base class for floating point data operations.
    """

    op: str
    "Operation to perform"

    dest: Reg
    "Destination register to load into"

    src: Reg
    "Register containing source address to load from"

    def __init__(self, op: str, dest: Reg, src: Reg, text: str | Comment = "") -> None:
        super().__init__(text)
        self.op = op
        self.dest = dest
        self.src = src

    def __str__(self) -> str:
        return f"{self.op} {self.dest}, {self.src}{super().__str__()}"


class Cvt_s_w(FpDataOp):
    """
    MIPS `cvt.s.w` instruction.
    Convert from integer in :src: register into float in :dest: register.
    """

    def __init__(self, dest: Reg, src: Reg, text: str | Comment = "") -> None:
        super().__init__("cvt.s.w", dest, src, text)

class Cvt_d_s(FpDataOp):
    """
    MIPS `cvt.d.s` instruction.
    Convert from single precision (float) in :src: register into double precision (double) in :dest: register.
    """
    def __init__(self, dest: Regf, src: Regf, text: str | Comment = "") -> None:
        super().__init__("cvt.d.s", dest, src, text)

class Cvt_w_s(FpDataOp):
    """
    MIPS `cvt.w.s` instruction.
    Convert from float in :src: register into integer in :dest: register.
    """

    def __init__(self, dest: Reg, src: Reg, text: str | Comment = "") -> None:
        super().__init__("cvt.w.s", dest, src, text)


class Mov_s(FpDataOp):
    """
    MIPS `mov.s` instruction.
    Move float in :src: register into :dest: register.
    """

    def __init__(self, dest: Reg, src: Reg, text: str | Comment = "") -> None:
        super().__init__("mov.s", dest, src, text)


class L_s(Instruction):
    """
    MIPS `l.s` instruction.
    Load float at address in :src: register with offset :offset: into :dest: float register.
    """

    dest: Regf
    "Destination register to load into"

    src: Reg
    "Register containing source address to load from"

    offset: int
    "Offset from the source address"

    def __new__(self, dest: Regf, src: Reg, offset: int = 0, text: str | Comment = "") -> None:
        return (Lw(Reg.t0, src, offset, text), Mtc1(Reg.t0, dest))


class S_s(Instruction):
    """
    MIPS `s.s` instruction.
    Store float in the ``src`` register with at address ``dest`` with an offset ``offset`` in memory.
    """

    dest: Regf
    "Register to load from"

    src: Reg
    "Register containing destination address to load into"

    offset: int
    "Offset from the destination address"

    def __new__(self, src: Regf, dest: Reg, offset: int = 0, text: str | Comment = "") -> None:
        return (Mfc1(Reg.t0, src, text), Sw(Reg.t0, dest, offset))


class FpMInstruction(Instruction):
    """
    Base class for MIPS `mfc1` and `mtc1` instructions.
    """

    dir: str
    "Direction to move in, `f` or `t`"

    main_reg: Reg
    "Special register to load from, can be `hi` or `lo`"

    c1_reg: Regf
    "Destination register to move into"

    def __init__(self, dir: str, main_reg: Reg, c1_reg: Regf, text: str | Comment = "") -> None:
        super().__init__(text)
        self.dir = dir
        self.main_reg = main_reg
        self.c1_reg = c1_reg

    def __str__(self) -> str:
        return f"m{self.dir}c1 {self.main_reg}, {self.c1_reg}{super().__str__()}"


class Mtc1(FpMInstruction):
    """
    MIPS `mtc1` instruction.
    Move :main_reg: register contents into :c1_reg: register.
    """

    def __init__(self, main_reg: Reg, c1_reg: Regf, text: str | Comment = "") -> None:
        super().__init__("t", main_reg, c1_reg, text)


class Mfc1(FpMInstruction):
    """
    MIPS `mfc1` instruction.
    Move :c1_reg: register contents into :main_reg: register.
    """

    def __init__(self, main_reg: Reg, c1_reg: Regf, text: str | Comment = "") -> None:
        super().__init__("f", main_reg, c1_reg, text)
