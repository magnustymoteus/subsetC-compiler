from src.constructs.mips_program.node.instr import Slt, Slti
from src.constructs.mips_program.node.reg import Reg


def test_slt():
    instruction = Slt(Reg.t0, Reg.t1, Reg.t2)
    assert str(instruction) == "slt $t0, $t1, $t2"


def test_slti():
    instruction = Slti(Reg.t0, Reg.t1, Reg.t2)
    assert str(instruction) == "slti $t0, $t1, $t2"
