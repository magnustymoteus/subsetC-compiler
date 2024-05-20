from src.constructs.mips_program.node.instr.arith import Add, Addi, Addiu, Addu, Div, Divu, Mul, Mult, Sub, Subu, Add_s, Sub_s, Mul_s, Div_s, Abs_s, Neg_s
from src.constructs.mips_program.node.reg import Reg, Regf


def test_add() -> None:
    assert str(Add(Reg.t0, Reg.t1, Reg.t2)) == "add $t0, $t1, $t2"


def test_addi() -> None:
    assert str(Addi(Reg.t0, Reg.t1, 42)) == "addi $t0, $t1, 42"


def test_addiu() -> None:
    assert str(Addiu(Reg.t0, Reg.t1, 42)) == "addiu $t0, $t1, 42"


def test_addu() -> None:
    assert str(Addu(Reg.t0, Reg.t1, Reg.t2)) == "addu $t0, $t1, $t2"


def test_div() -> None:
    assert str(Div(Reg.t0, Reg.t1)) == "div $t0, $t1"


def test_divu() -> None:
    assert str(Divu(Reg.t0, Reg.t1)) == "divu $t0, $t1"


def test_mul() -> None:
    assert str(Mul(Reg.t0, Reg.t1, Reg.t2)) == "mul $t0, $t1, $t2"


def test_mult() -> None:
    assert str(Mult(Reg.t0, Reg.t1, Reg.t2)) == "mult $t0, $t1, $t2"


def test_sub() -> None:
    assert str(Sub(Reg.t0, Reg.t1, Reg.t2)) == "sub $t0, $t1, $t2"


def test_subu() -> None:
    assert str(Subu(Reg.t0, Reg.t1, Reg.t2)) == "subu $t0, $t1, $t2"

def test_add_s() -> None:
    assert str(Add_s(Regf.f0, Regf.f1, Regf.f2)) == "add.s $f0, $f1, $f2"

def test_sub_s() -> None:
    assert str(Sub_s(Regf.f0, Regf.f1, Regf.f2)) == "sub.s $f0, $f1, $f2"

def test_mul_s() -> None:
    assert str(Mul_s(Regf.f0, Regf.f1, Regf.f2)) == "mul.s $f0, $f1, $f2"

def test_div_s() -> None:
    assert str(Div_s(Regf.f0, Regf.f1, Regf.f2)) == "div.s $f0, $f1, $f2"

def test_abs_s() -> None:
    assert str(Abs_s(Regf.f0, Regf.f1)) == "abs.s $f0, $f1"

def test_neg_s() -> None:
    assert str(Neg_s(Regf.f0, Regf.f1)) == "neg.s $f0, $f1"