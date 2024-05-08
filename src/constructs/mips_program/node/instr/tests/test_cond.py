from src.constructs.mips_program.node.instr import Beq, Bge, Bgt, Ble, Blt, Bne
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg


def test_beq():
    instruction = Beq(Reg.t0, Reg.t1, Label("test"))
    assert str(instruction) == "beq $t0, $t1, test"


def test_bge_reg():
    instructions = Bge(Reg.t0, Reg.t1, Label("test"))
    assert str(instructions[0]) == "slt $at, $t0, $t1"
    assert str(instructions[1]) == "beq $at, $zero, test"

def test_bge_imm():
    instructions = Bge(Reg.t0, 4, Label("test"))
    assert str(instructions[0]) == "slti $at, $t0, 4"
    assert str(instructions[1]) == "beq $at, $zero, test"


def test_bgt_reg():
    instruction = Bgt(Reg.t0, Reg.t1, Label("test"))
    assert str(instruction[0]) == "slt $at, $t0, $t1"
    assert str(instruction[1]) == "bne $at, $zero, test"

def test_bgt_imm():
    instructions = Bgt(Reg.t0, 4, Label("test"))
    assert str(instructions[0]) == "addi $at, $zero, 4"
    assert str(instructions[1]) == "slt $at, $at, $t0"
    assert str(instructions[2]) == "bne $at, $zero, test"


def test_ble_reg():
    instructions = Ble(Reg.t0, Reg.t1, Label("test"))
    assert str(instructions[0]) == "slt $at, $t1, $t0"
    assert str(instructions[1]) == "beq $at, $zero, test"

def test_ble_imm():
    instructions = Ble(Reg.t0, 4, Label("test"))
    assert str(instructions[0]) == "addi $at, $t0, -1"
    assert str(instructions[1]) == "slti $at, $at, 4"
    assert str(instructions[2]) == "bne $at, $zero, test"


def test_blt_reg():
    instructions = Blt(Reg.t0, Reg.t1, Label("test"))
    assert str(instructions[0]) == "slt $at, $t0, $t1"
    assert str(instructions[1]) == "bne $at, $zero, test"

def test_blt_imm():
    instructions = Blt(Reg.t0, 4, Label("test"))
    assert str(instructions[0]) == "slti $at, $t0, 4"
    assert str(instructions[1]) == "bne $at, $zero, test"


def test_bne():
    instruction = Bne(Reg.t0, Reg.t1, Label("test"))
    assert str(instruction) == "bne $t0, $t1, test"
