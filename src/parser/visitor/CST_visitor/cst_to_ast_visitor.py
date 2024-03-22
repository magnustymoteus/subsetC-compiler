from src.antlr_files.C_GrammarVisitor import *
from src.antlr_files.C_GrammarParser import *
from src.parser.AST import *


class CSTToASTVisitor(C_GrammarVisitor):
    def visitTypeSpec(self, ctx: C_GrammarParser.TypeSpecContext):
        # returns for example "int"
        return ctx.getChild(0).getText()

    def visitFunctionDef(self, ctx: C_GrammarParser.FunctionDefContext):
        # TODO complete this in the future: patryk
        # visits the last child node of the current context
        # ctx.getChild(ctx.getChildCount()-1) e.g. compoundStmtContext
        return self.visit(ctx.getChild(ctx.getChildCount() - 1))

    def visitPostfixExpr(self, ctx: C_GrammarParser.PostfixExprContext):
        if ctx.getChildCount() > 1:
            result = wrap(UnaryOp(ctx.getChild(1).getChild(0).getText(), True))
            result.n.set_line_col_nr(ctx.start.line, ctx.start.column)
            result.n.operand_w = self.visit(ctx.getChild(0))
            return result
        return self.visit(ctx.getChild(0))

    def visitDeclaration(self, ctx: C_GrammarParser.DeclarationContext):
        type_specifier = self.visit(ctx.getChild(0))
        declarator_result = self.visit(ctx.getChild(1))
        identifier_node = declarator_result[0]

        result: Wrapper[VariableDeclaration] = wrap(VariableDeclaration(identifier_node.n.name, type_specifier))
        result.n.set_line_col_nr(ctx.start.line, ctx.start.column)
        result.n.definition_w = declarator_result[1]
        return result

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
            result.n.set_line_col_nr(ctx.start.line, ctx.start.column)
            result.n.expression_w = expr_w
            return result
        return self.visitChildren(ctx)

    def visitDeclarationSpec(self, ctx: C_GrammarParser.DeclarationSpecContext):
        type_specifier = None
        is_constant = False
        ptr_count = 0
        const_ptrs = []
        for child in ctx.getChildren():
            if isinstance(child, C_GrammarParser.TypeQualContext):
                is_constant = True
            elif isinstance(child, C_GrammarParser.TypeSpecContext):
                type_specifier = self.visit(child)
            elif isinstance(child, C_GrammarParser.PointerContext):
                if child.getChildCount() > 1:
                    const_ptrs.append(ptr_count)
                ptr_count += 1
        return PrimitiveType(type_specifier, is_constant, ptr_count, const_ptrs)

    def visitExprStmt(self, ctx: C_GrammarParser.ExprStmtContext):
        return self.visit(ctx.getChild(0))

    def visitCompoundStmt(self, ctx: C_GrammarParser.CompoundStmtContext):
        statement_list = []
        for child in ctx.children:
            if not (child.getText() in ['{', '}']):
                statement_list.append(self.visit(child))
        result = wrap(CompoundStatement())
        result.n.set_line_col_nr(ctx.start.line, ctx.start.column)
        result.n.statements = statement_list
        return result

    def visitAssignmentExpr(self, ctx: C_GrammarParser.AssignmentOpContext):
        if ctx.getChildCount() == 1:
            return self.visitChildren(ctx)
        node: Wrapper[Assignment] = wrap(Assignment(ctx.getChild(1).getText()))
        node.n.set_line_col_nr(ctx.start.line, ctx.start.column)
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
        node.n.set_line_col_nr(ctx.start.line, ctx.start.column)
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
        program_node.n.set_line_col_nr(ctx.start.line, ctx.start.column)
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
            node.n.set_line_col_nr(ctx.start.line, ctx.start.column)
            return node
        return self.visitChildren(ctx)

    def visitCharLiteral(self, ctx: C_GrammarParser.CharLiteralContext):
        char_value = ctx.getChild(0).getText()[1:-1].encode('utf-8').decode('unicode_escape')
        node: Wrapper[CharLiteral] = wrap(CharLiteral(char_value))
        node.n.set_line_col_nr(ctx.start.line, ctx.start.column)
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
        node.n.set_line_col_nr(ctx.start.line, ctx.start.column)
        return node

    def visitIdentifier(self, ctx: C_GrammarParser.IdentifierContext):
        node: Wrapper[Identifier] = wrap(Identifier(ctx.getChild(0).getText()))
        node.n.set_line_col_nr(ctx.start.line, ctx.start.column)
        return node

    def visitParenExpr(self, ctx: C_GrammarParser.ParenExprContext):
        return self.visit(ctx.getChild(1))

    def visitBlockItem(self, ctx: C_GrammarParser.StmtContext):
        return self.visit(ctx.getChild(0))
