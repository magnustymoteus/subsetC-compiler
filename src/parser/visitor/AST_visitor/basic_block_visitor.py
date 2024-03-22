from src.parser.visitor.AST_visitor.ast_visitor import *
from src.parser.CFG import *

class BasicBlockVisitor(ASTVisitor):
    def __init__(self, ast: Ast):
        self.cfg: ControlFlowGraph = ControlFlowGraph()
        self.current_basic_block_w: Wrapper[BasicBlock] = wrap(BasicBlock())
        self.cfg.bblock_list.n.basic_blocks.append(self.current_basic_block_w)
        super().__init__(ast)

    def program(self, node_w: Wrapper[Program]):
        for statement_w in node_w.n.children:
            self.current_basic_block_w.n.local_symtab_w = statement_w.n.local_symtab_w
            if not isinstance(statement_w.n, CompoundStatement):
                self.current_basic_block_w.n.ast_items.append(statement_w)
            self.visit(statement_w)

    def compound_stmt(self, node_w: Wrapper[CompoundStatement]):
        # TODO future: handle abnormal terminated statements (if, else if, else, switch, ...)
        for statement_w in node_w.n.statements:
            if not isinstance(statement_w.n, CompoundStatement):
                self.current_basic_block_w.n.ast_items.append(statement_w)
            self.visit(statement_w)





