from src.constructs.mips_program.node.instr import Add, Addi, Addiu, Addu, Div, Divu, Mul, Mult, Sub, Subu
from src.constructs.mips_program.node.reg import Reg


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
