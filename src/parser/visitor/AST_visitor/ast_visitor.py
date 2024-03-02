from src.parser import *
from src.parser.node import *
from src.symbol_table import *
class ASTVisitor():
    def __init__(self, ast: Ast):
        self.visit(ast.root_w)

    def visit(self, node_w: Wrapper[NodeType]):
        match node_w.n:
            case Program():
                self.program(node_w)
            case Assignment():
                self.assign(node_w)
            case BinaryOp():
                self.bin_op(node_w)
            case DerefOp():
                self.deref_op(node_w)
            case AddressOfOp():
                self.addressof_op(node_w)
            case UnaryOp():
                self.un_op(node_w)
            case CompoundStatement():
                self.compound_stmt(node_w)
            case FunctionDefinition():
                self.func_def(node_w)
            case VariableDeclaration():
                self.variable_decl(node_w)
            case Literal():
                self.lit(node_w)
            case Identifier():
                self.identifier(node_w)
            case _:
                raise Exception

    
    def program(self, node_w: Wrapper[Program]):
        """Method called when encountering a Program node."""
        for child in node_w.n.children:
            self.visit(child)
    
    def bin_op(self, node_w: Wrapper[BinaryOp]):
        """Method called when encountering a BinOp node."""
        self.visit(node_w.n.lhs_w)
        self.visit(node_w.n.rhs_w)

    def deref_op(self, node_w: Wrapper[DerefOp]):
        self.un_op(node_w)

    def addressof_op(self, node_w: Wrapper[AddressOfOp]):
        self.un_op(node_w)
    
    def un_op(self, node_w: Wrapper[UnaryOp]):
        """Method called when encountering a UnOp node."""
        self.visit(node_w.n.operand_w)

    
    def lit(self, node_w: Wrapper[Literal]):
        """Method called when encountering a UnOp node."""
        pass
    
    def assign(self, node_w: Wrapper[Assignment]):
        """Method called when encountering a Assign node."""
        self.visit(node_w.n.assignee_w)
        self.visit(node_w.n.value_w)
    
    def identifier(self, node_w: Wrapper[Identifier]):
        """Method called when encountering a Assign node."""
        pass

    
    def compound_stmt(self, node_w: Wrapper[CompoundStatement]):
        """Method called when encountering a Assign node."""
        for statement in node_w.n.statements:
            self.visit(statement)

    
    def func_def(self, node_w: Wrapper[FunctionDefinition]):
        """Method called when encountering a Assign node."""
        pass

    
    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        """Method called when encountering a Assign node."""
        if node_w.n.definition_w.n is not None:
            self.visit(node_w.n.definition_w)



