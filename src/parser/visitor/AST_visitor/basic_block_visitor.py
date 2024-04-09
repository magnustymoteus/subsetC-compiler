from src.parser.CFG.node.basic_block import BasicBlock
from src.parser.visitor.AST_visitor.ast_visitor import *
from src.parser.CFG import *
from src.parser.visitor.AST_visitor.copy_visitor import *

class BasicBlockVisitor(ASTVisitor):
    def __init__(self, ast: Ast):
        self.cfg: ControlFlowGraph = ControlFlowGraph()
        self.add_bblock_next: bool = False
        self.assign_end_branch: bool = False
        self.statement_stack: list[Wrapper[Statement]] = []
        self.current_basic_block_w: Wrapper[BasicBlock] = None
        super().__init__(ast)

    def add_node_to_bblock(self, node_w: Wrapper[Basic]):
        self.current_basic_block_w = self.cfg.add_basic_block()
        self.current_basic_block_w.n.local_symtab_w = node_w.n.local_symtab_w
        node_w.n.basic_block_w = self.current_basic_block_w
        if isinstance(node_w.n, CompoundStatement):
            for statement_w in node_w.n.statements:
                node_w.n.basic_block_w.n.ast_items.append(statement_w)
        else:
            node_w.n.basic_block_w.n.ast_items.append(node_w)
    def visit(self, node_w: Wrapper[Basic]):
        if self.add_bblock_next:
            self.add_node_to_bblock(node_w)
            self.add_bblock_next = False
        if self.assign_end_branch:
            for selection_w in self.statement_stack:
                selection_w.n.end_branch_w = node_w
            self.assign_end_branch = False
            self.statement_stack.clear()

        if self.current_basic_block_w is not None:
            node_w.n.basic_block_w = self.current_basic_block_w
        super().visit(node_w)
    def program(self, node_w: Wrapper[Program]):
        self.add_bblock_next: bool = True
        for child_w in node_w.n.children:
            self.visit(child_w)
    def select(self, node_w: Wrapper[SelectionStatement]):
        is_root: bool = len(self.statement_stack) == 0
        self.add_node_to_bblock(node_w)
        for condition_w in node_w.n.conditions:
            self.visit(condition_w)
        for i in range(0, len(node_w.n.branches)):
            self.add_node_to_bblock(node_w.n.branches[i])
            self.visit(node_w.n.branches[i])
        if node_w.n.default_branch_w is not None:
            self.add_node_to_bblock(node_w.n.default_branch_w)
            self.visit(node_w.n.default_branch_w)
        self.statement_stack.append(node_w)
        self.assign_end_branch = is_root
    def iteration(self, node_w: Wrapper[IterationStatement]):
        is_root: bool = len(self.statement_stack) == 0
        self.add_node_to_bblock(node_w)
        self.visit(node_w.n.condition_w)
        self.add_node_to_bblock(node_w.n.body_w)
        self.visit(node_w.n.body_w)
        self.statement_stack.append(node_w)
        self.assign_end_branch = is_root

