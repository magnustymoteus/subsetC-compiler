from src.constructs.mips_program.node.instr import La, Li, Lui, Lw, Mfhi, Mflo, Move, Sw
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg


def test_la():
    instruction = La(Reg.t0, Label("test"))
    assert str(instruction) == "la $t0, test"


def test_li():
    instruction = Li(Reg.t0, 1)
    assert str(instruction) == "li $t0, 1"


def test_lui():
    instruction = Lui(Reg.t0, 1)
    assert str(instruction) == "lui $t0, 1"


def test_lw():
    instruction = Lw(Reg.t0, Reg.s0, 1)
    assert str(instruction) == "lw $t0, 1($s0)"


def test_mfhi():
    instruction = Mfhi(Reg.t0)
    assert str(instruction) == "mfhi $t0"


def test_mflo():
    instruction = Mflo(Reg.t0)
    assert str(instruction) == "mflo $t0"


def test_move():
    instruction = Move(Reg.t0, Reg.t1)
    assert str(instruction) == "move $t0, $t1"


def test_sw():
    instruction = Sw(Reg.t0, Reg.s0, 1)
    assert str(instruction) == "sw $t0, 1($s0)"
