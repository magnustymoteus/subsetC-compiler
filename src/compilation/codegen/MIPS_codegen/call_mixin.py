import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase, get_args_size, get_type_size
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg, Regf


class MVHandleCallMixin(MVBase):
    def handle_call(self, instr: ir.CallInstr):
        """
        function call stack layout:
        +-----------------+  ┓
        | stack of caller |  ┃
        +-----------------+  ┃
        | function return |  ┃ responsibility of caller
        +-----------------+  ┃
        | function args   |  ┛
        +-----------------+  ┓
        | old $fp         |  ┃
        +-----------------+  ┃
        | new $ra         |  ┃ responsibility of callee
        +-----------------+  ┃
        | stack of callee |  ┃
        +-----------------+  ┛
        """
        func: ir.Function = instr.operands[0]
        ret_size = get_type_size(func.return_value.type)
        arg_size = get_args_size(func.args)
        tot_size = ret_size + arg_size
        self.align_to(ret_size)
        var = self.variables.new_var(Label(instr.name), self.stack_offset)
        # only increase stack offset by return size to overwrite arguments after call ends
        # in mips the stack pointer is increased by total size and reset before return jump
        self.stack_offset -= ret_size

        self.last_block.add_instr(
            # allocate stack space for function and return arguments
            mips_inst.Addiu(
                Reg.sp, Reg.sp, -tot_size, mips_inst.IrComment(f"{instr}")
            ),  # addiu $sp, $sp, -(ret_size + arg_size)
            [
                (
                    # load argument value into t1 or f0
                    self.load_value(
                        oper,
                        Regf.f0 if isinstance(oper.type, ir.FloatType) else Reg.t1,
                        mips_inst.Comment(f"load arg {i}"),
                    ),
                    # store argument value on stack. stored at return offset (negative) - return size - argument size up to stored argument
                    self.store_value(
                        oper,
                        Regf.f0 if isinstance(oper.type, ir.FloatType) else Reg.t1,
                        var.offset - ret_size - get_args_size(func.args[:i]),
                        mips_inst.Comment(f"store arg {i}"),
                    ),
                )
                for i, oper in enumerate(instr.operands[1:])
            ],
            mips_inst.Jal(Label(f"{func.name}.{func.basic_blocks[0].name}")),
            mips_inst.Blank(),
        )
