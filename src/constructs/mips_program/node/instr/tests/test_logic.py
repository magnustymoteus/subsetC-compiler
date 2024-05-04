from src.constructs.mips_program.node.instr import And, Andi, Or, Ori, Ssl, Srl
from src.constructs.mips_program.node.reg import Reg


def test_and():
    instruction = And(Reg.t0, Reg.t1, Reg.t2)
    assert str(instruction) == "and $t0, $t1, $t2"


def test_andi():
    instruction = Andi(Reg.t0, Reg.t1, 1)
    assert str(instruction) == "andi $t0, $t1, 1"


def test_or():
    instruction = Or(Reg.t0, Reg.t1, Reg.t2)
    assert str(instruction) == "or $t0, $t1, $t2"


def test_ori():
    instruction = Ori(Reg.t0, Reg.t1, 1)
    assert str(instruction) == "ori $t0, $t1, 1"


def test_ssl():
    instruction = Ssl(Reg.t0, Reg.t1, 1)
    assert str(instruction) == "ssl $t0, $t1, 1"


def test_srl():
    instruction = Srl(Reg.t0, Reg.t1, 1)
    assert str(instruction) == "srl $t0, $t1, 1"
