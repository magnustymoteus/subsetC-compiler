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
        assert instr.type.is_pointer

        num_elements: ir.Instruction = instr.operands[0]
        pointee_type = instr.type.pointee

        # size of the allocated type
        size = get_type_size(pointee_type)

        self.stack_offset -= size
        self.last_block.add_instr(
            # move the stack pointer by the size of the variable
            mips_inst.Addiu(Reg.sp, Reg.sp, -(size), mips_inst.IrComment(f"{instr}")),  # addiu $sp, $sp, -size
        )

        # add variable to the list of variables of that function scope
        var = self.variables.new_var(Label(instr.name), self.stack_offset)
        self.stack_offset -= PTR_SIZE
        self.last_block.add_instr(
            mips_inst.Addiu(Reg.sp, Reg.sp, -PTR_SIZE),
            # calculate address of allocated variable
            mips_inst.Addiu(Reg.t1, Reg.fp, var.offset + size),
            # offset (already negative) minus type size
            self.store_int(instr, Reg.t1, var.offset),
            mips_inst.Blank(),
        )
