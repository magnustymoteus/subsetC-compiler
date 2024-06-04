import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase, get_type_size
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg, Regf


class MVHandleCastMixin(MVBase):
    def handle_cast(self, instr: ir.CastInstr):
        assert len(instr.operands) == 1

        size = get_type_size(instr.type)
        var = self.variables.new_var(Label(instr.name), self.stack_offset)
        self.stack_offset -= size

        value = instr.operands[0]

        is_float = isinstance(value.type, ir.FloatType)
        "whether the result is a float"

        self.last_block.add_instr(
            mips_inst.IrComment(f"{instr}"),
        )

        match instr.opname:
            case "trunc":
                assert not is_float
                self.last_block.add_instr(
                    self.load_int(value, Reg.t1),
                    self.store_int(instr, Reg.t1, var.offset),
                )
            case "zext":
                assert not is_float
                self.last_block.add_instr(
                    self.load_int(value, Reg.t1),
                    self.store_int(instr, Reg.t1, var.offset),
                )
            case "sext":
                assert not is_float
                self.last_block.add_instr(
                    self.load_int(value, Reg.t1),
                    self.store_int(instr, Reg.t1, var.offset),
                )
            case "fptosi":
                assert is_float
                self.last_block.add_instr(
                    self.load_float(value, Regf.f0),
                    mips_inst.Cvt_w_s(Regf.f0, Regf.f0),
                    mips_inst.Mfc1(Reg.t1, Regf.f0),
                    self.store_int(value, Reg.t1, var.offset),
                )
            case "sitofp":
                assert not is_float
                self.last_block.add_instr(
                    self.load_int(value, Reg.t1),
                    mips_inst.Mtc1(Reg.t1, Regf.f0),
                    mips_inst.Cvt_s_w(Regf.f0, Regf.f0),
                    self.store_float(value, Regf.f0, var.offset),
                )
            case "fpext":
                assert is_float
                self.last_block.add_instr(
                    self.load_float(value, Regf.f0),
                    self.store_float(value, Regf.f0, var.offset)
                )
            case "ptrtoint":
                assert not is_float
                self.last_block.add_instr(
                    self.load_int(value, Reg.t1),
                    self.store_int(instr, Reg.t1, var.offset),
                )
            case "inttoptr":
                assert not is_float
                self.last_block.add_instr(
                    self.load_int(value, Reg.t1),
                    self.store_int(instr, Reg.t1, var.offset),
                )
            case "bitcast":
                print("unhandled: bitcast")
            case "addrspacecast":
                print("unhandled: addrspacecast")

            case "fptoui":
                print("no mips support: unhandled: fptoui")
                assert False
            case "uitofp":
                print("no mips support: unhandled: uitofp")
                assert False
            case "fptrunc":
                print("only float support: unhandled: fptrunc")
                assert False
            case _:
                raise ValueError(f"Unsupported cast operation: '{instr.opname}'")

        self.last_block.add_instr(mips_inst.Blank())
