import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase, get_args_size, get_type_size
from src.constructs.mips_program.node.reg import Reg, Regf


class MVHandleRetMixin(MVBase):
    def handle_ret(self, instr: ir.Ret):
        assert len(instr.operands) == 1  # ? likely wrong for structs
        ret_val: ir.Instruction = instr.operands[0]
        ret_size = get_type_size(ret_val.type)  # TODO unused
        arg_size = get_args_size(self.function.args)
        tot_size = arg_size + ret_size

        is_float = isinstance(ret_val.type, ir.FloatType)

        self.last_block.add_instr(
            mips_inst.Comment("clean up stack frame"),
            # load return value and store it at return address on the stack
            self.load_value(ret_val, Regf.f0 if is_float else Reg.t1, mips_inst.IrComment(f"{instr}")),
            # mips_inst.Sw(Reg.t1, Reg.fp, tot_size),  # sw $t1, $fp, 4
            self.store_value(ret_val, Regf.f0 if is_float else Reg.t1, tot_size),
            # self.copy_data(Reg.fp, self.variables[ret_val.name].offset, Reg.fp, tot_size, ret_size),
            # restore return register
            mips_inst.Lw(Reg.ra, Reg.fp, -4),  # lw  $ra, -4($fp)
            # restore stack pointer to start of frame
            mips_inst.Move(Reg.sp, Reg.fp),  # move    $sp, $fp
            # restore previous frame pointer
            mips_inst.Lw(Reg.fp, Reg.sp),  # lw  $fp, 0($sp)
            # reset stack by size of arguments
            mips_inst.Addiu(Reg.sp, Reg.sp, arg_size),  # reset stack pointer to "deallocate" arguments
            # jump back to caller
            mips_inst.Jr(Reg.ra),  # jr  $ra
            mips_inst.Blank(),
        )
