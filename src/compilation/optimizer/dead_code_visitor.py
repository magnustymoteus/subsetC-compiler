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
        if node_w.n.local_symtab_w.n is not None:
            node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.name).used = True
    def compound_stmt(self, node_w: Wrapper[CompoundStatement]):
        for i, stmt_w in enumerate(node_w.n.statements):
            if isinstance(stmt_w.n, JumpStatement):
                node_w.n.statements = node_w.n.statements[:i+1]
        super().compound_stmt(node_w)
        for i, stmt_w in enumerate(node_w.n.statements):
            if isinstance(stmt_w.n, VariableDeclaration):
                if not stmt_w.n.local_symtab_w.n.lookup_symbol(stmt_w.n.identifier).used:
                    self.dead_nodes.append(stmt_w)

        for dead_node_w in self.dead_nodes:
            if dead_node_w in node_w.n.statements:
                node_w.n.statements.remove(dead_node_w)
        for false_conditional_w in self.false_conditionals:
            if false_conditional_w in node_w.n.statements:
                self.raiseWarning(f"condition is never true.")
                if false_conditional_w.n.false_branch_w is None:
                    node_w.n.statements.remove(false_conditional_w)
                else:
                    index = node_w.n.statements.index(false_conditional_w)
                    node_w.n.statements[index] = false_conditional_w.n.false_branch_w

    def conditional(self, node_w: Wrapper[ConditionalStatement]):
        if isinstance(node_w.n.condition_w.n, IntLiteral) and node_w.n.condition_w.n.value == 0:
            self.false_conditionals.append(node_w)
        super().conditional(node_w)


    def iteration(self, node_w: Wrapper[IterationStatement]):
        if isinstance(node_w.n.condition_w.n, IntLiteral) and node_w.n.condition_w.n.value == 0:
            self.dead_nodes.append(node_w)
        else:
            super().iteration(node_w)
    def object_access(self, node_w: Wrapper[ObjectAccess]):
        if isinstance(node_w.n.object_w.n, Identifier):
            node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.object_w.n.name).used = True
        super().object_access(node_w)
    def composite_decl(self, node_w: Wrapper[CompositeDeclaration]):
        pass

