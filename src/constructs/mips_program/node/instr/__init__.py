from src.constructs.mips_program.node.instr.arith import Add, Addi, Addiu, Addu, Div, Divu, Mul, Mult, Sub, Subu
from src.constructs.mips_program.node.instr.comment import Comment, CComment, IrComment, Blank
from src.constructs.mips_program.node.instr.comp import Slt, Slti, Sltu, Sle, Sne
from src.constructs.mips_program.node.instr.cond import Beq, Bge, Bgt, Ble, Blt, Bne
from src.constructs.mips_program.node.instr.data import La, Li, Lui, Lw, Mfhi, Mflo, Move, Sw
from src.constructs.mips_program.node.instr.jump import J, Jr, Jal, Jalr
from src.constructs.mips_program.node.instr.instruction import Instruction
from src.constructs.mips_program.node.instr.logic import And, Andi, Or, Ori, Ssl, Srl
