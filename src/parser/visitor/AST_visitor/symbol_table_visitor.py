from src.parser import *
from src.parser.node import *
from src.symbol_table import *
from src.parser.ast import Stack
class SymbolTableVisitor(AstVisit):
    def visit(self) -> SymbolTable:
        #elf.symtab_stack: Stack = Stack()
        #self.root = T
        self.__iter__()
        return
    def __init__(self, ast: Ast):
        super().__init__(ast)
    def program(self, node_w: Wrapper[Program]):
        """Method called when encountering a Program node."""
        pass
    def bin_op(self, node_w: Wrapper[BinaryOp]):
        """Method called when encountering a BinOp node."""
        pass
    def un_op(self, node_w: Wrapper[UnaryOp]):
        """Method called when encountering a UnOp node."""
        pass

    def lit(self, node_w: Wrapper[Literal]):
        """Method called when encountering a UnOp node."""
        pass
    def assign(self, node_w: Wrapper[Assignment]):
        """Method called when encountering a Assign node."""
        pass

    def identifier(self, node_w: Wrapper[Identifier]):
        """Method called when encountering a Assign node."""
        pass

    def compound_stmt(self, node_w: Wrapper[CompoundStatement]):
        """Method called when encountering a Assign node."""
        pass

    def func_def(self, node_w: Wrapper[FunctionDefinition]):
        """Method called when encountering a Assign node."""
        pass

    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        """Method called when encountering a Assign node."""
        pass


