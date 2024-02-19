from ..AST import *


def constant_folding(ast: Ast):
    for node in ast.iter(AstIterPostorder):
        match node:
            case AstBinOpNode():
                pass
            case AstUnOpNode():
                pass
