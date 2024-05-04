from src.constructs.mips_program.node.instr import J, Jr, Jal, Jalr
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg


def test_j():
    instruction = J(Label("test"))
    assert str(instruction) == "j test"


def test_jr():
    instruction = Jr(Reg.t0)
    assert str(instruction) == "jr $t0"


def test_jal():
    instruction = Jal(Label("test"))
    assert str(instruction) == "jal test"


def test_jalr():
    instruction = Jalr(Reg.t0)
    assert str(instruction) == "jalr $t0"
