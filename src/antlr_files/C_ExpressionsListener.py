# Generated from C_Expressions.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .C_ExpressionsParser import C_ExpressionsParser
else:
    from C_ExpressionsParser import C_ExpressionsParser

# This class defines a complete listener for a parse tree produced by C_ExpressionsParser.
class C_ExpressionsListener(ParseTreeListener):

    # Enter a parse tree produced by C_ExpressionsParser#statement.
    def enterStatement(self, ctx:C_ExpressionsParser.StatementContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#statement.
    def exitStatement(self, ctx:C_ExpressionsParser.StatementContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#exprStatement.
    def enterExprStatement(self, ctx:C_ExpressionsParser.ExprStatementContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#exprStatement.
    def exitExprStatement(self, ctx:C_ExpressionsParser.ExprStatementContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#expr.
    def enterExpr(self, ctx:C_ExpressionsParser.ExprContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#expr.
    def exitExpr(self, ctx:C_ExpressionsParser.ExprContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#constantExpr.
    def enterConstantExpr(self, ctx:C_ExpressionsParser.ConstantExprContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#constantExpr.
    def exitConstantExpr(self, ctx:C_ExpressionsParser.ConstantExprContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#conditionalExpr.
    def enterConditionalExpr(self, ctx:C_ExpressionsParser.ConditionalExprContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#conditionalExpr.
    def exitConditionalExpr(self, ctx:C_ExpressionsParser.ConditionalExprContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#logicalOrExpr.
    def enterLogicalOrExpr(self, ctx:C_ExpressionsParser.LogicalOrExprContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#logicalOrExpr.
    def exitLogicalOrExpr(self, ctx:C_ExpressionsParser.LogicalOrExprContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#logicalAndExpr.
    def enterLogicalAndExpr(self, ctx:C_ExpressionsParser.LogicalAndExprContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#logicalAndExpr.
    def exitLogicalAndExpr(self, ctx:C_ExpressionsParser.LogicalAndExprContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#bitwiseOrExpr.
    def enterBitwiseOrExpr(self, ctx:C_ExpressionsParser.BitwiseOrExprContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#bitwiseOrExpr.
    def exitBitwiseOrExpr(self, ctx:C_ExpressionsParser.BitwiseOrExprContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#logicalXorExpr.
    def enterLogicalXorExpr(self, ctx:C_ExpressionsParser.LogicalXorExprContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#logicalXorExpr.
    def exitLogicalXorExpr(self, ctx:C_ExpressionsParser.LogicalXorExprContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#bitwiseAndExpr.
    def enterBitwiseAndExpr(self, ctx:C_ExpressionsParser.BitwiseAndExprContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#bitwiseAndExpr.
    def exitBitwiseAndExpr(self, ctx:C_ExpressionsParser.BitwiseAndExprContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#equalityExpr.
    def enterEqualityExpr(self, ctx:C_ExpressionsParser.EqualityExprContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#equalityExpr.
    def exitEqualityExpr(self, ctx:C_ExpressionsParser.EqualityExprContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#relationalExpr.
    def enterRelationalExpr(self, ctx:C_ExpressionsParser.RelationalExprContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#relationalExpr.
    def exitRelationalExpr(self, ctx:C_ExpressionsParser.RelationalExprContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#shiftExpr.
    def enterShiftExpr(self, ctx:C_ExpressionsParser.ShiftExprContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#shiftExpr.
    def exitShiftExpr(self, ctx:C_ExpressionsParser.ShiftExprContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#addExpr.
    def enterAddExpr(self, ctx:C_ExpressionsParser.AddExprContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#addExpr.
    def exitAddExpr(self, ctx:C_ExpressionsParser.AddExprContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#multExpr.
    def enterMultExpr(self, ctx:C_ExpressionsParser.MultExprContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#multExpr.
    def exitMultExpr(self, ctx:C_ExpressionsParser.MultExprContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#unaryExpr.
    def enterUnaryExpr(self, ctx:C_ExpressionsParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#unaryExpr.
    def exitUnaryExpr(self, ctx:C_ExpressionsParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#unaryOperator.
    def enterUnaryOperator(self, ctx:C_ExpressionsParser.UnaryOperatorContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#unaryOperator.
    def exitUnaryOperator(self, ctx:C_ExpressionsParser.UnaryOperatorContext):
        pass


    # Enter a parse tree produced by C_ExpressionsParser#constant.
    def enterConstant(self, ctx:C_ExpressionsParser.ConstantContext):
        pass

    # Exit a parse tree produced by C_ExpressionsParser#constant.
    def exitConstant(self, ctx:C_ExpressionsParser.ConstantContext):
        pass



del C_ExpressionsParser