from src.compilation.visitor.AST_visitor import *

class DeadCodeVisitor(ASTVisitor):

    def __init__(self, ast: Ast):
        self.dead_nodes: list[Wrapper] = []
        self.false_conditionals: list[Wrapper[ConditionalStatement]] = []
        self.working_var: str | None = None
        super().__init__(ast)
    def mark_wvar_as_used(self, symtab: SymbolTable):
        symtab.lookup_symbol(self.working_var).used = True
    def assign(self, node_w: Wrapper[Assignment]):
        self.mark_wvar_as_used(node_w.n.local_symtab_w.n)
        super().assign(node_w)
    def un_op(self, node_w: Wrapper[UnaryOp]):
        if node_w.n.operator in ["++", "--"]:
            self.mark_wvar_as_used(node_w.n.local_symtab_w.n)
        super().un_op(node_w)
    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        self.working_var = node_w.n.identifier
        super().variable_decl(node_w)

    def identifier(self, node_w: Wrapper[Identifier]):
        node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.name).used = True
    def compound_stmt(self, node_w: Wrapper[CompoundStatement]):
        super().compound_stmt(node_w)
        for stmt_w in node_w.n.statements:
            if isinstance(stmt_w.n, VariableDeclaration):
                if not stmt_w.n.local_symtab_w.n.lookup_symbol(stmt_w.n.identifier).used:
                    self.dead_nodes.append(stmt_w)
        for dead_node_w in self.dead_nodes:
            if dead_node_w in node_w.n.statements:
                node_w.n.statements.remove(dead_node_w)
        for false_conditional_w in self.false_conditionals:
            if false_conditional_w in node_w.n.statements:
                if false_conditional_w.n.false_branch_w is None:
                    node_w.n.statements.remove(false_conditional_w)
                else:
                    index = node_w.n.statements.index(false_conditional_w)
                    node_w.n.statements[index] = false_conditional_w.n.false_branch_w

    def conditional(self, node_w: Wrapper[ConditionalStatement]):
        super().conditional(node_w)
        if isinstance(node_w.n.condition_w.n, IntLiteral) and node_w.n.condition_w.n.value == 0:
            self.false_conditionals.append(node_w)

    def iteration(self, node_w: Wrapper[IterationStatement]):
        if isinstance(node_w.n.condition_w.n, IntLiteral) and node_w.n.condition_w.n.value == 0:
            self.dead_nodes.append(node_w)
        else:
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
    def object_access(self, node_w: Wrapper[ObjectAccess]):
        node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.identifier_w.n.name).used = True
    def composite_decl(self, node_w: Wrapper[CompositeDeclaration]):
        pass

