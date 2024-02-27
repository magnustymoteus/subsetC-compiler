from src.antlr_files.C_GrammarVisitor import *
from src.antlr_files.C_GrammarParser import *
from src.parser.ast import Ast
from src.parser.node import *


class CSTToASTVisitor(C_GrammarVisitor):
    def visitBinaryOp(self, ctx: ParserRuleContext):
        if ctx.getChildCount() == 3:
            node: Wrapper[BinaryOp] = wrap(
                BinaryOp(ctx.getChild(1).getText()))
            left = self.visit(ctx.getChild(0))
            right = self.visit(ctx.getChild(2))
            node.n.lhs_w = left
            node.n.rhs_w = right
            return node
        return self.visitChildren(ctx)

    def visit(self, tree):
        return super().visit(tree)

    def visitProgram(self, ctx: C_GrammarParser.ProgramContext):
        statements = []
        for i in range(0, ctx.getChildCount()):
            if ctx.getChild(i).getChildCount() == 2:
                statements.append(self.visit(ctx.getChild(i)))
        program_node = wrap(Program(statements))
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

    def visitLiteral(self, ctx: C_GrammarParser.LiteralContext):
        node: Wrapper[IntLiteral] = wrap(IntLiteral(
            int(ctx.getChild(0).getText())))  # TODO: delete the int cast and do better
        return node

    def visitParenExpr(self, ctx: C_GrammarParser.ParenExprContext):
        return self.visit(ctx.getChild(1))

    def visitStmt(self, ctx: C_GrammarParser.StmtContext):
        return self.visit(ctx.getChild(0))
