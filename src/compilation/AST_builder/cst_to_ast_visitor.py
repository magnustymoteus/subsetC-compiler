from src.antlr_files.C_GrammarVisitor import *
from src.antlr_files.C_GrammarParser import *
from src.constructs import *

class CSTToASTVisitor(C_GrammarVisitor):
    """
    This class represents a visitor that converts a Concrete Syntax Tree (CST) to an Abstract Syntax Tree (AST).
    It inherits from the C_GrammarVisitor class.
    """

    def visitFirstMatch(self, ctx, match_type):
        """
        Visits the first child node of the given context that matches the specified type.

        Args:
            ctx: The context node to visit.
            match_type: The type of the child node to match.

        Returns:
            The result of visiting the first matching child node, or None if no matching child node is found.
        """
        if isinstance(match_type, list):
            return next((self.visit(child) for child in ctx.getChildren() if type(child) in match_type), None)
        return next((self.visit(child) for child in ctx.getChildren() if isinstance(child, match_type)), None)

    def visitAllMatches(self, ctx, match_type):
        """
        Visits all child nodes of the given context that match the specified type.

        Args:
            ctx: The context node to visit.
            match_type: The type of the child nodes to match.

        Returns:
            A list of results from visiting the matching child nodes.
        """
        if isinstance(match_type, list):
            return [self.visit(child) for child in ctx.getChildren() if type(child) in match_type]
        return [self.visit(child) for child in ctx.getChildren() if isinstance(child, match_type)]

    def __init__(self, tokens):
        """
        Initializes the CSTToASTVisitor object.

        Args:
            tokens: The token stream associated with the CST.
        """
        super().__init__()
        self.tokens = tokens
        self.processed_indices = set()

    def get_comments_for_ctx(self, ctx):
        """
        Retrieves the comments associated with the given context node.

        Args:
            ctx: The context node.

        Returns:
            A list of comments associated with the context node.
        """
        token_stream = self.tokens.getHiddenTokensToLeft(ctx.start.tokenIndex)
        if token_stream:
            result = [token.text for token in token_stream if token.tokenIndex not in self.processed_indices]
            self.processed_indices = self.processed_indices.union({token.tokenIndex for token in token_stream})
            return result
        return []

    def attach_comments(self, ast_node_w, ctx):
        """
        Attaches the comments associated with the given context node to the corresponding AST node.

        Args:
            ast_node_w: The wrapper object representing the AST node.
            ctx: The context node.
        """
        ast_node_w.n.comments += self.get_comments_for_ctx(ctx)
        ast_node_w.n.source_code_line = ctx.parser.getInputStream().getText(ctx.start, ctx.stop)

    def visit(self, tree):
        """
        Visits the given tree and returns the result of the visit.

        Args:
            tree: The tree to visit.

        Returns:
            The result of the visit.
        """
        result = super().visit(tree)
        if isinstance(result, Wrapper):
            self.attach_comments(result, tree)
            result.n.set_line_col_nr(tree.start.line, tree.start.column)
        return result

    def visitSelectionStmt(self, ctx:C_GrammarParser.SelectionStmtContext):
        """
        Visits the given selection statement context and converts it to an AST node.

        Args:
            ctx: The selection statement context.

        Returns:
            The AST node representing the selection statement.
        """
        expr_w: Wrapper[Expression] = self.visitFirstMatch(ctx, C_GrammarParser.ExprContext)
        compound_or_selection_stmts = self.visitAllMatches(ctx, [C_GrammarParser.CompoundStmtContext, C_GrammarParser.SelectionStmtContext])
        match ctx.getChild(0).getText():
            case 'if':
                false_branch_w = compound_or_selection_stmts[1] if len(compound_or_selection_stmts) == 2 else None
                expr_w = wrap(BinaryOp("!=", expr_w, wrap(IntLiteral(0))))
                return wrap(ConditionalStatement(expr_w, compound_or_selection_stmts[0], false_branch_w))
            case 'switch':
                labeled_stmts: list[Wrapper[LabeledStatement]] = self.visitAllMatches(ctx, C_GrammarParser.LabeledStmtContext)
                conditions = [child.n.expr_w for child in labeled_stmts if child.n.expr_w is not None]

                defaults = [labeled_stmts.index(child) for child in labeled_stmts if child.n.label == "default"]
                default_index = defaults[0] if len(defaults) != 0 else None

                bodies = [wrap(CompoundStatement(child.n.body)) for child in labeled_stmts]

                return wrap(SwitchStatement(expr_w, conditions, bodies, default_index))
            case _:
                raise ValueError("Unexpected selection statement")

    def visitJumpStmt(self, ctx:C_GrammarParser.JumpStmtContext):
        """
        Visits the given jump statement context and converts it to an AST node.

        Args:
            ctx: The jump statement context.

        Returns:
            The AST node representing the jump statement.
        """
        type: str = ctx.getChild(0).getText()
        match type:
            case "return":
                expr_w: Wrapper[Expression] | None = self.visitFirstMatch(ctx, C_GrammarParser.ExprContext)
                return wrap(ReturnStatement(expr_w))
            case _:
                return wrap(JumpStatement(type))

    def visitLabeledStmt(self, ctx:C_GrammarParser.LabeledStmtContext):
        """
        Visits the given labeled statement context and converts it to an AST node.

        Args:
            ctx: The labeled statement context.

        Returns:
            The AST node representing the labeled statement.
        """
        return wrap(LabeledStatement(ctx.getChild(0).getText(), self.visitAllMatches(ctx, C_GrammarParser.BlockItemContext),
                                self.visitFirstMatch(ctx, C_GrammarParser.ConstantExprContext)))

    def visitIterationStmt(self, ctx: C_GrammarParser.IterationStmtContext):
        """
        Visits the given iteration statement context and converts it to an AST node.

        Args:
            ctx: The iteration statement context.

        Returns:
            The AST node representing the iteration statement.
        """
        body_w: Wrapper[CompoundStatement] = self.visitFirstMatch(ctx, C_GrammarParser.CompoundStmtContext)
        match ctx.getChild(0).getText():
            case 'for':
                elements = self.visitFirstMatch(ctx, C_GrammarParser.ForConditionContext)
                result: CompoundStatement = CompoundStatement()
                if elements[0] is not None:
                    result.statements.append(elements[0])
                condition_w: Wrapper[Expression] = elements[1] if elements[1] is not None else wrap(IntLiteral(1))
                condition_w = wrap(BinaryOp("!=", condition_w, wrap(IntLiteral(0))))
                advancement_w = elements[2]
                result.statements.append(wrap(IterationStatement(condition_w, body_w, advancement_w)))
                return wrap(result)
            case 'while':
                condition_w: Wrapper[Expression] = self.visitFirstMatch(ctx, C_GrammarParser.ExprContext)
                condition_w = wrap(BinaryOp("!=", condition_w, wrap(IntLiteral(0))))
                return wrap(IterationStatement(condition_w, body_w))
            case _:
                raise ValueError("Unexpected iteration statement")

    def visitForCondition(self, ctx:C_GrammarParser.ForConditionContext):
        """
        Visits the given for condition context and returns the elements of the for condition.

        Args:
            ctx: The for condition context.

        Returns:
            A list of elements representing the for condition.
        """
        elements: list[Wrapper[Expression | VariableDeclaration] | None] = [None, None, None] # [initialization, condition, advancement]
        i: int = 0
        for child in ctx.getChildren():
            if isinstance(child, TerminalNode):
                i += 1
            else:
                elements[i] = self.visit(child)
        return elements

    def visitParameterList(self, ctx:C_GrammarParser.ParameterListContext):
        return self.visitAllMatches(ctx, C_GrammarParser.ParameterDeclarationContext)
    def visitParameterDeclaration(self, ctx:C_GrammarParser.ParameterDeclarationContext):
        return self.visitDeclaration(ctx)

    def visitFunctionCallExpr(self, ctx:C_GrammarParser.FunctionCallExprContext):
        func_name: str = ctx.getChild(0).getText()
        arguments: list[Wrapper[Expression]] = self.visitAllMatches(ctx, C_GrammarParser.AssignmentExprContext)
        return wrap(FunctionCall(func_name, arguments))

    def visitFunctionDef(self, ctx: C_GrammarParser.FunctionDefContext):
        """
        Visits the given function definition context and converts it to an AST node.

        Args:
            ctx: The function definition context.

        Returns:
            The AST node representing the function definition.
        """
        body_w: Wrapper[CompoundStatement] = self.visitFirstMatch(ctx, C_GrammarParser.CompoundStmtContext)
        function_name: str = self.visitFirstMatch(ctx, C_GrammarParser.IdentifierContext).n.name
        return_type: PrimitiveType = self.visitFirstMatch(ctx, C_GrammarParser.DeclarationSpecContext)[1]
        parameters: list[Wrapper[VariableDeclaration]] = self.visitFirstMatch(ctx, C_GrammarParser.ParameterListContext)
        if parameters is None:
            parameters = []
        result = FunctionDefinition(function_name, body_w, parameters)
        result.type = FunctionType(return_type, [parameter_w.n.type for parameter_w in parameters])
        return wrap(result)

    def visitPrintfStmt(self, ctx: C_GrammarParser.PrintfStmtContext):
        """
        Visits the given printf statement context and converts it to an AST node.

        Args:
            ctx: The printf statement context.

        Returns:
            The AST node representing the printf statement.
        """
        format: str = ""
        argument: Wrapper[Basic] | None = None
        for child in ctx.getChildren():
            match child:
                case C_GrammarParser.PrintfFormatContext():
                    format = child.getChild(0).getText()
                case C_GrammarParser.IdentifierContext():
                    argument = self.visit(child)
                case C_GrammarParser.LiteralContext():
                    argument = self.visit(child)
        return wrap(PrintStatement(format, argument))

    def visitPostfixExpr(self, ctx: C_GrammarParser.PostfixExprContext):
        """
        Visits the given postfix expression context and converts it to an AST node.

        Args:
            ctx: The postfix expression context.

        Returns:
            The AST node representing the postfix expression.
        """
        if ctx.getChildCount() > 1:
            result = wrap(UnaryOp(ctx.getChild(1).getChild(0).getText(), True))

            result.n.operand_w = self.visit(ctx.getChild(0))
            return result
        return self.visit(ctx.getChild(0))

    def visitEnumSpec(self, ctx:C_GrammarParser.EnumSpecContext):
        """
        Visits the given enum specification context and converts it to an AST node.

        Args:
            ctx: The enum specification context.

        Returns:
            The AST node representing the enum specification.
        """
        is_enum_definition: bool = False
        labels: list[Wrapper[Identifier]] = []
        identifier = None
        for child in ctx.getChildren():
            visitedChild = self.visit(child)
            match child:
                case C_GrammarParser.IdentifierContext():
                    identifier = visitedChild
                case C_GrammarParser.EnumContext():
                    is_enum_definition = True
                    labels.append(visitedChild.n.name)
        if is_enum_definition:
            return wrap(Enumeration(identifier.n.name, labels))
        return identifier.n.name

    def visitPointer(self, ctx:C_GrammarParser.PointerContext):
        """
        Visits the given pointer context and returns the pointer count and constant pointers.

        Args:
            ctx: The pointer context.

        Returns:
            A tuple containing the pointer count and a list of constant pointers.
        """
        ptr_count: int = 0
        const_ptrs: list[int] = []
        for child in ctx.getChildren():
            match child.getText():
                case '*':
                    ptr_count += 1
                case 'const':
                    const_ptrs.append(ptr_count-1)
        return ptr_count, const_ptrs

    def visitDeclaration(self, ctx:C_GrammarParser.DeclarationContext):
        """
        Visits the given declaration context and converts it to an AST node.

        Args:
            ctx: The declaration context.

        Returns:
            The AST node representing the declaration.
        """
        declaration_spec = self.visit(ctx.getChild(0))
        declarator_result = self.visitFirstMatch(ctx, C_GrammarParser.DeclaratorContext)
        storage_class_specifier = declaration_spec[0]
        type_specifier = declaration_spec[1]
        if declarator_result is not None:
            identifier_node = declarator_result[0]
            result = VariableDeclaration(identifier_node.n.name, type_specifier, storage_class_specifier)
            result.definition_w = declarator_result[1]
            return wrap(result)
        elif isinstance(type_specifier.n, Enumeration):
            return type_specifier

    def visitForDeclaration(self, ctx:C_GrammarParser.ForDeclarationContext):
        """
        Visits the given for declaration context and converts it to an AST node.

        Args:
            ctx: The for declaration context.

        Returns:
            The AST node representing the for declaration.
        """
        return self.visitDeclaration(ctx)

    def visitDeclarationSpec(self, ctx: C_GrammarParser.DeclarationSpecContext):
        """
        Visits the given declaration specification context and returns the storage class specifier and type specifier.

        Args:
            ctx: The declaration specification context.

        Returns:
            A tuple containing the storage class specifier and the type specifier.
        """
        type_specifier = None
        is_constant = False
        ptr_count = 0
        const_ptrs = []
        storage_class_specifier: str | None = None
        for child in ctx.getChildren():
            visitedChild = self.visit(child)
            match child:
                case C_GrammarParser.TypeQualContext():
                    # assume its const (temporarily)
                    is_constant = True
                case C_GrammarParser.TypeSpecContext():
                    type_specifier = visitedChild
                    if isinstance(type_specifier, Wrapper):
                        return None, type_specifier
                case C_GrammarParser.PointerContext():
                    ptr_count = visitedChild[0]
                    const_ptrs = visitedChild[1]
                case C_GrammarParser.StorageClassSpecContext():
                    # assume its typedef (temporarily)
                    storage_class_specifier = child.getChild(0).getText()
        return storage_class_specifier, PrimitiveType(type_specifier, is_constant, ptr_count, const_ptrs)

    def visitTypeSpec(self, ctx:C_GrammarParser.TypeSpecContext):
        """
        Visits the given type specification context and converts it to an AST node.

        Args:
            ctx: The type specification context.

        Returns:
            The AST node representing the type specification.
        """
        visitedChild = self.visit(ctx.getChild(0))
        is_enum: bool = isinstance(ctx.getChild(0), C_GrammarParser.EnumSpecContext)
        return visitedChild if is_enum else ctx.getText()



    def visitDeclarator(self, ctx: C_GrammarParser.DeclaratorContext):
        if ctx.getChildCount() > 1:
            return self.visit(ctx.getChild(0)), self.visit(ctx.getChild(2))
        return self.visit(ctx.getChild(0)), wrap()

    def visitCastExpr(self, ctx: C_GrammarParser.CastExprContext):
        if ctx.getChildCount() > 1:
            target_type: PrimitiveType | None = None
            expr_w: Wrapper | None = None
            for i in range(0, ctx.getChildCount()):
                if isinstance(ctx.getChild(i), C_GrammarParser.TypeSpecContext):
                    target_type = PrimitiveType(self.visit(ctx.getChild(i)))
                if isinstance(ctx.getChild(i), C_GrammarParser.CastExprContext):
                    expr_w = self.visit(ctx.getChild(i))
            result: Wrapper[CastOp] = wrap(CastOp(target_type))

            result.n.expression_w = expr_w
            return result
        return self.visitChildren(ctx)


    def visitExprStmt(self, ctx: C_GrammarParser.ExprStmtContext):
        return self.visit(ctx.getChild(0))

    def visitCompoundStmt(self, ctx: C_GrammarParser.CompoundStmtContext):
        statement_list = []
        for child in ctx.children:
            if not (child.getText() in ['{', '}']):
                statement_list.append(self.visit(child))
        result = wrap(CompoundStatement())

        result.n.statements = statement_list
        return result

    def visitAssignmentExpr(self, ctx: C_GrammarParser.AssignmentOpContext):
        if ctx.getChildCount() == 1:
            return self.visitChildren(ctx)
        node: Wrapper[Assignment] = wrap(Assignment(ctx.getChild(1).getText()))

        left = self.visit(ctx.getChild(0))
        right = self.visit(ctx.getChild(2))
        node.n.assignee_w = left
        node.n.value_w = right
        return node

    def visitBinaryOp(self, ctx: ParserRuleContext):
        if ctx.getChildCount() == 1:
            return self.visitChildren(ctx)
        node: Wrapper[BinaryOp] = wrap(
            BinaryOp(ctx.getChild(1).getText()))

        left = self.visit(ctx.getChild(0))
        right = self.visit(ctx.getChild(2))
        node.n.lhs_w = left
        node.n.rhs_w = right
        return node

    def visitProgram(self, ctx: C_GrammarParser.ProgramContext):
        # remove EOF token
        ctx.removeLastChild()
        # iterates over every context(=child) and visits it
        children = [self.visit(child) for child in ctx.getChildren()]
        program_node = wrap(Program())

        program_node.n.children = children
        return program_node

    # Visit a parse tree produced by C_GrammarParser#logicalOrExpr.
    def visitLogicalOrExpr(self, ctx: C_GrammarParser.LogicalOrExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_GrammarParser#logicalAndExpr.
    def visitLogicalAndExpr(self, ctx: C_GrammarParser.LogicalAndExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_GrammarParser#bitwiseOrExpr.
    def visitBitwiseOrExpr(self, ctx: C_GrammarParser.BitwiseOrExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_GrammarParser#logicalXorExpr.
    def visitLogicalXorExpr(self, ctx: C_GrammarParser.LogicalXorExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_GrammarParser#bitwiseAndExpr.
    def visitBitwiseAndExpr(self, ctx: C_GrammarParser.BitwiseAndExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_GrammarParser#equalityExpr.
    def visitEqualityExpr(self, ctx: C_GrammarParser.EqualityExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_GrammarParser#shiftExpr.
    def visitShiftExpr(self, ctx: C_GrammarParser.ShiftExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_GrammarParser#addExpr.
    def visitAddExpr(self, ctx: C_GrammarParser.AddExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_GrammarParser#multExpr.
    def visitMultExpr(self, ctx: C_GrammarParser.MultExprContext):
        return self.visitBinaryOp(ctx)

    def visitRelationalExpr(self, ctx: C_GrammarParser.RelationalExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_GrammarParser#unaryExpr.
    def visitUnaryExpr(self, ctx: C_GrammarParser.UnaryExprContext):
        if ctx.getChildCount() == 2:
            match ctx.getChild(0).getText():
                case '*':
                    node = wrap(DerefOp())
                case '&':
                    node = wrap(AddressOfOp())
                case _:
                    node = wrap(UnaryOp(ctx.getChild(0).getText()))
            node.n.operand_w = self.visit(ctx.getChild(1))

            return node
        return self.visitChildren(ctx)

    def visitCharLiteral(self, ctx: C_GrammarParser.CharLiteralContext):
        char_value = ctx.getChild(0).getText()[1:-1].encode('utf-8').decode('unicode_escape')
        node: Wrapper[CharLiteral] = wrap(CharLiteral(char_value))

        return node

    def visitIntLiteral(self, ctx: C_GrammarParser.IntLiteralContext):
        node: Wrapper[IntLiteral] = wrap(IntLiteral(
            int(ctx.getChild(0).getText())))
        node.n.line_nr = ctx.start.line
        node.n.col_nr = ctx.start.column
        return node

    def visitFloatLiteral(self, ctx: C_GrammarParser.FloatLiteralContext):
        node: Wrapper[FloatLiteral] = wrap(FloatLiteral(
            float(ctx.getChild(0).getText())))

        return node

    def visitIdentifier(self, ctx: C_GrammarParser.IdentifierContext):
        node: Wrapper[Identifier] = wrap(Identifier(ctx.getChild(0).getText()))

        return node

    def visitBlockItem(self, ctx: C_GrammarParser.StmtContext):
        return self.visit(ctx.getChild(0))

    def visitPrimaryExpr(self, ctx:C_GrammarParser.PrimaryExprContext):
        for child in ctx.getChildren():
            if not isinstance(child, TerminalNode):
                return self.visit(child)
