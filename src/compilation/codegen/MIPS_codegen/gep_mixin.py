import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase, get_type_size
from src.constructs.mips_program.node.label import Label
from src.constructs.mips_program.node.reg import Reg


def contained_type(t: ir.Type) -> ir.Type:
    match t:
        case ir.PointerType():
            return t.pointee
        case ir.ArrayType():
            return t.element
        case ir.LiteralStructType():
            assert False, f"unimplemented: {type(t.type).__name__}"
        case ir.IdentifiedStructType():
            assert False, f"unimplemented: {type(t.type).__name__}"
        case ir.BaseStructType():
            assert False, f"unimplemented: {type(t.type).__name__}"
        case _:
            assert False, f"type '{type(t.type).__name__}' has no contained type"


class MVHandleGEPMixin(MVBase):
    def handle_gep(self, instr: ir.GEPInstr):
        # %"2" = getelementptr inbounds i32, i32* %"0", i64 %"1"
        # moves the pointer %"0" forward by one element of type i32 and stores the result in %"2".

        base_ptr: ir.Instruction = instr.pointer
        indices = instr.indices
        # ret_type = instr.type
        size = get_type_size(instr.type)

        # self.align_to(size)
        var = self.variables.new_var(Label(instr.name), self.stack_offset)
        self.stack_offset -= size

        self.last_block.add_instr(
            mips_inst.Addiu(Reg.sp, Reg.sp, -size, mips_inst.IrComment(f"{instr}")),
            mips_inst.Move(Reg.t1, Reg.zero),
        )
        
        ptr_type: ir.PointerType = base_ptr.type

        for i in indices:
            ptr_type = contained_type(ptr_type)
            self.last_block.add_instr(
                self.load_int(i, Reg.t2, mips_inst.Comment(f"load index \"{i}\"")),
                mips_inst.Li(Reg.t3, get_type_size(ptr_type), mips_inst.Comment(f"load type size")),
                mips_inst.Mul(Reg.t2, Reg.t2, Reg.t3, mips_inst.Comment(f"index * type size")),
                mips_inst.Add(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment(f"add offset")),
            )
        self.last_block.add_instr(
            self.load_int(base_ptr, Reg.t2),
            mips_inst.Sub(Reg.t1, Reg.t2, Reg.t1),
            self.store_int(instr, Reg.t1, var.offset),  # store calculated offset
            mips_inst.Blank(),
        )