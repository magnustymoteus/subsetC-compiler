"""
All jump MIPS instructions.
"""

from src.constructs.mips_program.node.instr.instruction import Instruction
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg


class J(Instruction):
    """
    MIPS `j` (jump) instruction.
    Jump to the address in :label: label.
    """

    label: Label
    "Label to jump to"

    def __init__(self, label: Label) -> None:
        super().__init__()
        self.label = label

    def __str__(self) -> str:
        return f"j {self.label.label}"


class Jr(Instruction):
    """
    MIPS `jr` (jump register) instruction.
    Jump to the address in :dest: register.
    """

    dest: Reg
    "Register containing destination address to jump to"

    def __init__(self, dest: Reg) -> None:
        super().__init__()
        self.dest = dest

    def __str__(self) -> str:
        return f"jr {self.dest}"


class Jal(Instruction):
    """
    MIPS `jal` (jump and link) instruction.
    Jump to the address in the :dest: register and store the current program counter in `$ra` register.
    """

    label: Label
    "Register containing destination address to jump to"

    def __init__(self, label: Label) -> None:
        super().__init__()
        self.label = label

    def __str__(self) -> str:
        return f"jal {self.label.label}"


class Jalr(Instruction):
    """
    MIPS `jalr` (jump and link register) instruction.
    Jump to the address in the :dest: register and store the current program counter in `$ra` register.
    """

    dest: Reg
    "Register containing destination address to jump to"

    def __init__(self, dest: Reg) -> None:
        super().__init__()
        self.dest = dest

    def __str__(self) -> str:
        return f"jalr {self.dest}"
