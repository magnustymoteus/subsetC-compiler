from src.constructs.mips_program.node.instr.comp import (
    Slt,
    Slti,
    Sltu,
    Sle,
    Sne,
    Seq,
    Sgtu,
    Sge,
    Sgeu,
    Sleu,
    Sgt,
    C_eq_s,
    C_le_s,
    C_lt_s,
)
from src.constructs.mips_program.node.reg import Reg, Regf


def test_slt():
    instruction = Slt(Reg.t0, Reg.t1, Reg.t2)
    assert str(instruction) == "slt $t0, $t1, $t2"


def test_slti():
    instruction = Slti(Reg.t0, Reg.t1, Reg.t2)
    assert str(instruction) == "slti $t0, $t1, $t2"


def test_sltu():
    instruction = Sltu(Reg.t0, Reg.t1, Reg.t2)
    assert str(instruction) == "sltu $t0, $t1, $t2"


def test_sle():
    instructions = Sle(Reg.t1, Reg.t2, Reg.t3)
    assert len(instructions) == 3
    assert str(instructions[0]) == "slt $t1, $t3, $t2"
    assert str(instructions[1]) == "ori $t0, $zero, 1"
    assert str(instructions[2]) == "subu $t1, $t0, $t1"


def test_sle_imm():
    instructions = Sle(Reg.t1, Reg.t2, 5)
    assert len(instructions) == 4
    assert str(instructions[0]) == "addi $t0, $zero, 5"
    assert str(instructions[1]) == "slt $t1, $t0, $t2"
    assert str(instructions[2]) == "ori $t0, $zero, 1"
    assert str(instructions[3]) == "subu $t1, $t0, $t1"


def test_sne_reg():
    instructions = Sne(Reg.t1, Reg.t1, Reg.t2)
    assert len(instructions) == 2
    assert str(instructions[0]) == "subu $t1, $t1, $t2"
    assert str(instructions[1]) == "sltu $t1, $zero, $t1"


def test_sne_imm():
    instructions = Sne(Reg.t1, Reg.t2, 5)
    assert len(instructions) == 3
    assert str(instructions[0]) == "addi $t0, $zero, 5"
    assert str(instructions[1]) == "subu $t1, $t2, $t0"
    assert str(instructions[2]) == "sltu $t1, $zero, $t1"


def test_seq_reg():
    instruction = Seq(Reg.t1, Reg.t2, Reg.t3)
    assert str(instruction[0]) == "subu $t1, $t2, $t3"
    assert str(instruction[1]) == "ori $t0, $zero, 1"
    assert str(instruction[2]) == "sltu $t1, $t1, $t0"


def test_seq_imm():
    instruction = Seq(Reg.t1, Reg.t2, 5)
    assert str(instruction[0]) == "addi $t0, $zero, 5"
    assert str(instruction[1]) == "subu $t1, $t2, $t0"
    assert str(instruction[2]) == "ori $t0, $zero, 1"
    assert str(instruction[3]) == "sltu $t1, $t1, $t0"


def test_sge_reg():
    instructions = Sge(Reg.t1, Reg.t2, Reg.t3)
    assert len(instructions) == 3
    assert str(instructions[0]) == "slt $t1, $t2, $t3"
    assert str(instructions[1]) == "ori $t0, $zero, 1"
    assert str(instructions[2]) == "subu $t1, $t0, $t1"


def test_sge_imm():
    instructions = Sge(Reg.t1, Reg.t2, 5)
    assert len(instructions) == 4
    assert str(instructions[0]) == "addi $t0, $zero, 5"
    assert str(instructions[1]) == "slt $t1, $t2, $t0"
    assert str(instructions[2]) == "ori $t0, $zero, 1"
    assert str(instructions[3]) == "subu $t1, $t0, $t1"


def test_sgtu():
    instruction = Sgtu(Reg.t1, Reg.t2, Reg.t3)
    assert str(instruction) == "sltu $t1, $t3, $t2"


def test_sgeu_reg():
    instructions = Sgeu(Reg.t1, Reg.t2, Reg.t3)
    assert len(instructions) == 3
    assert str(instructions[0]) == "sltu $t1, $t2, $t3"
    assert str(instructions[1]) == "ori $t0, $zero, 1"
    assert str(instructions[2]) == "subu $t1, $t0, $t1"


def test_sgeu_imm():
    instructions = Sgeu(Reg.t1, Reg.t2, 5)
    assert len(instructions) == 4
    assert str(instructions[0]) == "addi $t0, $zero, 5"
    assert str(instructions[1]) == "sltu $t1, $t2, $t0"
    assert str(instructions[2]) == "ori $t0, $zero, 1"
    assert str(instructions[3]) == "subu $t1, $t0, $t1"


def test_sleu_reg():
    instructions = Sleu(Reg.t1, Reg.t2, Reg.t3)
    assert len(instructions) == 3
    assert str(instructions[0]) == "sltu $t1, $t3, $t2"
    assert str(instructions[1]) == "ori $t0, $zero, 1"
    assert str(instructions[2]) == "subu $t1, $t0, $t1"


def test_sleu_imm():
    instructions = Sleu(Reg.t1, Reg.t2, 5)
    assert len(instructions) == 4
    assert str(instructions[0]) == "addi $t0, $zero, 5"
    assert str(instructions[1]) == "sltu $t1, $t0, $t2"
    assert str(instructions[2]) == "ori $t0, $zero, 1"
    assert str(instructions[3]) == "subu $t1, $t0, $t1"


def test_sgt_reg():
    instruction = Sgt(Reg.t1, Reg.t2, Reg.t3)
    assert str(instruction) == "slt $t1, $t3, $t2"


def test_sgt_imm():
    instructions = Sgt(Reg.t1, Reg.t2, 5)
    assert len(instructions) == 2
    assert str(instructions[0]) == "addi $t0, $zero, 5"
    assert str(instructions[1]) == "slt $t1, $t0, $t2"


def test_c_eq_s():
    instruction = C_eq_s(Regf.f1, Regf.f2)
    assert str(instruction) == "c.eq.s $f1, $f2"


def test_c_le_s():
    instruction = C_le_s(Regf.f1, Regf.f2)
    assert str(instruction) == "c.le.s $f1, $f2"


def test_c_lt_s():
    instruction = C_lt_s(Regf.f1, Regf.f2)
    assert str(instruction) == "c.lt.s $f1, $f2"
