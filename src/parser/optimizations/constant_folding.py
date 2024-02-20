from ..AST import *


def constant_folding(ast: Ast):
    for node_w in ast.iter(AstIterPostorder):
        match node_w.n:
            case AstBinOpNode():
                if isinstance(node_w.n.lhs, AstLiteralNode) and isinstance(node_w.n.rhs, AstLiteralNode):
                    pass
            case AstUnOpNode():
                if isinstance(node_w.n.operand, AstLiteralNode):
                    pass
