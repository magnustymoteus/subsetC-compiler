import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase, get_type_size
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg


class MVHandleGEPMixin(MVBase):
    def handle_gep(self, instr: ir.GEPInstr):
        # %"2" = getelementptr inbounds i32, i32* %"0", i64 %"1"
        # moves the pointer %"0" forward by one element of type i32 and stores the result in %"2".

        assert len(instr.operands) == 2 and isinstance(instr.operands[1], ir.CastInstr)

        base_ptr = instr.operands[0]
        offset = get_type_size(base_ptr.type)

        # Store the new pointer address in the variables list
        self.variables.new_var(Label(instr.name), self.stack_offset)
        self.stack_offset -= offset

        self.last_block.add_instr(mips_inst.IrComment(f"{instr}"))
        self.last_block.add_instr(
            # Load the adress of the base pointer into $t1
            mips_inst.Lw(
                Reg.t1,
                Reg.fp,
                # IR: %"2" = getelementptr inbounds i32, i32* %"0", i64 %"1"
                # this gets the pointer that %0 points to
                self.variables[instr.operands[0].operands[0].name].offset,
                mips_inst.Comment(f"Load value of %{instr.operands[0].operands[0].name}"),
            ),
            # Load the base pointer into $t2
            mips_inst.Li(Reg.t2, offset, mips_inst.Comment("Load offset")),
            # Sub the offset from the address of the base pointer
            (
                # pointer++
                mips_inst.Sub(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("Sub offset from base pointer"))
                if isinstance(instr.operands[1].operands[0], ir.Constant)
                # pointer--
                else mips_inst.Add(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("Add offset to base pointer"))
            ),
            # Store result on the stack on the variables offset
            mips_inst.Sw(
                Reg.t1,
                Reg.fp,
                self.variables[instr.name].offset,
                mips_inst.Comment("Store new ptr address on the stack"),
            ),
        )
        self.last_block.add_instr(mips_inst.Blank()),

        # print("unhandled! for arrays")
