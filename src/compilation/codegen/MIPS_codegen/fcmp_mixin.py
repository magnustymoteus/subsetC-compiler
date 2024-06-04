import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase, get_type_size
from src.constructs.mips_program.node.block import LabeledBlock
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg, Regf


class MVHandleFCMPMixin(MVBase):
    def handle_fcmp(self, instr: ir.FCMPInstr):
        assert len(instr.operands) == 2

        value1: ir.Instruction = instr.operands[0]
        value2: ir.Instruction = instr.operands[1]

        size = get_type_size(instr.type)
        var = self.variables.new_var(Label(instr.name), self.stack_offset)
        self.stack_offset -= size

        branch_true_label = Label(f"{self.function.name}.{self.basic_block.name}.{instr.name}.true")
        branch_false_label = Label(f"{self.function.name}.{self.basic_block.name}.{instr.name}.false")
        branch_end_label = Label(f"{self.function.name}.{self.basic_block.name}.{instr.name}.end")

        self.last_block.add_instr(
            mips_inst.IrComment(f"{instr}"),
            self.load_float(value1, Regf.f0),
            self.load_float(value2, Regf.f2),
        )

        match instr.op:
            case "false":
                self.last_block.add_instr(mips_inst.J(branch_false_label))
            case "ueq":
                self.last_block.add_instr(
                    mips_inst.C_eq_s(Regf.f0, Regf.f2),
                    mips_inst.Bc1t(branch_true_label),
                    mips_inst.Bc1f(branch_false_label),
                )
            case "ugt":
                self.last_block.add_instr(
                    mips_inst.C_le_s(Regf.f0, Regf.f2),
                    mips_inst.Bc1t(branch_false_label),
                    mips_inst.Bc1f(branch_true_label),
                )
            case "uge":
                self.last_block.add_instr(
                    mips_inst.C_lt_s(Regf.f0, Regf.f2),
                    mips_inst.Bc1t(branch_false_label),
                    mips_inst.Bc1f(branch_true_label),
                )
            case "ult":
                self.last_block.add_instr(
                    mips_inst.C_lt_s(Regf.f0, Regf.f2),
                    mips_inst.Bc1t(branch_true_label),
                    mips_inst.Bc1f(branch_false_label),
                )
            case "ule":
                self.last_block.add_instr(
                    mips_inst.C_le_s(Regf.f0, Regf.f2),
                    mips_inst.Bc1t(branch_true_label),
                    mips_inst.Bc1f(branch_false_label),
                )
            case "une":
                self.last_block.add_instr(
                    mips_inst.C_eq_s(Regf.f0, Regf.f2),
                    mips_inst.Bc1t(branch_false_label),
                    mips_inst.Bc1f(branch_true_label),
                )
            case "true":
                self.last_block.add_instr(mips_inst.J(branch_true_label))
            case "oeq" | "ogt" | "oge" | "olt" | "ole" | "one" | "ord" | "uno":
                print("unhandled: ", instr.op)
                assert False
            case _:
                assert False

        self.tree.add_block(LabeledBlock(branch_true_label))
        self.last_block.add_instr(
            mips_inst.Li(Reg.t1, 1, mips_inst.Comment(f"branch if true")),
            mips_inst.J(branch_end_label),
        )
        self.tree.add_block(LabeledBlock(branch_false_label))
        self.last_block.add_instr(
            mips_inst.Li(Reg.t1, 0, mips_inst.Comment(f"branch if false")),
            mips_inst.J(branch_end_label),
        )
        self.tree.add_block(LabeledBlock(branch_end_label))
        self.last_block.add_instr(self.store_value(instr, Reg.t1, var.offset))
