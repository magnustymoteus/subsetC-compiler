from src.parser.AST import *
from src.symbol_table import *
from src.parser.AST.ast import *
import warnings

class SemanticError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
class ASTVisitor():
    def __init__(self, ast: Ast):
        self.visit(ast.root_w)
        self.current_line_nr: int = 0
        self.current_col_nr: int = 0

    def raiseSemanticErr(self, message: str):
        raise SemanticError(f"{self.current_line_nr}:{self.current_col_nr}:error: {message}")

    def raiseWarning(self, message: str):
        warnings.warn(f"{self.current_line_nr}:{self.current_col_nr}:error: {message}")

    def visit(self, node_w: Wrapper[Basic]):
        self.current_col_nr = node_w.n.col_nr
        self.current_line_nr = node_w.n.line_nr
        match node_w.n:
            case Program():
                # Recursive call to visit the children of the node
                return self.program(node_w)
            case Assignment():
                return self.assign(node_w)
            case BinaryOp():
                return self.bin_op(node_w)
            case DerefOp():
                return self.deref_op(node_w)
            case AddressOfOp():
                return self.addressof_op(node_w)
            case UnaryOp():
                return self.un_op(node_w)
            case CastOp():
                return self.cast_op(node_w)
            case CompoundStatement():
                return self.compound_stmt(node_w)
            case FunctionDefinition():
                return self.func_def(node_w)
            case VariableDeclaration():
                return self.variable_decl(node_w)
            case Literal():
                return self.lit(node_w)
            case Identifier():
                return self.identifier(node_w)
            case PrintStatement():
                return self.print(node_w)
            case Enumeration():
                return self.enum(node_w)
            case SwitchStatement():
                return self.switch(node_w)
            case ConditionalStatement():
                return self.conditional(node_w)
            case IterationStatement():
                return self.iteration(node_w)
            case JumpStatement():
                return self.jump(node_w)
            case LabeledStatement():
                return self.labeled(node_w)

            case _:
                raise Exception

    
    def program(self, node_w: Wrapper[Program]):
        """Method called when encountering a Program node."""
        for child in node_w.n.children:
            self.visit(child)
    def labeled(self, node_w: Wrapper[LabeledStatement]):
        if node_w.n.expr_w is not None:
            self.visit(node_w.n.expr_w)
        for statement_w in node_w.n.body:
            self.visit(statement_w)
    def jump(self, node_w: Wrapper[JumpStatement]):
        pass

    def switch(self, node_w: Wrapper[SwitchStatement]):
        self.visit(node_w.n.value_w)
        for condition_w in node_w.n.conditions:
            self.visit(condition_w)
        for branch_w in node_w.n.branches:
            self.visit(branch_w)

    def conditional(self, node_w: Wrapper[ConditionalStatement]):
        self.visit(node_w.n.condition_w)
        self.visit(node_w.n.true_branch_w)
        if node_w.n.false_branch_w is not None:
            self.visit(node_w.n.false_branch_w)

    def iteration(self, node_w: Wrapper[IterationStatement]):
        if node_w.n.adv_w is not None:
            self.visit(node_w.n.adv_w)
        self.visit(node_w.n.condition_w)
        self.visit(node_w.n.body_w)

    def enum(self, node_w: Wrapper[Enumeration]):
        pass
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

    def cast_op(self, node_w: Wrapper[CastOp]):
        self.visit(node_w.n.expression_w)

    
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

    def print(self, node_w: Wrapper[PrintStatement]):
        self.visit(node_w.n.argument_w)



