from src.constructs.mips_program.node import LabeledBlock
from src.constructs.mips_program.variable import Global

entry: str = """
.text
main:
    move $fp, $sp       # set frame pointer
    addiu $sp, $sp, -4  # allocate space for return value
    jal main.entry      # call main function
    lw $a0, 0($fp)      # load return value from main function
    li $v0, 1           # set syscall code to 1 (print int)
    syscall             # print return value
    li $v0, 10          # set syscall code to 10 (exit)
    syscall             # exit
"""

class MipsProgram:

    def __init__(self) -> None:
        self.blocks: list[LabeledBlock] = []
        self.data: list[Global] = []

    def add_block(self, block: LabeledBlock):
        self.blocks.append(block)

    def to_asm(self) -> str:
        globl = ".globl main"
        data = "\n".join([f"{d}" for d in self.data])
        # convert all blocks in the program to asm and join them with a newline
        blocks = "\n".join([f"{b}" for b in self.blocks])
        return f"{globl}\n.data\n{data}\n{entry}\n{blocks}"
