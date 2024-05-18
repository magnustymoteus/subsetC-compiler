from src.compilation.visitor.AST_visitor.ast_visitor import *
from src.compilation.optimizer.constant_propagation_visitor import *

'''Here we traverse the AST in pre-order(top down) in terms of making symbol tables and references to them '''
class SymbolTableVisitor(ASTVisitor):
    """
    A visitor class for building and managing symbol tables during AST traversal.

    Attributes:
        stack (list[Wrapper[SymbolTable]]): A stack to keep track of symbol tables.

    Methods:
        _get_most_local_sym_tab(self) -> Wrapper[SymbolTable]: Returns the most local symbol table from the stack.
        visit(self, node_w: Wrapper[Basic]): Visits a node in the AST and updates the local symbol table.
        __init__(self, ast: Ast): Initializes the SymbolTableVisitor with the given AST.
        program(self, node_w: Wrapper[Program]): Visits the program node in the AST and creates a global scope symbol table.
        identifier(self, node_w: Wrapper[Identifier]): Visits an identifier node in the AST and checks if the symbol is declared.
        compound_stmt(self, node_w: Wrapper[CompoundStatement]): Visits a compound statement node in the AST and creates a new symbol table.
        cast_op(self, node_w: Wrapper[CastOp]): Visits a cast operation node in the AST.
        variable_decl(self, node_w: Wrapper[VariableDeclaration]): Visits a variable declaration node in the AST and adds the symbol to the symbol table.
        enum(self, node_w: Wrapper[Enumeration]): Visits an enumeration node in the AST and adds the symbols to the symbol table.
    """

    def _get_most_local_sym_tab(self) -> Wrapper[SymbolTable]:
        """
        Returns the most local symbol table from the stack.

        Returns:
            Wrapper[SymbolTable]: The most local symbol table.
        """
        return self.stack[-1]

    def visit(self, node_w: Wrapper[Basic]):
        """
        Visits a node in the AST and updates the local symbol table.

        Args:
            node_w (Wrapper[Basic]): The wrapped node to visit.

        Returns:
            Any: The result of visiting the node.
        """
        if len(self.stack) > 0:
            node_w.n.local_symtab_w = self._get_most_local_sym_tab()
        return super().visit(node_w)

    def __init__(self, ast: Ast):
        """
        Initializes the SymbolTableVisitor with the given AST as well as the constant propagation visitor

        Args:
            ast (Ast): The abstract syntax tree.
        """
        self.stack: list[Wrapper[SymbolTable]] = list()
        super().__init__(ast)

    def program(self, node_w: Wrapper[Program]):
        """
        Visits the program node in the AST and creates a global scope symbol table.

        Args:
            node_w (Wrapper[Program]): The wrapped program node to visit.
        """
        # make global scope symbol table
        self.stack.append(wrap(SymbolTable()))
        super().program(node_w)
        self.stack.pop()

    def func_call(self, node_w: Wrapper[FunctionCall]):
        super().func_call(node_w)
        if not node_w.n.local_symtab_w.n.symbol_exists(node_w.n.func_name):
            self.raiseSemanticErr(f"Undeclared function {node_w.n.func_name}")
        else:
            symbol_entry = node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.func_name)
            if symbol_entry.definition_w.n is None:
                self.raiseSemanticErr(f"Function {node_w.n.func_name} declared without definition")

    def identifier(self, node_w: Wrapper[Identifier]):
        """
        Visits an identifier node in the AST and checks if the symbol is declared.

        Args:
            node_w (Wrapper[Identifier]): The wrapped identifier node to visit.
        """
        symtab_entry = node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.name)
        # if the symbol is not found in the current symbol table raise an error
        if symtab_entry is None:
            self.raiseSemanticErr(f"Undeclared variable {node_w.n.name}")
        if symtab_entry.is_enum:
            value = symtab_entry.definition_w
            CopyVisitor().visit(value)
            node_w.n = value.n

    def object_access(self, node_w: Wrapper[ObjectAccess]):
        self.visit(node_w.n.object_w)

    def compound_stmt(self, node_w: Wrapper[CompoundStatement]):
        """
        Visits a compound statement node in the AST and creates a new symbol table.

        Args:
            node_w (Wrapper[CompoundStatement]): The wrapped compound statement node to visit.
        """
        new_symtab = wrap(SymbolTable(self._get_most_local_sym_tab()))
        self.stack.append(new_symtab)
        super().compound_stmt(node_w)
        self.stack.pop()

    def func_decl(self, node_w: Wrapper[FunctionDeclaration]):
        function_encloser = wrap(FunctionEncloser(self._get_most_local_sym_tab(), node_w.n.type))
        self.stack.append(function_encloser)
        statements = node_w.n.body_w.n.statements
        node_w.n.body_w.n.statements = node_w.n.parameters+statements
        entry = SymbolTableEntry(node_w.n.name, node_w.n.type)
        entry.definition_w = node_w.n.body_w
        node_w.n.local_symtab_w.n.add_symbol(entry)
        self.visit(node_w.n.body_w)
        node_w.n.body_w.n.statements = statements
        self.stack.pop()



    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        """
        Visits a variable declaration node in the AST and adds the symbol to the symbol table.

        Args:
            node_w (Wrapper[VariableDeclaration]): The wrapped variable declaration node to visit.
        """
        super().variable_decl(node_w)
        symbol_name = node_w.n.identifier
        if node_w.n.local_symtab_w.n.symbol_exists_in_scope(symbol_name):
            decl_or_def: str = "Redeclaration" if not node_w.n.definition_w.n else "Redefinition"
            self.raiseSemanticErr(f"{decl_or_def} of symbol {symbol_name}")
        symtab_entry = SymbolTableEntry(symbol_name, node_w.n.type)
        symtab_entry.definition_w.n = node_w.n.definition_w.n
        symtab_entry.definition_w.n = node_w.n.definition_w.n
        node_w.n.local_symtab_w.n.add_symbol(symtab_entry)

    def enum(self, node_w: Wrapper[Enumeration]):
        """
        Visits an enumeration node in the AST and adds the symbols to the symbol table.

        Args:
            node_w (Wrapper[Enumeration]): The wrapped enumeration node to visit.
        """
        super().enum(node_w)
        for i, label in enumerate(node_w.n.chronological_labels):
            current_symtab_entry = SymbolTableEntry(label, node_w.n.type)
            current_symtab_entry.is_enum = True
            lit = IntLiteral(i)
            current_symtab_entry.definition_w.n = lit
            current_symtab_entry.definition_w.n = lit
            node_w.n.local_symtab_w.n.add_symbol(current_symtab_entry)
        symtab_entry = SymbolTableEntry(node_w.n.name, node_w.n.type)
        node_w.n.local_symtab_w.n.add_symbol(symtab_entry)
