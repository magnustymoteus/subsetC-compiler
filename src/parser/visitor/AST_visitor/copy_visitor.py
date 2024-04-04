from src.parser.visitor.AST_visitor.ast_visitor import *
from copy import deepcopy


class CopyVisitor(ASTVisitor):
    def __init__(self):
        pass

    def visit(self, node_w: Wrapper[Basic]):
        node_w.n = deepcopy(node_w.n)
        node_w.n.id = uuid4()
        match node_w.n:
            case Program():
                self.program(node_w)
            case Assignment():
                self.assign(node_w)
            case BinaryOp():
                self.bin_op(node_w)
            case DerefOp():
                self.deref_op(node_w)
            case AddressOfOp():
                self.addressof_op(node_w)
            case UnaryOp():
                self.un_op(node_w)
            case CastOp():
                self.cast_op(node_w)
            case CompoundStatement():
                self.compound_stmt(node_w)
            case FunctionDefinition():
                self.func_def(node_w)
            case VariableDeclaration():
                self.variable_decl(node_w)
            case Literal():
                self.lit(node_w)
            case Identifier():
                self.identifier(node_w)
            case Enumeration():
                self.enum(node_w)
            case _:
                raise Exception
