from src.antlr_files.C_ExpressionsVisitor import *

class MainVisitor(C_ExpressionsVisitor):
    # Visit a parse tree produced by C_ExpressionsParser#statement.
    def visitStatement(self, ctx: C_ExpressionsParser.StatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#exprStatement.
    def visitExprStatement(self, ctx: C_ExpressionsParser.ExprStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#expr.
    def visitExpr(self, ctx: C_ExpressionsParser.ExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#constantExpr.
    def visitConstantExpr(self, ctx: C_ExpressionsParser.ConstantExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#conditionalExpr.
    def visitConditionalExpr(self, ctx: C_ExpressionsParser.ConditionalExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#logicalOrExpr.
    def visitLogicalOrExpr(self, ctx: C_ExpressionsParser.LogicalOrExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#logicalAndExpr.
    def visitLogicalAndExpr(self, ctx: C_ExpressionsParser.LogicalAndExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#bitwiseOrExpr.
    def visitBitwiseOrExpr(self, ctx: C_ExpressionsParser.BitwiseOrExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#logicalXorExpr.
    def visitLogicalXorExpr(self, ctx: C_ExpressionsParser.LogicalXorExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#bitwiseAndExpr.
    def visitBitwiseAndExpr(self, ctx: C_ExpressionsParser.BitwiseAndExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#equalityExpr.
    def visitEqualityExpr(self, ctx: C_ExpressionsParser.EqualityExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#relationalExpr.
    def visitRelationalExpr(self, ctx: C_ExpressionsParser.RelationalExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#shiftExpr.
    def visitShiftExpr(self, ctx: C_ExpressionsParser.ShiftExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#addExpr.
    def visitAddExpr(self, ctx: C_ExpressionsParser.AddExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#multExpr.
    def visitMultExpr(self, ctx: C_ExpressionsParser.MultExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#unaryExpr.
    def visitUnaryExpr(self, ctx: C_ExpressionsParser.UnaryExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#unaryOperator.
    def visitUnaryOperator(self, ctx: C_ExpressionsParser.UnaryOperatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#constant.
    def visitConstant(self, ctx: C_ExpressionsParser.ConstantContext):
        return self.visitChildren(ctx)


