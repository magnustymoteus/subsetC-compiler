from src.parser.visitor.AST_visitor.ast_visitor import *
from src.parser.CFG import *

class CFGVisitor(ASTVisitor):
    def __init__(self, cfg: ControlFlowGraph):
        self.visit(cfg.bblock_list)

    def visit(self, node_w: Wrapper[CFGNode]):
        match node_w.n:
            case BasicBlockList():
                return self.basic_block_list(node_w)
            case BasicBlock():
                return self.basic_block(node_w)
            case _:
                return super().visit(node_w)


    def basic_block_list(self, node_w: Wrapper[BasicBlockList]):
        for basic_block in node_w.n.basic_blocks:
            self.visit(basic_block)
    def basic_block(self, node_w: Wrapper[BasicBlock]):
        for ast_item in node_w.n.ast_items:
            self.visit(ast_item)




