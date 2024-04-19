from src.compilation.visitor.AST_visitor import *
from src.constructs import *

class ConstantPropagationVisitor(ASTVisitor):
    """Traverses the AST tree in pre-order to perform constant propagation along other small optimizations (operator
    assignments, removing code after jump statements)"""

    def __init__(self, ast: Ast):
        self.stop_propagating: bool = False
        self.propagated_symbols: set[SymbolTableEntry] = set()
        super().__init__(ast)

    def stop_propagation(self):
        self.stop_propagating = True
    def start_propagation(self):
        self.stop_propagating = False

    def compound_stmt(self, node_w: Wrapper[CompoundStatement]):
        for i, statement_w in enumerate(node_w.n.statements):
            symbols_before = self.propagated_symbols
            self.visit(statement_w)
            symbols_after = self.propagated_symbols
            for stopped_symbol in symbols_after-symbols_before:
                stopped_symbol.stopped_propagating = True
            self.propagated_symbols.clear()
            if isinstance(statement_w.n, ReturnStatement):
                node_w.n.statements = node_w.n.statements[:i + 1]
                break

    def _lookup_cpropagated_symbol(self, symtab_w: Wrapper[SymbolTable], symbol: str):
        entry = symtab_w.n.lookup_symbol(symbol)
        while not entry.stopped_propagating and isinstance(entry.value_w.n, Identifier):
            return self._lookup_cpropagated_symbol(symtab_w, entry.value_w.n.name)
        return entry

    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        if node_w.n.type.ptr_count > 0:
            self.stop_propagation()
            node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.identifier).stopped_propagating = True
        super().variable_decl(node_w)
        self.start_propagation()

    def un_op(self, node_w: Wrapper[UnaryOp]):
        if node_w.n.operator in ["++", "--"]:
            symbol: SymbolTableEntry = node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.operand_w.n.name)
            symbol.stopped_propagating = True
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
                symbol.value_w = node_w.n.value_w
                symbol.stopped_propagating = self.stop_propagating

    def deref_op(self, node_w: Wrapper[DerefOp]):
        if isinstance(node_w.n.operand_w.n, AddressOfOp):
            node_w.n = node_w.n.operand_w.n.operand_w.n
            self.visit(node_w)
        else:
            super().deref_op(node_w)

    def addressof_op(self, node_w: Wrapper[AddressOfOp]):
        pass

    def identifier(self, node_w: Wrapper[Identifier]):
        if not self.stop_propagating:
            symbol: SymbolTableEntry = self._lookup_cpropagated_symbol(node_w.n.local_symtab_w, node_w.n.name)
            if symbol.value_w.n is not None and symbol.type.ptr_count == 0 and not symbol.stopped_propagating:
                self.propagated_symbols.add(symbol)
                value = symbol.value_w
                CopyVisitor().visit(value)
                node_w.n = value.n
                node_w.n.type = symbol.type
        else:
            node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.name).stopped_propagating = True
    def iteration(self, node_w: Wrapper[IterationStatement]):
        pass

