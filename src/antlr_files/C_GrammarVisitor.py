# Generated from ../../grammars/C_Grammar.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .C_GrammarParser import C_GrammarParser
else:
    from C_GrammarParser import C_GrammarParser

# This class defines a complete generic visitor for a parse tree produced by C_GrammarParser.

class C_GrammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by C_GrammarParser#program.
    def visitProgram(self, ctx:C_GrammarParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#functionDef.
    def visitFunctionDef(self, ctx:C_GrammarParser.FunctionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#typeSpec.
    def visitTypeSpec(self, ctx:C_GrammarParser.TypeSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#typeQual.
    def visitTypeQual(self, ctx:C_GrammarParser.TypeQualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#storageClassSpec.
    def visitStorageClassSpec(self, ctx:C_GrammarParser.StorageClassSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#declarationSpec.
    def visitDeclarationSpec(self, ctx:C_GrammarParser.DeclarationSpecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#declaration.
    def visitDeclaration(self, ctx:C_GrammarParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#declarator.
    def visitDeclarator(self, ctx:C_GrammarParser.DeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#typedefName.
    def visitTypedefName(self, ctx:C_GrammarParser.TypedefNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#pointer.
    def visitPointer(self, ctx:C_GrammarParser.PointerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#initializer.
    def visitInitializer(self, ctx:C_GrammarParser.InitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#parameterList.
    def visitParameterList(self, ctx:C_GrammarParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#parameterDeclaration.
    def visitParameterDeclaration(self, ctx:C_GrammarParser.ParameterDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#stmt.
    def visitStmt(self, ctx:C_GrammarParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#printfStmt.
    def visitPrintfStmt(self, ctx:C_GrammarParser.PrintfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#printfFormat.
    def visitPrintfFormat(self, ctx:C_GrammarParser.PrintfFormatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#compoundStmt.
    def visitCompoundStmt(self, ctx:C_GrammarParser.CompoundStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#blockItem.
    def visitBlockItem(self, ctx:C_GrammarParser.BlockItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#exprStmt.
    def visitExprStmt(self, ctx:C_GrammarParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#expr.
    def visitExpr(self, ctx:C_GrammarParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#assignmentExpr.
    def visitAssignmentExpr(self, ctx:C_GrammarParser.AssignmentExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#assignmentOp.
    def visitAssignmentOp(self, ctx:C_GrammarParser.AssignmentOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#constantExpr.
    def visitConstantExpr(self, ctx:C_GrammarParser.ConstantExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#conditionalExpr.
    def visitConditionalExpr(self, ctx:C_GrammarParser.ConditionalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#logicalOrExpr.
    def visitLogicalOrExpr(self, ctx:C_GrammarParser.LogicalOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#logicalAndExpr.
    def visitLogicalAndExpr(self, ctx:C_GrammarParser.LogicalAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#bitwiseOrExpr.
    def visitBitwiseOrExpr(self, ctx:C_GrammarParser.BitwiseOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#logicalXorExpr.
    def visitLogicalXorExpr(self, ctx:C_GrammarParser.LogicalXorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#bitwiseAndExpr.
    def visitBitwiseAndExpr(self, ctx:C_GrammarParser.BitwiseAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#equalityExpr.
    def visitEqualityExpr(self, ctx:C_GrammarParser.EqualityExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#relationalExpr.
    def visitRelationalExpr(self, ctx:C_GrammarParser.RelationalExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#shiftExpr.
    def visitShiftExpr(self, ctx:C_GrammarParser.ShiftExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#addExpr.
    def visitAddExpr(self, ctx:C_GrammarParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#multExpr.
    def visitMultExpr(self, ctx:C_GrammarParser.MultExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#castExpr.
    def visitCastExpr(self, ctx:C_GrammarParser.CastExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#unaryExpr.
    def visitUnaryExpr(self, ctx:C_GrammarParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#postfixExpr.
    def visitPostfixExpr(self, ctx:C_GrammarParser.PostfixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#postfixOp.
    def visitPostfixOp(self, ctx:C_GrammarParser.PostfixOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#primaryExpr.
    def visitPrimaryExpr(self, ctx:C_GrammarParser.PrimaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#parenExpr.
    def visitParenExpr(self, ctx:C_GrammarParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#unaryOp.
    def visitUnaryOp(self, ctx:C_GrammarParser.UnaryOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#identifier.
    def visitIdentifier(self, ctx:C_GrammarParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#literal.
    def visitLiteral(self, ctx:C_GrammarParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#intLiteral.
    def visitIntLiteral(self, ctx:C_GrammarParser.IntLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#charLiteral.
    def visitCharLiteral(self, ctx:C_GrammarParser.CharLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#floatLiteral.
    def visitFloatLiteral(self, ctx:C_GrammarParser.FloatLiteralContext):
        return self.visitChildren(ctx)



del C_GrammarParser