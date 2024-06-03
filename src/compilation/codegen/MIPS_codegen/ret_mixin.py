import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase, get_type_size
from src.constructs.mips_program.node.reg import Reg, Regf


class MVHandleRetMixin(MVBase):
    def handle_ret(self, instr: ir.Ret):
        assert 0 <= len(instr.operands) <= 1
        is_void = len(instr.operands) == 0
        # arg_size = get_args_size(self.function.args)
        args_with_offset = self.calc_arg_offsets(instr.function.args, self.stack_offset)
        tot_arg_size = (
            (self.stack_offset - args_with_offset[-1].offset + get_type_size(args_with_offset[-1].instr.type))
            if len(args_with_offset) > 0
            else 0
        )

        if not is_void:
            ret_val: ir.Instruction = instr.operands[0]
            ret_size = get_type_size(ret_val.type)
            tot_size = tot_arg_size + ret_size
            is_float = isinstance(ret_val.type, ir.FloatType)
            is_const: bool = isinstance(ret_val, ir.Constant)

        self.last_block.add_instr(
            mips_inst.Comment("clean up stack frame"),
            (
                (
                    (
                        (
                            # load value to be stored
                            self.load_value(ret_val, Regf.f0 if is_float else Reg.t1),
                            # store value at store address
                            self.store_value(ret_val, Regf.f0 if is_float else Reg.t1, tot_size),
                        )
                        if is_const
                        else self.copy_data(
                            Reg.fp, self.variables[ret_val.name].offset, Reg.fp, tot_size, ret_size,
                        )
                    ),
                )
                if not is_void
                else ()
            ),
            # restore return register
            mips_inst.Lw(Reg.ra, Reg.fp, -4, mips_inst.IrComment(f"{instr}")),  # lw  $ra, -4($fp)
            # restore stack pointer to start of frame
            mips_inst.Move(Reg.sp, Reg.fp),  # move    $sp, $fp
            # restore previous frame pointer
            mips_inst.Lw(Reg.fp, Reg.sp),  # lw  $fp, 0($sp)
            # reset stack by size of arguments  #? do with virtual stack checkpoint instead  #TODO
            mips_inst.Addiu(Reg.sp, Reg.sp, tot_arg_size),  # reset stack pointer to "deallocate" arguments
            # jump back to caller
            mips_inst.Jr(Reg.ra),  # jr  $ra
            mips_inst.Blank(),
        )
