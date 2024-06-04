from src.constructs.mips_program.node.instr.data import La, Li, Lui, Lw, Lb, Lbu, Lh, Lhu, Mfhi, Mflo, Move, Sw, Sb, Sbu, Sh, Shu, Cvt_s_w, Cvt_w_s, Mov_s, L_s, S_s, Mtc1, Mfc1
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg, Regf


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


def test_lb():
    instruction = Lb(Reg.t0, Reg.s0, 1)
    assert str(instruction) == "lb $t0, 1($s0)"


def test_lbu():
    instruction = Lbu(Reg.t0, Reg.s0, 1)
    assert str(instruction) == "lbu $t0, 1($s0)"


def test_lh():
    instruction = Lh(Reg.t0, Reg.s0, 1)
    assert str(instruction) == "lh $t0, 1($s0)"


def test_lhu():
    instruction = Lhu(Reg.t0, Reg.s0, 1)
    assert str(instruction) == "lhu $t0, 1($s0)"


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

def test_sb():
    instruction = Sb(Reg.t0, Reg.s0, 1)
    assert str(instruction) == "sb $t0, 1($s0)"


def test_sbu():
    instruction = Sbu(Reg.t0, Reg.s0, 1)
    assert str(instruction) == "sbu $t0, 1($s0)"


def test_sh():
    instruction = Sh(Reg.t0, Reg.s0, 1)
    assert str(instruction) == "sh $t0, 1($s0)"


def test_shu():
    instruction = Shu(Reg.t0, Reg.s0, 1)
    assert str(instruction) == "shu $t0, 1($s0)"

def test_cvt_s_w():
    instruction = Cvt_s_w(Regf.f0, Regf.f1)
    assert str(instruction) == "cvt.s.w $f0, $f1"

def test_cvt_w_s():
    instruction = Cvt_w_s(Regf.f0, Regf.f1)
    assert str(instruction) == "cvt.w.s $f0, $f1"

def test_mov_s():
    instruction = Mov_s(Regf.f0, Regf.f1)
    assert str(instruction) == "mov.s $f0, $f1"

def test_l_s():
    instruction = L_s(Regf.f0, Reg.t1, 1)
    assert len(instruction) == 2
    assert str(instruction[0]) == "lw $t0, 1($t1)"
    assert str(instruction[1]) == "mtc1 $t0, $f0"

def test_s_s():
    instruction = S_s(Regf.f0, Reg.t1, 1)
    assert len(instruction) == 2
    assert str(instruction[0]) == "mfc1 $t0, $f0"
    assert str(instruction[1]) == "sw $t0, 1($t1)"

def test_mtc1():
    instruction = Mtc1(Regf.f0, Regf.f1)
    assert str(instruction) == "mtc1 $f0, $f1"

def test_mfc1():
    instruction = Mfc1(Regf.f0, Regf.f1)
    assert str(instruction) == "mfc1 $f0, $f1"