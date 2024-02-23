from src.antlr_files.C_ExpressionsVisitor import *
from src.antlr_files.C_ExpressionsParser import *
from src.parser.AST import *


class CSTToASTVisitor(C_ExpressionsVisitor):
    def visitBinaryOp(self, ctx: ParserRuleContext):
        if ctx.getChildCount() == 3:
            node: NodeWrapper[AstBinOpNode] = wrap(AstBinOpNode(ctx.getChild(1).getText()))
            left = self.visit(ctx.getChild(0))
            right = self.visit(ctx.getChild(2))
            node.n.lhs_w = left
            node.n.rhs_w = right
            return node
        return self.visitChildren(ctx)

    def visit(self, tree):
        return super().visit(tree)

    def visitProgram(self, ctx: C_ExpressionsParser.ProgramContext):
        statements = []
        for i in range(0, ctx.getChildCount()):
            if ctx.getChild(i).getChildCount() == 2:
                statements.append(self.visit(ctx.getChild(i)))
        program_node = wrap(AstProgramNode(statements))
        return program_node

    # Visit a parse tree produced by C_ExpressionsParser#logicalOrExpr.
    def visitLogicalOrExpr(self, ctx: C_ExpressionsParser.LogicalOrExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#logicalAndExpr.
    def visitLogicalAndExpr(self, ctx: C_ExpressionsParser.LogicalAndExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#bitwiseOrExpr.
    def visitBitwiseOrExpr(self, ctx: C_ExpressionsParser.BitwiseOrExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#logicalXorExpr.
    def visitLogicalXorExpr(self, ctx: C_ExpressionsParser.LogicalXorExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#bitwiseAndExpr.
    def visitBitwiseAndExpr(self, ctx: C_ExpressionsParser.BitwiseAndExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#equalityExpr.
    def visitEqualityExpr(self, ctx: C_ExpressionsParser.EqualityExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#shiftExpr.
    def visitShiftExpr(self, ctx: C_ExpressionsParser.ShiftExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#addExpr.
    def visitAddExpr(self, ctx: C_ExpressionsParser.AddExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#multExpr.
    def visitMultExpr(self, ctx: C_ExpressionsParser.MultExprContext):
        return self.visitBinaryOp(ctx)

    def visitRelationalExpr(self, ctx: C_ExpressionsParser.RelationalExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#unaryExpr.
    def visitUnaryExpr(self, ctx: C_ExpressionsParser.UnaryExprContext):
        if ctx.getChildCount() == 2:
            node: NodeWrapper[AstUnOpNode] = wrap(AstUnOpNode(ctx.getChild(0).getText()))
            node.n.operand_w = self.visit(ctx.getChild(1))
            return node
        return self.visitChildren(ctx)

    def visitLiteral(self, ctx: C_ExpressionsParser.LiteralContext):
        node: NodeWrapper[AstLiteralNode] = wrap(AstLiteralNode(int(ctx.getChild(0).getText()))) # TODO: delete the int cast and do better
        return node

    def visitParenExpr(self, ctx: C_ExpressionsParser.ParenExprContext):
        return self.visit(ctx.getChild(1))

    def visitStatement(self, ctx: C_ExpressionsParser.StatementContext):
        return self.visit(ctx.getChild(0))
