from src.parser.visitor.AST_visitor.ast_visitor import *

'''Here we traverse the AST in pre-order(top down) in terms of making symbol tables and references to them '''
class SymbolTableVisitor(ASTVisitor):
    def _get_most_local_sym_tab(self) -> Wrapper[SymbolTable]:
        return self.stack[-1]

    def __init__(self, ast: Ast):
        self.stack: list[Wrapper[SymbolTable]] = list()
        super().__init__(ast)

    def program(self, node_w: Wrapper[Program]):
        # make global scope symbol table
        self.stack.append(wrap(SymbolTable()))
        super().program(node_w)
        self.stack.pop()

    def bin_op(self, node_w: Wrapper[BinaryOp]):
        # TODO : why is local_symtab_w not set in the super class?
        node_w.n.local_symtab_w = self._get_most_local_sym_tab()
        super().bin_op(node_w)

    def un_op(self, node_w: Wrapper[UnaryOp]):
        node_w.n.local_symtab_w = self._get_most_local_sym_tab()
        super().un_op(node_w)

    def deref_op(self, node_w: Wrapper[DerefOp]):
        super().deref_op(node_w)

    def addressof_op(self, node_w: Wrapper[AddressOfOp]):
        super().addressof_op(node_w)

    def lit(self, node_w: Wrapper[Literal]):
        node_w.n.local_symtab_w = self._get_most_local_sym_tab()

    def assign(self, node_w: Wrapper[Assignment]):
        node_w.n.local_symtab_w = self._get_most_local_sym_tab()
        super().assign(node_w)

    def identifier(self, node_w: Wrapper[Identifier]):
        node_w.n.local_symtab_w = self._get_most_local_sym_tab()
        # if the symbol is not found in the current symbol table raise an error
        if node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.name) is None:
            self.raiseSemanticErr(f"Undeclared variable {node_w.n.name}")


    def compound_stmt(self, node_w: Wrapper[CompoundStatement]):
        node_w.n.local_symtab_w = self._get_most_local_sym_tab()
        new_symtab = wrap(SymbolTable(self._get_most_local_sym_tab()))
        self.stack.append(new_symtab)
        super().compound_stmt(node_w)
        self.stack.pop()

    def cast_op(self, node_w: Wrapper[CastOp]):
        node_w.n.local_symtab_w = self._get_most_local_sym_tab()
        super().cast_op(node_w)

    def func_def(self, node_w: Wrapper[FunctionDefinition]):
        # TODO
        pass

    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        node_w.n.local_symtab_w = self._get_most_local_sym_tab()
        super().variable_decl(node_w)
        symbol_name = node_w.n.identifier
        if node_w.n.local_symtab_w.n.symbol_exists(symbol_name):
            decl_or_def : str = "Redeclaration" if not node_w.n.definition_w.n else "Redefinition"
            self.raiseSemanticErr(f"{decl_or_def} of symbol {symbol_name}")
        symtab_entry = SymbolTableEntry(symbol_name, node_w.n.type)
        symtab_entry.definition_w.n = node_w.n.definition_w.n
        # TODO: shouldn't this be value_w instead of definition_w?
        symtab_entry.value_w.n = node_w.n.definition_w.n
        node_w.n.local_symtab_w.n.add_symbol(symtab_entry)
