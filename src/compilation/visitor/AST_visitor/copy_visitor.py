from src.constructs import *
from .ast_visitor import *
from copy import deepcopy


class CopyVisitor(ASTVisitor):
    def __init__(self):
        pass

    def visit(self, node_w: Wrapper[Basic]):
        node_w.n = deepcopy(node_w.n)
        node_w.n.id = uuid4()
        return super().visit(node_w)
