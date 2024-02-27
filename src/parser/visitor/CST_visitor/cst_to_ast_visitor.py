from src.antlr_files.C_GrammarVisitor import *
from src.antlr_files.C_GrammarParser import *
from src.parser.ast import Ast
from src.parser.node import *
from src.symbol_table import *

class CSTToASTVisitor(C_GrammarVisitor):
    def visitTypeSpec(self, ctx:C_GrammarParser.TypeSpecContext):
        return PrimitiveType(ctx.getChild(0).getText())
    def visitFunctionDef(self, ctx: C_GrammarParser.FunctionDefContext):
        # TODO complete this in the future: patryk
#        return_type: SymbolType = self.visit(ctx.getChild())
        #return wrap(CompoundStatement(ctx.getChild(0)))
        return self.visit(ctx.getChild(ctx.getChildCount()-1))
    def visitPostfixExpr(self, ctx:C_GrammarParser.PostfixExprContext):
        if ctx.getChildCount() > 1:
            return wrap(Basic())
        return self.visitChildren(ctx)
    def visitDeclaration(self, ctx:C_GrammarParser.DeclarationContext):
        ctx.removeLastChild()
        # TODO soon: patryk
        #return wrap(VariableDeclaration(self.visit())
        pass

    def visitDeclarationSpec(self, ctx:C_GrammarParser.DeclarationSpecContext):
        # TODO soon: patryk
        pass

    def visitExprStmt(self, ctx:C_GrammarParser.ExprStmtContext):
        return self.visit(ctx.getChild(0))

    def visitCompoundStmt(self, ctx:C_GrammarParser.CompoundStmtContext):
        statement_list = []
        for child in ctx.children:
            if not (child.getText() in ['{', '}']):
                statement_list.append(self.visit(child))
        return wrap(CompoundStatement(statement_list))

    def visitAssignmentExpr(self, ctx:C_GrammarParser.AssignmentOpContext):
        return self.visitBinaryOp(ctx)

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
        ctx.removeLastChild()
        children = [self.visit(child) for child in ctx.getChildren()]
        program_node = wrap(Program(children))
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
            node: Wrapper[UnaryOp] = wrap(
                UnaryOp(ctx.getChild(0).getText()))
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
        return node
    def visitFloatLiteral(self, ctx:C_GrammarParser.FloatLiteralContext):
        node: Wrapper[FloatLiteral] = wrap(FloatLiteral(
            float(ctx.getChild(0).getText())))
        return node

    def visitIdentifier(self, ctx:C_GrammarParser.IdentifierContext):
        node: Wrapper[Identifier] = wrap(Identifier(ctx.getChild(0).getText()))
        return node

    def visitParenExpr(self, ctx: C_GrammarParser.ParenExprContext):
        return self.visit(ctx.getChild(1))

    def visitStmt(self, ctx: C_GrammarParser.StmtContext):
        return self.visit(ctx.getChild(0))
