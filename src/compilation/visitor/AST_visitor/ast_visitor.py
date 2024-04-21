from src.constructs import *
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
        warnings.warn(f"{self.current_line_nr}:{self.current_col_nr}:warning: {message}")

    def visit(self, node_w: Wrapper[Basic]):
        """
        Visit method to traverse the AST nodes.

        Args:
            node_w (Wrapper[Basic]): The AST node wrapper.

        Raises:
            Exception: If an unknown node type is encountered.

        Returns:
            None
        """
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
            case FunctionDeclaration():
                return self.func_decl(node_w)
            case VariableDeclaration():
                return self.variable_decl(node_w)
            case ArrayLiteral():
                return self.array_lit(node_w)
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
            case ReturnStatement():
                return self.return_stmt(node_w)
            case JumpStatement():
                return self.jump(node_w)
            case LabeledStatement():
                return self.labeled(node_w)
            case FunctionCall():
                return self.func_call(node_w)
            case ArrayAccess():
                return self.array_access(node_w)
            case _:
                raise Exception

    def program(self, node_w: Wrapper[Program]):
        """
        Method called when encountering a Program node.

        Args:
            node_w (Wrapper[Program]): The Program node wrapper.

        Returns:
            None
        """
        for child in node_w.n.children:
            self.visit(child)

    def labeled(self, node_w: Wrapper[LabeledStatement]):
        """
        Method called when encountering a LabeledStatement node.

        Args:
            node_w (Wrapper[LabeledStatement]): The LabeledStatement node wrapper.

        Returns:
            None
        """
        if node_w.n.expr_w is not None:
            self.visit(node_w.n.expr_w)
        for statement_w in node_w.n.body:
            self.visit(statement_w)

    def return_stmt(self, node_w: Wrapper[ReturnStatement]):
        if node_w.n.expr_w is not None:
            self.visit(node_w.n.expr_w)
    def array_access(self, node_w: Wrapper[ArrayAccess]):
        self.visit(node_w.n.identifier_w)
        for index_w in node_w.n.indices:
            self.visit(index_w)

    def func_call(self, node_w: Wrapper[FunctionCall]):
        for arg_w in node_w.n.arguments:
            self.visit(arg_w)

    def jump(self, node_w: Wrapper[JumpStatement]):
        """
        Method called when encountering a JumpStatement node.

        Args:
            node_w (Wrapper[JumpStatement]): The JumpStatement node wrapper.

        Returns:
            None
        """
        pass

    def switch(self, node_w: Wrapper[SwitchStatement]):
        """
        Method called when encountering a SwitchStatement node.

        Args:
            node_w (Wrapper[SwitchStatement]): The SwitchStatement node wrapper.

        Returns:
            None
        """
        self.visit(node_w.n.value_w)
        for condition_w in node_w.n.conditions:
            self.visit(condition_w)
        for branch_w in node_w.n.branches:
            self.visit(branch_w)

    def conditional(self, node_w: Wrapper[ConditionalStatement]):
        """
        Method called when encountering a ConditionalStatement node.

        Args:
            node_w (Wrapper[ConditionalStatement]): The ConditionalStatement node wrapper.

        Returns:
            None
        """
        self.visit(node_w.n.condition_w)
        self.visit(node_w.n.true_branch_w)
        if node_w.n.false_branch_w is not None:
            self.visit(node_w.n.false_branch_w)

    def iteration(self, node_w: Wrapper[IterationStatement]):
        """
        Method called when encountering an IterationStatement node.

        Args:
            node_w (Wrapper[IterationStatement]): The IterationStatement node wrapper.

        Returns:
            None
        """
        if node_w.n.adv_w is not None:
            self.visit(node_w.n.adv_w)
        self.visit(node_w.n.condition_w)
        self.visit(node_w.n.body_w)

    def enum(self, node_w: Wrapper[Enumeration]):
        """
        Method called when encountering an Enumeration node.

        Args:
            node_w (Wrapper[Enumeration]): The Enumeration node wrapper.

        Returns:
            None
        """
        pass

    def bin_op(self, node_w: Wrapper[BinaryOp]):
        """
        Method called when encountering a BinaryOp node.

        Args:
            node_w (Wrapper[BinaryOp]): The BinaryOp node wrapper.

        Returns:
            None
        """
        self.visit(node_w.n.lhs_w)
        self.visit(node_w.n.rhs_w)

    def deref_op(self, node_w: Wrapper[DerefOp]):
        """
        Method called when encountering a DerefOp node.

        Args:
            node_w (Wrapper[DerefOp]): The DerefOp node wrapper.

        Returns:
            None
        """
        self.un_op(node_w)

    def addressof_op(self, node_w: Wrapper[AddressOfOp]):
        """
        Method called when encountering an AddressOfOp node.

        Args:
            node_w (Wrapper[AddressOfOp]): The AddressOfOp node wrapper.

        Returns:
            None
        """
        self.un_op(node_w)

    def un_op(self, node_w: Wrapper[UnaryOp]):
        """
        Method called when encountering a UnaryOp node.

        Args:
            node_w (Wrapper[UnaryOp]): The UnaryOp node wrapper.

        Returns:
            None
        """
        self.visit(node_w.n.operand_w)

    def cast_op(self, node_w: Wrapper[CastOp]):
        """
        Method called when encountering a CastOp node.

        Args:
            node_w (Wrapper[CastOp]): The CastOp node wrapper.

        Returns:
            None
        """
        self.visit(node_w.n.expression_w)

    def array_lit(self, node_w: Wrapper[ArrayLiteral]):
        for elem_w in node_w.n.value:
            self.visit(elem_w)
    def lit(self, node_w: Wrapper[Literal]):
        """
        Method called when encountering a Literal node.

        Args:
            node_w (Wrapper[Literal]): The Literal node wrapper.

        Returns:
            None
        """
        pass

    def assign(self, node_w: Wrapper[Assignment]):
        """
        Method called when encountering an Assignment node.

        Args:
            node_w (Wrapper[Assignment]): The Assignment node wrapper.

        Returns:
            None
        """
        self.visit(node_w.n.assignee_w)
        self.visit(node_w.n.value_w)

    def identifier(self, node_w: Wrapper[Identifier]):
        """
        Method called when encountering an Identifier node.

        Args:
            node_w (Wrapper[Identifier]): The Identifier node wrapper.

        Returns:
            None
        """
        pass

    def compound_stmt(self, node_w: Wrapper[CompoundStatement]):
        """
        Method called when encountering a CompoundStatement node.

        Args:
            node_w (Wrapper[CompoundStatement]): The CompoundStatement node wrapper.

        Returns:
            None
        """
        for statement in node_w.n.statements:
            self.visit(statement)

    def func_decl(self, node_w: Wrapper[FunctionDeclaration]):
        """
        Method called when encountering a FunctionDeclaration node.

        Args:
            node_w (Wrapper[FunctionDeclaration]): The FunctionDeclaration node wrapper.

        Returns:
            None
        """
        for param_w in node_w.n.parameters:
            self.visit(param_w)
        if node_w.n.body_w.n is not None:
            self.visit(node_w.n.body_w)

    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        """
        Method called when encountering a VariableDeclaration node.

        Args:
            node_w (Wrapper[VariableDeclaration]): The VariableDeclaration node wrapper.

        Returns:
            None
        """
        if node_w.n.definition_w.n is not None:
            self.visit(node_w.n.definition_w)

    def print(self, node_w: Wrapper[PrintStatement]):
        """
        Method called when encountering a PrintStatement node.

        Args:
            node_w (Wrapper[PrintStatement]): The PrintStatement node wrapper.

        Returns:
            None
        """
        self.visit(node_w.n.argument_w)
