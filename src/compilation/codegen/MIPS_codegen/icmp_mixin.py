import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase, get_type_size
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg


class MVHandleICMPMixin(MVBase):
    def handle_icmp(self, instr: ir.ICMPInstr):
        """
        Performs integer comparison
        """

        assert len(instr.operands) == 2

        size: int = get_type_size(instr.type)  # TODO allow for arrays
        var = self.variables.new_var(Label(instr.name), self.stack_offset)
        self.stack_offset -= size

        self.last_block.add_instr(
            self.load_int(instr.operands[0], Reg.t1, mips_inst.IrComment(f"{instr}")),
            self.load_int(instr.operands[1], Reg.t2),
        )

        match instr.op:
            case "eq":
                self.last_block.add_instr(mips_inst.Seq(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp eq")))
            case "ne":
                self.last_block.add_instr(mips_inst.Sne(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp ne")))
            case "ugt":
                self.last_block.add_instr(mips_inst.Sgtu(Reg.t1, Reg.t2, Reg.t1, mips_inst.Comment("icmp ugt")))
            case "uge":
                self.last_block.add_instr(mips_inst.Sgeu(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp uge")))
            case "ult":
                self.last_block.add_instr(mips_inst.Sleu(Reg.t1, Reg.t2, Reg.t1, mips_inst.Comment("icmp ult")))
            case "ule":
                self.last_block.add_instr(mips_inst.Sltu(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp ule")))
            case "sgt":
                self.last_block.add_instr(mips_inst.Sgt(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp sgt")))
            case "sge":
                self.last_block.add_instr(mips_inst.Sge(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp sge")))
            case "slt":
                self.last_block.add_instr(mips_inst.Slt(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp slt")))
            case "sle":
                self.last_block.add_instr(mips_inst.Sle(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp sle")))
            case _:
                raise ValueError(f"Unsupported icmp operation: '{instr.op}'")

        self.last_block.add_instr(
            self.store_int(instr, Reg.t1, var.offset),
            # mips_inst.Sw(Reg.t1, Reg.fp, var.offset),
            mips_inst.Addiu(Reg.sp, Reg.sp, -size),
            mips_inst.Blank(),
        )
