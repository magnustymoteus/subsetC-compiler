from src.constructs.mips_program.node.instr import Slt, Slti, Sltu, Sle, Sne, Seq
from src.constructs.mips_program.node.reg import Reg


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
