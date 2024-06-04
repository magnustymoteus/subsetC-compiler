import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase, get_type_size
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg, Regf


class MVHandleCallMixin(MVBase):

    def handle_call(self, instr: ir.CallInstr):
        """
        function call stack layout:
        +-----------------+  ┓ responsibility of caller
        | stack of caller |  ┃
        +-----------------+  ┃
        | function return |  ┃
        +-----------------+  ┃
        | function arg1   |  ┃
        +-----------------+  ┃
        | function arg2   |  ┃
        +-----------------+  ┃
        | function arg... |  ┛
        +-----------------+  ┓ responsibility of callee
        | old $fp         |  ┃ <= where $fp points to while in callee
        +-----------------+  ┃
        | new $ra         |  ┃ <= where to return back to
        +-----------------+  ┃
        | stack of callee |  ┃
        +-----------------+  ┛
        """
        func: ir.Function = instr.operands[0]
        func_args: list = instr.args
        jal_block = ""
        ret_size = get_type_size(func.return_value.type)

        if instr.called_function.name in ["printf", "scanf"]:
            jal_block = Label(instr.called_function.name)
            func_args.append(ir.Constant(ir.IntType(32), len(func_args)))
            ret_size = 0
        else:
            jal_block = Label(f"{func.name}.{func.basic_blocks[0].name}")

        var = self.variables.new_var(Label(instr.name), self.stack_offset)
        # only increase stack offset by return size to overwrite arguments after call ends
        # in mips the stack pointer is increased by total size and reset before return jump
        self.stack_offset -= ret_size

        args_with_offset = self.calc_arg_offsets(func_args, -ret_size)
        tot_arg_size = (
            (-ret_size - args_with_offset[-1].offset + get_type_size(args_with_offset[-1].instr.type))
            if len(args_with_offset) > 0
            else 0
        )

        tot_size = ret_size + tot_arg_size

        self.last_block.add_instr(
            # allocate stack space for function and return arguments
            mips_inst.Addiu(Reg.sp, Reg.sp, -tot_size, mips_inst.IrComment(f"{instr}")),
            [
                (
                    (
                        # load value to be stored
                        self.load_value(
                            arg, Regf.f0 if isinstance(arg.type, (ir.FloatType, ir.DoubleType)) else Reg.t1
                        ),
                        # store value at store address
                        self.store_value(
                            arg, Regf.f0 if isinstance(arg.type, (ir.FloatType, ir.DoubleType)) else Reg.t1, arg_offset
                        ),
                    )
                    if isinstance(arg, ir.Constant)
                    else self.copy_data(Reg.fp, self.variables[arg.name].offset, Reg.s7, arg_offset, arg_size)
                )
                for arg, arg_offset, arg_size in args_with_offset
            ],
            mips_inst.Jal(jal_block),
            self.copy_data(Reg.s7, 0, Reg.fp, var.offset, ret_size),
            # restore stack pointer
            # mips_inst.Addiu(Reg.sp, Reg.sp, tot_size),
            mips_inst.Move(Reg.sp, Reg.s7),
            mips_inst.Blank(),
        )
