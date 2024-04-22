from src.constructs.CFG.node.basic_block import BasicBlock
from src.constructs.CFG import *
from src.compilation.visitor.AST_visitor.ast_visitor import *
from src.compilation.visitor.AST_visitor.copy_visitor import *
from copy import copy
class BasicBlockVisitor(ASTVisitor):
    """
    A visitor class for creating basic blocks in the control flow graph (CFG).

    Attributes:
        cfg (ControlFlowGraph): The control flow graph.
        assign_end_branch (bool): Flag indicating whether to assign the end branch.
        statement_stack (list[Wrapper[Statement]]): Stack to keep track of statements.
        current_basic_block_w (Wrapper[BasicBlock]): The current basic block wrapper.
        add_bblock_next (bool): Flag indicating whether to add a new basic block next.
    """

    def __init__(self, ast: Ast):
        self.cfg: ControlFlowGraph = ControlFlowGraph()
        self.assign_end_branch: bool = False
        self.statement_stack: list[Wrapper[Statement]] = []
        self.current_basic_block_w: Wrapper[BasicBlock] = None
        self.add_bblock_next: bool = False
        super().__init__(ast)

    def create_bblock(self, node_w: Wrapper[Basic]):
        """
        Creates a new basic block from a node and returns the node itself inside the new block.

        Args:
            node_w (Wrapper[Basic]): The node wrapper.

        Returns:
            Basic: The node inside the new basic block.
        """
        self.current_basic_block_w = self.cfg.add_basic_block()
        self.current_basic_block_w.n.local_symtab_w = node_w.n.local_symtab_w
        node_w.n.basic_block_w = self.current_basic_block_w
        node_copy_w = wrap(copy(node_w.n))
        node_w.n.basic_block_w.n.ast_items.append(node_copy_w)
        node_w.n = self.current_basic_block_w.n
        return self.current_basic_block_w.n.ast_items[-1]

    def func_decl(self, node_w: Wrapper[FunctionDeclaration]):
        self.add_bblock_next: bool = True
        self.visit(node_w.n.body_w)

    def visit(self, node_w: Wrapper[Basic]):
        """
        Visits a basic node.

        Args:
            node_w (Wrapper[Basic]): The node wrapper.
        """
        if self.add_bblock_next:
            node_w = self.create_bblock(node_w)
            self.add_bblock_next = False
        if self.assign_end_branch:
            for selection_w in self.statement_stack:
                selection_w.n.end_branch_w = self.current_basic_block_w
            self.assign_end_branch = False
            self.statement_stack.clear()

        super().visit(node_w)

    def switch(self, node_w: Wrapper[SwitchStatement]):
        # Add implementation for the switch method
        pass
        """
        Visits a switch statement node.

        Args:
            node_w (Wrapper[SwitchStatement]): The switch statement node wrapper.
        """
        is_root: bool = len(self.statement_stack) == 0
        for condition_w in node_w.n.conditions:
            self.visit(condition_w)
        for i in range(0, len(node_w.n.branches)):
            self.visit(self.create_bblock(node_w.n.branches[i]))
        self.statement_stack.append(node_w)
        self.add_bblock_next = is_root

    def conditional(self, node_w: Wrapper[ConditionalStatement]):
        """
        Visits a conditional statement node.

        Args:
            node_w (Wrapper[ConditionalStatement]): The conditional statement node wrapper.
        """
        is_root: bool = len(self.statement_stack) == 0
        self.visit(self.create_bblock(node_w.n.condition_w))
        self.visit(self.create_bblock(node_w.n.true_branch_w))
        if node_w.n.false_branch_w is not None:
            self.visit(self.create_bblock(node_w.n.false_branch_w))
        self.statement_stack.append(node_w)
        self.add_bblock_next = is_root

    def iteration(self, node_w: Wrapper[IterationStatement]):
        """
        Visits an iteration statement node.

        Args:
            node_w (Wrapper[IterationStatement]): The iteration statement node wrapper.
        """
        is_root: bool = len(self.statement_stack) == 0
        if node_w.n.adv_w is not None:
            self.visit(self.create_bblock(node_w.n.adv_w))
        self.visit(self.create_bblock(node_w.n.condition_w))
        self.visit(self.create_bblock(node_w.n.body_w))
        self.statement_stack.append(node_w)
        self.add_bblock_next = is_root

