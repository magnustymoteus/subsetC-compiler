import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase, get_type_size, PTR_SIZE
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg


class MVHandleAllocaMixin(MVBase):
    def handle_alloca(self, instr: ir.AllocaInstr):
        """
        :count: array size
        :size: size of array content, in bytes
        advance sp by :count: * :size:
        save stack offset of array start

        addiu $sp, $sp, -:count:*:size:
        # save variable offset from $fp
        """

        assert len(instr.operands) == 1

        # size of the allocated type
        size = get_type_size(instr.operands[0].type)
        tot_size = size + PTR_SIZE
        self.align_to(instr.align)
        # add variable to the list of variables of that function scope
        var = self.variables.new_var(Label(instr.name), self.stack_offset - size)
        self.stack_offset -= tot_size

        # add instruction to the block and create new space on the stack for the var
        self.last_block.add_instr(
            # move the stack pointer by the size of the variable
            mips_inst.Addiu(Reg.sp, Reg.sp, -(tot_size), mips_inst.IrComment(f"{instr}")), # addiu $sp, $sp, -size

            # calculate address of allocated variable
            mips_inst.Addiu(Reg.t1, Reg.fp, var.offset + size),

            # offset (already negative) minus type size
            self.store_int(instr, Reg.t1, var.offset),
            mips_inst.Blank(),
        )
