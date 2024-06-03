import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase, get_type_size
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg, Regf


class MVHandleLoadMixin(MVBase):
    def handle_load(self, instr: ir.LoadInstr):
        assert len(instr.operands) == 1

        operand: ir.Instruction = instr.operands[0]

        assert operand.type.is_pointer, instr.type.is_pointer
        assert isinstance(operand, (ir.AllocaInstr, ir.GEPInstr, ir.LoadInstr, ir.GlobalVariable))

        # Allocate space for the new variable and store the loaded value
        size = get_type_size(instr.type)
        var = self.variables.new_var(Label(instr.name), self.stack_offset)
        self.stack_offset -= size

        # is_float = isinstance(operand.type, ir.FloatType)

        self.last_block.add_instr(
            mips_inst.Addiu(Reg.sp, Reg.sp, -size, mips_inst.IrComment(f"{instr}")),
            # load pointer address
            # assured operand is int because operand is pointer
            self.load_int(operand, Reg.t2, mips_inst.Comment("load pointer address")),

            # load value at pointer (deref)
            # store value at var offset from frame pointer
            self.copy_data( Reg.t2, 0, Reg.fp, var.offset, size),
            mips_inst.Blank(),
        )
