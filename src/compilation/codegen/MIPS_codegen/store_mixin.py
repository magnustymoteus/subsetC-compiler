import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase, get_align, get_type_size
from src.constructs.mips_program.node.reg import Reg, Regf

class MVHandleStoreMixin(MVBase):
    def handle_store(self, instr: ir.StoreInstr):
        assert len(instr.operands) == 2

        value: ir.Instruction = instr.operands[0]
        "value to be stored"
        value_t = value.type

        dest: ir.AllocaInstr = instr.operands[1]
        "instruction that contains the destination address"
        dest_t = dest.type

        assert dest_t.is_pointer
        assert isinstance(dest, (ir.AllocaInstr, ir.GEPInstr, ir.LoadInstr, ir.GlobalVariable))

        size: int = get_type_size(value_t)

        is_const = isinstance(value, ir.Constant)
        is_float = isinstance(value.type, ir.FloatType)

        self.last_block.add_instr(
            # load store address
            self.load_value(dest, Reg.t2),
            (
                (
                    # load value to be stored
                    self.load_value(value, Regf.f0 if is_float else Reg.t1, mips_inst.IrComment(f"{instr}")),
                    # store value at store address
                    self.store_value(value, Regf.f0 if is_float else Reg.t1, 0, mem_base=Reg.t2),
                )
                if is_const
                else self.copy_data(Reg.fp, self.variables[value.name].offset, Reg.t2, 0, size, get_align(dest))
            ),
            mips_inst.Blank(),
        )
