from src.compilation.visitor import ASTVisitor
from src.constructs import *

class CFGVisitor(ASTVisitor):
    def __init__(self, cfg: ControlFlowGraph):
        for basic_block_w in cfg.basic_blocks:
            self.visit(basic_block_w)

    def visit(self, node_w: Wrapper[CFGNode]):
        match node_w.n:
            case BasicBlock():
                return self.basic_block(node_w)
            case _:
                return super().visit(node_w)


    def basic_block(self, node_w: Wrapper[BasicBlock]):
        for ast_item in node_w.n.ast_items:
            self.visit(ast_item)




