import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase, get_type_size
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg, Regf


class MVHandleLoadMixin(MVBase):
    def handle_load(self, instr: ir.LoadInstr):
        assert len(instr.operands) == 1
        operand = instr.operands[0]
        assert isinstance(operand, (ir.AllocaInstr, ir.GEPInstr, ir.LoadInstr))

        # Allocate space for the new variable and store the loaded value
        size = get_type_size(operand.operands[0].type)
        self.align_to(operand.align)
        var = self.variables.new_var(Label(instr.name), self.stack_offset)
        self.stack_offset -= size

        is_float = isinstance(operand.type, ir.FloatType)

        if isinstance(instr.type, ir.PointerType):
            # address of operand(=var) gets stored in $t1
            assert isinstance(
                instr.type.pointee, (ir.IntType, ir.FloatType, ir.PointerType)
            ), "only pointers and ints implemented"
            self.last_block.add_instr(
                # mips_inst.Lw(
                #     Reg.t1,
                #     Reg.fp,
                #     self.variables[operand.name].offset,
                #     mips_inst.Comment(f"Load {operand.name}  (LoadInstr)"),
                # ),
                self.load_int(operand, Reg.t1, mips_inst.Comment(f"Load {operand.name}  (LoadInstr)")),
                # Dereference the address to get the value
                mips_inst.Lw(Reg.t1, Reg.t1, 0, mips_inst.Comment(f"Dereference {operand.name}")),
                # TODO support more than only integer/pointer types
            )

        else:
            # Load the value directly if not a pointer
            self.last_block.add_instr(
                mips_inst.Lw(
                    Reg.t1,
                    Reg.fp,
                    self.variables[operand.name].offset,
                    mips_inst.Comment(f"Load value of %{operand.name}"),
                ),
            )
            self.load_value(
                operand, Regf.f0 if is_float else Reg.t1, mips_inst.Comment(f"Load {operand.name}  (LoadInstr)")
            ),

        self.last_block.add_instr(
            mips_inst.Addiu(Reg.sp, Reg.sp, -size, mips_inst.IrComment(f"{instr}")),
            mips_inst.Sw(Reg.t1, Reg.fp, var.offset),  # Store value in new variable
            mips_inst.Blank(),
        )
