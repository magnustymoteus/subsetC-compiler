import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase
from src.constructs.mips_program.node.reg import Reg, Regf


class MVHandleStoreMixin(MVBase):
    def handle_store(self, instr: ir.StoreInstr):
        assert len(instr.operands) == 2

        value: ir.Instruction = instr.operands[0]
        "value to be stored"
        value_t = value.type

        gen: ir.AllocaInstr = instr.operands[1]
        "instruction that allocated the value space (expect alloca or gep)"
        gen_t = gen.type

        assert gen_t.is_pointer
        assert isinstance(gen, (ir.AllocaInstr, ir.GEPInstr, ir.LoadInstr, ir.GlobalVariable))

        is_float = isinstance(value.type, ir.FloatType)

        self.last_block.add_instr(
            # load value to be stored
            self.load_value(value, Regf.f0 if is_float else Reg.t1, mips_inst.IrComment(f"{instr}")),
            # load store address
            self.load_value(gen, Reg.t2),
            # store value at store address
            self.store_value(value, Regf.f0 if is_float else Reg.t1, 0, mem_base=Reg.t2),
            mips_inst.Blank(),
        )
