# Generated from ../../grammars/C_Grammar.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .C_GrammarParser import C_GrammarParser
else:
    from C_GrammarParser import C_GrammarParser

# This class defines a complete listener for a parse tree produced by C_GrammarParser.
class C_GrammarListener(ParseTreeListener):

    # Enter a parse tree produced by C_GrammarParser#program.
    def enterProgram(self, ctx:C_GrammarParser.ProgramContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#program.
    def exitProgram(self, ctx:C_GrammarParser.ProgramContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#functionDef.
    def enterFunctionDef(self, ctx:C_GrammarParser.FunctionDefContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#functionDef.
    def exitFunctionDef(self, ctx:C_GrammarParser.FunctionDefContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#typeSpec.
    def enterTypeSpec(self, ctx:C_GrammarParser.TypeSpecContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#typeSpec.
    def exitTypeSpec(self, ctx:C_GrammarParser.TypeSpecContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#typeQual.
    def enterTypeQual(self, ctx:C_GrammarParser.TypeQualContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#typeQual.
    def exitTypeQual(self, ctx:C_GrammarParser.TypeQualContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#storageClassSpec.
    def enterStorageClassSpec(self, ctx:C_GrammarParser.StorageClassSpecContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#storageClassSpec.
    def exitStorageClassSpec(self, ctx:C_GrammarParser.StorageClassSpecContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#declarationSpec.
    def enterDeclarationSpec(self, ctx:C_GrammarParser.DeclarationSpecContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#declarationSpec.
    def exitDeclarationSpec(self, ctx:C_GrammarParser.DeclarationSpecContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#declaration.
    def enterDeclaration(self, ctx:C_GrammarParser.DeclarationContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#declaration.
    def exitDeclaration(self, ctx:C_GrammarParser.DeclarationContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#declarator.
    def enterDeclarator(self, ctx:C_GrammarParser.DeclaratorContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#declarator.
    def exitDeclarator(self, ctx:C_GrammarParser.DeclaratorContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#typedefName.
    def enterTypedefName(self, ctx:C_GrammarParser.TypedefNameContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#typedefName.
    def exitTypedefName(self, ctx:C_GrammarParser.TypedefNameContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#pointer.
    def enterPointer(self, ctx:C_GrammarParser.PointerContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#pointer.
    def exitPointer(self, ctx:C_GrammarParser.PointerContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#initializer.
    def enterInitializer(self, ctx:C_GrammarParser.InitializerContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#initializer.
    def exitInitializer(self, ctx:C_GrammarParser.InitializerContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#parameterList.
    def enterParameterList(self, ctx:C_GrammarParser.ParameterListContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#parameterList.
    def exitParameterList(self, ctx:C_GrammarParser.ParameterListContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#parameterDeclaration.
    def enterParameterDeclaration(self, ctx:C_GrammarParser.ParameterDeclarationContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#parameterDeclaration.
    def exitParameterDeclaration(self, ctx:C_GrammarParser.ParameterDeclarationContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#stmt.
    def enterStmt(self, ctx:C_GrammarParser.StmtContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#stmt.
    def exitStmt(self, ctx:C_GrammarParser.StmtContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#printfStmt.
    def enterPrintfStmt(self, ctx:C_GrammarParser.PrintfStmtContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#printfStmt.
    def exitPrintfStmt(self, ctx:C_GrammarParser.PrintfStmtContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#printfFormat.
    def enterPrintfFormat(self, ctx:C_GrammarParser.PrintfFormatContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#printfFormat.
    def exitPrintfFormat(self, ctx:C_GrammarParser.PrintfFormatContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#compoundStmt.
    def enterCompoundStmt(self, ctx:C_GrammarParser.CompoundStmtContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#compoundStmt.
    def exitCompoundStmt(self, ctx:C_GrammarParser.CompoundStmtContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#blockItem.
    def enterBlockItem(self, ctx:C_GrammarParser.BlockItemContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#blockItem.
    def exitBlockItem(self, ctx:C_GrammarParser.BlockItemContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#exprStmt.
    def enterExprStmt(self, ctx:C_GrammarParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#exprStmt.
    def exitExprStmt(self, ctx:C_GrammarParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#expr.
    def enterExpr(self, ctx:C_GrammarParser.ExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#expr.
    def exitExpr(self, ctx:C_GrammarParser.ExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#assignmentExpr.
    def enterAssignmentExpr(self, ctx:C_GrammarParser.AssignmentExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#assignmentExpr.
    def exitAssignmentExpr(self, ctx:C_GrammarParser.AssignmentExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#assignmentOp.
    def enterAssignmentOp(self, ctx:C_GrammarParser.AssignmentOpContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#assignmentOp.
    def exitAssignmentOp(self, ctx:C_GrammarParser.AssignmentOpContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#constantExpr.
    def enterConstantExpr(self, ctx:C_GrammarParser.ConstantExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#constantExpr.
    def exitConstantExpr(self, ctx:C_GrammarParser.ConstantExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#conditionalExpr.
    def enterConditionalExpr(self, ctx:C_GrammarParser.ConditionalExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#conditionalExpr.
    def exitConditionalExpr(self, ctx:C_GrammarParser.ConditionalExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#logicalOrExpr.
    def enterLogicalOrExpr(self, ctx:C_GrammarParser.LogicalOrExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#logicalOrExpr.
    def exitLogicalOrExpr(self, ctx:C_GrammarParser.LogicalOrExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#logicalAndExpr.
    def enterLogicalAndExpr(self, ctx:C_GrammarParser.LogicalAndExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#logicalAndExpr.
    def exitLogicalAndExpr(self, ctx:C_GrammarParser.LogicalAndExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#bitwiseOrExpr.
    def enterBitwiseOrExpr(self, ctx:C_GrammarParser.BitwiseOrExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#bitwiseOrExpr.
    def exitBitwiseOrExpr(self, ctx:C_GrammarParser.BitwiseOrExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#logicalXorExpr.
    def enterLogicalXorExpr(self, ctx:C_GrammarParser.LogicalXorExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#logicalXorExpr.
    def exitLogicalXorExpr(self, ctx:C_GrammarParser.LogicalXorExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#bitwiseAndExpr.
    def enterBitwiseAndExpr(self, ctx:C_GrammarParser.BitwiseAndExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#bitwiseAndExpr.
    def exitBitwiseAndExpr(self, ctx:C_GrammarParser.BitwiseAndExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#equalityExpr.
    def enterEqualityExpr(self, ctx:C_GrammarParser.EqualityExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#equalityExpr.
    def exitEqualityExpr(self, ctx:C_GrammarParser.EqualityExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#relationalExpr.
    def enterRelationalExpr(self, ctx:C_GrammarParser.RelationalExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#relationalExpr.
    def exitRelationalExpr(self, ctx:C_GrammarParser.RelationalExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#shiftExpr.
    def enterShiftExpr(self, ctx:C_GrammarParser.ShiftExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#shiftExpr.
    def exitShiftExpr(self, ctx:C_GrammarParser.ShiftExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#addExpr.
    def enterAddExpr(self, ctx:C_GrammarParser.AddExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#addExpr.
    def exitAddExpr(self, ctx:C_GrammarParser.AddExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#multExpr.
    def enterMultExpr(self, ctx:C_GrammarParser.MultExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#multExpr.
    def exitMultExpr(self, ctx:C_GrammarParser.MultExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#castExpr.
    def enterCastExpr(self, ctx:C_GrammarParser.CastExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#castExpr.
    def exitCastExpr(self, ctx:C_GrammarParser.CastExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#unaryExpr.
    def enterUnaryExpr(self, ctx:C_GrammarParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#unaryExpr.
    def exitUnaryExpr(self, ctx:C_GrammarParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#postfixExpr.
    def enterPostfixExpr(self, ctx:C_GrammarParser.PostfixExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#postfixExpr.
    def exitPostfixExpr(self, ctx:C_GrammarParser.PostfixExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#postfixOp.
    def enterPostfixOp(self, ctx:C_GrammarParser.PostfixOpContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#postfixOp.
    def exitPostfixOp(self, ctx:C_GrammarParser.PostfixOpContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#primaryExpr.
    def enterPrimaryExpr(self, ctx:C_GrammarParser.PrimaryExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#primaryExpr.
    def exitPrimaryExpr(self, ctx:C_GrammarParser.PrimaryExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#parenExpr.
    def enterParenExpr(self, ctx:C_GrammarParser.ParenExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#parenExpr.
    def exitParenExpr(self, ctx:C_GrammarParser.ParenExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#unaryOp.
    def enterUnaryOp(self, ctx:C_GrammarParser.UnaryOpContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#unaryOp.
    def exitUnaryOp(self, ctx:C_GrammarParser.UnaryOpContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#identifier.
    def enterIdentifier(self, ctx:C_GrammarParser.IdentifierContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#identifier.
    def exitIdentifier(self, ctx:C_GrammarParser.IdentifierContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#literal.
    def enterLiteral(self, ctx:C_GrammarParser.LiteralContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#literal.
    def exitLiteral(self, ctx:C_GrammarParser.LiteralContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#intLiteral.
    def enterIntLiteral(self, ctx:C_GrammarParser.IntLiteralContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#intLiteral.
    def exitIntLiteral(self, ctx:C_GrammarParser.IntLiteralContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#charLiteral.
    def enterCharLiteral(self, ctx:C_GrammarParser.CharLiteralContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#charLiteral.
    def exitCharLiteral(self, ctx:C_GrammarParser.CharLiteralContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#floatLiteral.
    def enterFloatLiteral(self, ctx:C_GrammarParser.FloatLiteralContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#floatLiteral.
    def exitFloatLiteral(self, ctx:C_GrammarParser.FloatLiteralContext):
        pass



del C_GrammarParser