from src.parser.visitor.AST_visitor.ast_visitor import *
from src.parser.visitor.AST_visitor.copy_visitor import *
from copy import deepcopy


class OptimizationVisitor(ASTVisitor):
    """Traverses the AST tree in pre-order to perform constant propagation along other small optimizations (operator
    assignments, removing code after jump statements)"""

    def __init__(self, ast: Ast):
        super().__init__(ast)

    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        if node_w.n.definition_w.n is not None:
            self.visit(node_w.n.definition_w)

    def un_op(self, node_w: Wrapper[UnaryOp]):
        if node_w.n.operator in ["++", "--"]:
            if isinstance(node_w.n.operand_w.n, Identifier):
                symbol: SymbolTableEntry = node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.operand_w.n.name)
                symbol.has_changed = True
        super().un_op(node_w)

    def assign(self, node_w: Wrapper[Assignment]):
        if len(node_w.n.operator) > 1:
            operator: str = node_w.n.operator[0]
            node_w.n.operator = "="
            assignee_copy_w: Wrapper[Identifier] = wrap((node_w.n.assignee_w.n))
            value_copy_w: Wrapper[Expression] = wrap((node_w.n.value_w.n))
            CopyVisitor().visit(assignee_copy_w)
            CopyVisitor().visit(value_copy_w)

            bin_op: BinaryOp = BinaryOp(operator)
            bin_op.lhs_w = assignee_copy_w
            bin_op.rhs_w = value_copy_w
            bin_op.type = node_w.n.type
            bin_op.local_symtab_w.n = node_w.n.local_symtab_w.n

            node_w.n.value_w.n = bin_op
            self.visit(node_w)
        else:
            self.visit(node_w.n.value_w)
            if isinstance(node_w.n.assignee_w.n, Identifier):
                symbol: SymbolTableEntry = node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.assignee_w.n.name)
                symbol.has_changed = True

    def deref_op(self, node_w: Wrapper[DerefOp]):
        if isinstance(node_w.n.operand_w.n, AddressOfOp):
            node_w.n = node_w.n.operand_w.n.operand_w.n
            self.visit(node_w)
        else:
            super().deref_op(node_w)

    def addressof_op(self, node_w: Wrapper[AddressOfOp]):
        if not isinstance(node_w.n.operand_w.n, Identifier):
            self.visit(node_w.n.operand_w)

    def identifier(self, node_w: Wrapper[Identifier]):
        symbol: SymbolTableEntry = node_w.n.local_symtab_w.n.lookup_cpropagated_symbol(node_w.n.name)
        if symbol.type.ptr_count == 0 and not symbol.has_changed:
            value = symbol.value_w
            CopyVisitor().visit(value)
            node_w.n = value.n
    def iteration(self, node_w: Wrapper[IterationStatement]):
        self.visit(node_w.n.adv_w)
        self.visit(node_w.n.condition_w)
        for i, statement_w in enumerate(node_w.n.body_w.n.statements):
            self.visit(statement_w)
            if isinstance(statement_w.n, JumpStatement):
                node_w.n.body_w.n.statements = node_w.n.body_w.n.statements[:i+1]
                break
    def switch(self, node_w: Wrapper[SwitchStatement]):
        self.visit(node_w.n.value_w)
        for condition_w in node_w.n.conditions:
            self.visit(condition_w)
        for branch_w in node_w.n.branches:
            for i, statement_w in enumerate(branch_w.n.statements):
                self.visit(statement_w)
                if isinstance(statement_w.n, JumpStatement):
                    branch_w.n.statements = branch_w.n.statements[:i+1]
                    break
