import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase, get_type_size
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg, Regf


class MVHandleInstructionMixin(MVBase):
    def handle_instruction(self, instr: ir.Instruction):
        assert 0 < len(instr.operands) <= 2

        size = get_type_size(instr.type)
        self.align_to(size)
        var = self.variables.new_var(Label(instr.name), self.stack_offset)
        self.stack_offset -= size

        is_float = isinstance(instr.type, ir.FloatType)

        self.last_block.add_instr(
            mips_inst.Addiu(Reg.sp, Reg.sp, -size, mips_inst.IrComment(f"{instr}")),  # addiu $sp, $sp, -size
            self.load_value(instr.operands[0], Regf.f0 if is_float else Reg.t1),
            (self.load_value(instr.operands[1], Regf.f2 if is_float else Reg.t2) if len(instr.operands) == 2 else ()),
        )

        match instr.opname:
            case "add":
                self.last_block.add_instr(mips_inst.Addu(Reg.t1, Reg.t1, Reg.t2))
            case "sub":
                self.last_block.add_instr(mips_inst.Subu(Reg.t1, Reg.t1, Reg.t2))
            case "mul":
                self.last_block.add_instr(mips_inst.Mul(Reg.t1, Reg.t1, Reg.t2))
            case "sdiv":
                self.last_block.add_instr(
                    mips_inst.Div(Reg.t1, Reg.t2),
                    mips_inst.Mflo(Reg.t1),
                )
            case "udiv":
                self.last_block.add_instr(
                    mips_inst.Divu(Reg.t1, Reg.t2),
                    mips_inst.Mflo(Reg.t1),
                )
            case "srem":
                self.last_block.add_instr(
                    mips_inst.Div(Reg.t1, Reg.t2),
                    mips_inst.Mfhi(Reg.t1),
                )
            case "urem":
                self.last_block.add_instr(
                    mips_inst.Divu(Reg.t1, Reg.t2),
                    mips_inst.Mfhi(Reg.t1),
                )
            case "and":
                self.last_block.add_instr(mips_inst.And(Reg.t1, Reg.t1, Reg.t2), mips_inst.Comment("and"))
            case "or":
                self.last_block.add_instr(mips_inst.Or(Reg.t1, Reg.t1, Reg.t2), mips_inst.Comment("or"))
            case "xor":
                self.last_block.add_instr(mips_inst.Xor(Reg.t1, Reg.t1, Reg.t2), mips_inst.Comment("xor"))
            case "shl":
                self.last_block.add_instr(
                    mips_inst.Sll(Reg.t1, Reg.t1, instr.operands[1].constant, mips_inst.Comment("Shl")),
                )
            case "ashr":
                self.last_block.add_instr(
                    mips_inst.Srl(Reg.t1, Reg.t1, instr.operands[1].constant, mips_inst.Comment("Slr")),
                )
            case "fadd":
                self.last_block.add_instr(mips_inst.Add_s(Regf.f0, Regf.f0, Regf.f2))
            case "fsub":
                self.last_block.add_instr(mips_inst.Sub_s(Regf.f0, Regf.f0, Regf.f2, "fsub"))
            case "fmul":
                self.last_block.add_instr(mips_inst.Mul_s(Regf.f0, Regf.f0, Regf.f2))
            case "fdiv":
                self.last_block.add_instr(mips_inst.Div_s(Regf.f0, Regf.f0, Regf.f2))
            case "fneg" if is_float:
                self.last_block.add_instr(mips_inst.Neg_s(Regf.f0, Regf.f0))
            case _:
                print(f"Unhandled instruction: '{instr.opname}'")

        self.last_block.add_instr(
            self.store_value(instr, Regf.f0 if is_float else Reg.t1, var.offset),
            mips_inst.Blank(),
        )
