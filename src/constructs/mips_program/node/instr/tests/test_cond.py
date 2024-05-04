from src.constructs.mips_program.node.instr import Beq, Bge, Bgt, Ble, Blt, Bne
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg


def test_beq():
    instruction = Beq(Reg.t0, Reg.t1, Label("test"))
    assert str(instruction) == "beq $t0, $t1, test"


def test_bge():
    instruction = Bge(Reg.t0, Reg.t1, Label("test"))
    assert str(instruction) == "bge $t0, $t1, test"


def test_bgt():
    instruction = Bgt(Reg.t0, Reg.t1, Label("test"))
    assert str(instruction) == "bgt $t0, $t1, test"


def test_ble():
    instruction = Ble(Reg.t0, Reg.t1, Label("test"))
    assert str(instruction) == "ble $t0, $t1, test"


def test_blt():
    instruction = Blt(Reg.t0, Reg.t1, Label("test"))
    assert str(instruction) == "blt $t0, $t1, test"


def test_bne():
    instruction = Bne(Reg.t0, Reg.t1, Label("test"))
    assert str(instruction) == "bne $t0, $t1, test"
