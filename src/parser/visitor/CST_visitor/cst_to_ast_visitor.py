from src.antlr_files.C_GrammarVisitor import *
from src.antlr_files.C_GrammarParser import *
from src.parser.AST import *

class CSTToASTVisitor(C_GrammarVisitor):
    def visitFirstMatch(self, ctx, match_type):
        if isinstance(match_type, list):
            return next((self.visit(child) for child in ctx.getChildren() if type(child) in match_type), None)
        return next((self.visit(child) for child in ctx.getChildren() if isinstance(child, match_type)), None)
    def visitAllMatches(self, ctx, match_type):
        if isinstance(match_type, list):
            return [self.visit(child) for child in ctx.getChildren() if type(child) in match_type]
        return [self.visit(child) for child in ctx.getChildren() if isinstance(child, match_type)]
    def __init__(self, tokens):
        super().__init__()
        self.tokens = tokens
        self.processed_indices = set()

    def get_comments_for_ctx(self, ctx):
        token_stream = self.tokens.getHiddenTokensToLeft(ctx.start.tokenIndex)
        if token_stream:
            result = [token.text for token in token_stream if token.tokenIndex not in self.processed_indices]
            self.processed_indices = self.processed_indices.union({token.tokenIndex for token in token_stream})
            return result
        return []

    def attach_comments(self, ast_node_w, ctx):
        ast_node_w.n.comments += self.get_comments_for_ctx(ctx)
        ast_node_w.n.source_code_line = ctx.getText()

    def visit(self, tree):
        result = super().visit(tree)
        if isinstance(result, Wrapper):
            self.attach_comments(result, tree)
            result.n.set_line_col_nr(tree.start.line, tree.start.column)
        return result
    def visitSelectionStmt(self, ctx:C_GrammarParser.SelectionStmtContext):
        expr_w: Wrapper[Expression] = self.visitFirstMatch(ctx, C_GrammarParser.ExprContext)
        compound_or_selection_stmts = self.visitAllMatches(ctx, [C_GrammarParser.CompoundStmtContext, C_GrammarParser.SelectionStmtContext])
        match ctx.getChild(0).getText():
            case 'if':
                false_branch_w = compound_or_selection_stmts[1] if len(compound_or_selection_stmts) == 2 else None
                return wrap(SelectionStatement([expr_w], [compound_or_selection_stmts[0]], false_branch_w))
            case 'switch':
                labeled_stmts: list[Wrapper[LabeledStatement]] = self.visitAllMatches(ctx, C_GrammarParser.LabeledStmtContext)
                conditions = [wrap(BinaryOp('==', expr_w, child.n.expr_w)) for child in labeled_stmts if child.n.label == "case"]
                defaults = [wrap(CompoundStatement(child.n.body)) for child in labeled_stmts if child.n.label == "default"]
                cases = [wrap(CompoundStatement(child.n.body)) for child in labeled_stmts if child.n.label == "case"]
                return wrap(SelectionStatement(conditions, cases, None if not len(defaults) else defaults[0]))
            case _:
                raise ValueError("Unexpected selection statement")

    def visitJumpStmt(self, ctx:C_GrammarParser.JumpStmtContext):
        return wrap(JumpStatement(ctx.getChild(0).getText()))
    def visitLabeledStmt(self, ctx:C_GrammarParser.LabeledStmtContext):
        return wrap(LabeledStatement(ctx.getChild(0).getText(), self.visitAllMatches(ctx, C_GrammarParser.BlockItemContext),
                                self.visitFirstMatch(ctx, C_GrammarParser.ConstantExprContext)))

    def visitIterationStmt(self, ctx: C_GrammarParser.IterationStmtContext):
        body_w: Wrapper[CompoundStatement] = self.visitFirstMatch(ctx, C_GrammarParser.CompoundStmtContext)
        match ctx.getChild(0).getText():
            case 'for':
                elements = self.visitFirstMatch(ctx, C_GrammarParser.ForConditionContext)
                result: CompoundStatement = CompoundStatement()
                if elements[0] is not None:
                    result.statements.append(elements[0])
                condition_w: Wrapper[Expression] = elements[1] if elements[1] is not None else wrap(IntLiteral(1))
                if elements[2] is not None:
                    body_w.n.statements.append(elements[2])
                result.statements.append(wrap(IterationStatement(condition_w, body_w)))
                return wrap(result)
            case 'while':
                condition_w: Wrapper[Expression] = self.visitFirstMatch(ctx, C_GrammarParser.ExprContext)
                return wrap(IterationStatement(condition_w, body_w))
            case _:
                raise ValueError("Unexpected iteration statement")

    def visitForCondition(self, ctx:C_GrammarParser.ForConditionContext):
        elements: list[Wrapper[Expression | VariableDeclaration] | None] = [None, None, None] # [initialization, condition, advancement]
        i: int = 0
        for child in ctx.getChildren():
            if isinstance(child, TerminalNode):
                i += 1
            else:
                elements[i] = self.visit(child)
        return elements

    def visitFunctionDef(self, ctx: C_GrammarParser.FunctionDefContext):
        # TODO complete this in the future: patryk
        # visits the last child node of the current context
        # ctx.getChild(ctx.getChildCount()-1) e.g. compoundStmtContext
        return self.visit(ctx.getChild(ctx.getChildCount() - 1))

    def visitPrintfStmt(self, ctx: C_GrammarParser.PrintfStmtContext):
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
        if ctx.getChildCount() > 1:
            result = wrap(UnaryOp(ctx.getChild(1).getChild(0).getText(), True))

            result.n.operand_w = self.visit(ctx.getChild(0))
            return result
        return self.visit(ctx.getChild(0))
    def visitEnumSpec(self, ctx:C_GrammarParser.EnumSpecContext):
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
        return self.visitDeclaration(ctx)
    def visitDeclarationSpec(self, ctx: C_GrammarParser.DeclarationSpecContext):
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
