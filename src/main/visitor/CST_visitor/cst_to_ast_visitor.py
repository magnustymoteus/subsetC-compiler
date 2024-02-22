from src.antlr_files.C_ExpressionsVisitor import *
from src.antlr_files.C_ExpressionsParser import *
from src.parser.AST import *


class CSTToASTVisitor(C_ExpressionsVisitor):
    def visitBinaryOp(self, ctx: ParserRuleContext):
        node: NodeWrapper[AstBinOpNode] = wrap(AstBinOpNode(ctx.getChild(1)))
        left = wrap(AstLiteralNode(ctx.getChild(0))) if ctx.getChild(0).getChildCount() == 0 else self.visit(
            ctx.getChild(0))
        right = wrap(AstLiteralNode(ctx.getChild(2))) if ctx.getChild(2).getChildCount() == 0 else self.visit(
            ctx.getChild(2))
        node.n.lhs_w = left
        node.n.rhs_w = right
        return node

    def visitProgram(self, ctx: C_ExpressionsParser.ProgramContext):
        ast = Ast()
        statements = [self.visit(statement) for statement in ctx.getChildren()]
        program_node = wrap(AstProgramNode(statements))
        ast.set_root(program_node)
        return ast

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
    def visitRelationalExpr(self, ctx:C_ExpressionsParser.RelationalExprContext):
        return self.visitBinaryOp(ctx)

    # Visit a parse tree produced by C_ExpressionsParser#unaryExpr.
    def visitUnaryExpr(self, ctx: C_ExpressionsParser.UnaryExprContext):
        node: NodeWrapper[AstUnOpNode] = wrap(AstUnOpNode(ctx.getChild(0)))
        node.n.operand_w = wrap(AstLiteralNode(ctx.getChild(1))) if ctx.getChild(1).getChildCount() == 0 \
            else self.visit(ctx.getChild(1))
        return node

