from src.compilation.visitor.AST_visitor import *
from src.constructs import *

class ConstantPropagationVisitor(ASTVisitor):
    """Traverses the AST tree in pre-order to perform constant propagation"""

    def __init__(self, ast: Ast):
        self.propagation_counter: int = 0
        self.propagated_symbols: set[SymbolTableEntry] = set()
        super().__init__(ast)

    @property
    def stop_propagating(self) -> bool:
        return False if self.propagation_counter == 0 else True
    def stop_propagation(self):
        self.propagation_counter += 1
    def start_propagation(self):
        if self.propagation_counter > 0:
            self.propagation_counter -= 1

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
        if entry.cprop_value_w.n is None and entry.definition_w.n is not None:
            return self._lookup_cpropagated_symbol(symtab_w.n.parent, symbol)
        while not entry.stopped_propagating and isinstance(entry.cprop_value_w.n, Identifier):
            return self._lookup_cpropagated_symbol(symtab_w, entry.cprop_value_w.n.name)
        return entry

    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.identifier).cprop_value_w.n = node_w.n.definition_w.n
        is_pointer: bool = node_w.n.type.ptr_count > 0
        if is_pointer:
            self.stop_propagation()
        super().variable_decl(node_w)
        if self.stop_propagating:
            node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.identifier).stopped_propagating = True
        if is_pointer:
            self.start_propagation()

    def un_op(self, node_w: Wrapper[UnaryOp]):
        if node_w.n.operator in ["++", "--"]:
            self.stop_propagation()
        super().un_op(node_w)
        if node_w.n.operator in ["++", "--"]:
            self.start_propagation()
    def enum(self, node_w: Wrapper[Enumeration]):
        super().enum(node_w)
        for i, label in enumerate(node_w.n.chronological_labels):
            symtab_entry = node_w.n.local_symtab_w.n.lookup_symbol(label)
            symtab_entry.cprop_value_w.n = symtab_entry.definition_w.n

    def assign(self, node_w: Wrapper[Assignment]):
        self.visit(node_w.n.value_w)
        if isinstance(node_w.n.assignee_w.n, Identifier):
            symbol: SymbolTableEntry = node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.assignee_w.n.name)
            value_w = wrap(CastOp(node_w.n.type))
            value_w.n.expression_w = node_w.n.value_w
            symbol.cprop_value_w = value_w
            symbol.stopped_propagating = self.stop_propagating

        else:
            self.stop_propagation()
            self.visit(node_w.n.assignee_w)
            self.start_propagation()


    def deref_op(self, node_w: Wrapper[DerefOp]):
        self.stop_propagation()
        if isinstance(node_w.n.operand_w.n, AddressOfOp):
            node_w.n = node_w.n.operand_w.n.operand_w.n
            self.visit(node_w)
        else:
            super().deref_op(node_w)

    def addressof_op(self, node_w: Wrapper[AddressOfOp]):
        self.stop_propagation()
        super().addressof_op(node_w)

    def identifier(self, node_w: Wrapper[Identifier]):
        if node_w.n.local_symtab_w.n is not None:
            if not self.stop_propagating:
                symbol: SymbolTableEntry = self._lookup_cpropagated_symbol(node_w.n.local_symtab_w, node_w.n.name)
                if symbol.cprop_value_w.n is not None and symbol.type.ptr_count == 0 and not symbol.stopped_propagating:
                    self.propagated_symbols.add(symbol)
                    value = symbol.cprop_value_w
                    CopyVisitor().visit(value)
                    node_w.n = value.n
            else:
                node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.name).stopped_propagating = True
    def object_access(self, node_w: Wrapper[ObjectAccess]):
        self.stop_propagation()
        super().object_access(node_w)
        self.start_propagation()
    def iteration(self, node_w: Wrapper[IterationStatement]):
        self.stop_propagation()
        super().iteration(node_w)
        self.start_propagation()
    def array_access(self, node_w: Wrapper[ArrayAccess]):
        self.stop_propagation()
        super().array_access(node_w)
        self.start_propagation()

