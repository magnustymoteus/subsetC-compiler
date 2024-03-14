from llvmlite import ir
from src.parser.visitor.CFG_visitor.cfg_visitor import *
from .mapping import *

'''This visitor assumes that the AST/CFG is in TAC form'''
class LLVMVisitor(CFGVisitor):
    def __init__(self, cfg: ControlFlowGraph, name: str):
        self.module: ir.Module = ir.Module(name=name)
        self.reg_counter: int = 0
        void_type = ir.VoidType()
        fnty = ir.FunctionType(void_type, ())
        func = ir.Function(self.module, fnty, name="main")
        block = func.append_basic_block(name="entry")
        self.builder: ir.IRBuilder = ir.IRBuilder(block)
        super().__init__(cfg)
        self.builder.ret_void()
    def _get_type(self, type: PrimitiveType) -> tuple[ir.Type, int]:
        result: list[ir.Type, int] = []
        match type.type:
            case "int":
                result = [ir.IntType(32), 4]
            case "char":
                result = [ir.IntType(8), 4]
            case "float":
                result = [ir.FloatType(), 4]
            case _:
                raise ValueError(f"Critical Error: unrecognized type")
        for ptr in range(0,type.ptr_count):
            result[0] = ir.PointerType(result[0])
            result[1] = 8
        return result[0], result[1]

    def _get_value_of_terminal(self, node: Identifier | Literal) -> int | str | float:
        if isinstance(node, Identifier):
            return node.name
        return node.value

    def _add_binary_op(self, node_w: Wrapper[BinaryOp], name: str):
        lhs_value : int | float | str = self._get_value_of_terminal(node_w.n.lhs_w.n)
        rhs_value : int | float | str = self._get_value_of_terminal(node_w.n.rhs_w.n)
        match node_w.n.type.type:
            case "int":
                get_signed_int_binary_op_mapping(node_w.n.operator, self.builder)(lhs_value, rhs_value, name)
            case "float":
                get_float_binary_op_mapping(node_w.n.operator, self.builder)(lhs_value, rhs_value, name)
            case _:
                raise ValueError(f"Critical Error: unrecognized type")
    def _add_unary_op(self, node_w: Wrapper[UnaryOp], name: str):
        pass

    def _create_reg_from_expr(self, node_w: Wrapper[Expression]) -> str:
        result: str = str(self.reg_counter)
        match node_w.n:
            case UnaryOp():
                pass
            case BinaryOp():
                pass

        self.reg_counter += 1
        return result


    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        decl_ir_type = self._get_type(node_w.n.type)
        if node_w.n.definition_w.n is not None:
            self.builder.load(decl_ir_type[0], self._create_reg_from_expr(node_w.definition_w), decl_ir_type[1])
        else:
            self.builder.alloca(decl_ir_type[0], decl_ir_type[1], node_w.n.identifier)
        #super().variable_decl(node_w)





