from llvmlite import ir
from src.parser.visitor.CFG_visitor.cfg_visitor import *

# TODO
class LLVMVisitor(CFGVisitor):
    def __init__(self, cfg: ControlFlowGraph, name: str):
        self.module: ir.Module = ir.Module(name=name)
        void_type = ir.VoidType()
        fnty = ir.FunctionType(void_type, ())
        func = ir.Function(self.module, fnty, name="main")
        block = func.append_basic_block(name="entry")
        self.builder: ir.IRBuilder = ir.IRBuilder(block)
        super().__init__(cfg)
    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        result: dict[str, ir.Type | int | str] = {}
        match node_w.n.type.type:
            case "int":
                result = {"type": ir.IntType(32), "size": 4, "name": node_w.n.identifier}
            case "char":
                result = {"type": ir.IntType(8), "size": 4, "name": node_w.n.identifier}
            case "float":
                result = {"type": ir.FloatType(), "size": 4, "name": node_w.n.identifier}
            case _:
                raise ValueError(f"Error: unrecognized type in variable declaration")
        for ptr in range(0,node_w.n.type.ptr_count):
            result["type"] = ir.PointerType(result["type"])
        self.builder.alloca(result["type"], result["size"], result["name"])
        super().variable_decl(node_w)
    def assign(self, node_w: Wrapper[Assignment]):
        super().assign(node_w)





