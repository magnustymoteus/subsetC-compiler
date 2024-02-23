# Generated from ../../grammars/C_Expressions.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,26,188,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,1,0,
        5,0,42,8,0,10,0,12,0,45,9,0,1,0,1,0,1,1,1,1,1,1,1,1,3,1,53,8,1,1,
        2,1,2,1,3,1,3,1,4,1,4,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,5,6,69,8,6,
        10,6,12,6,72,9,6,1,7,1,7,1,7,1,7,1,7,1,7,5,7,80,8,7,10,7,12,7,83,
        9,7,1,8,1,8,1,8,1,8,1,8,1,8,5,8,91,8,8,10,8,12,8,94,9,8,1,9,1,9,
        1,9,1,9,1,9,1,9,5,9,102,8,9,10,9,12,9,105,9,9,1,10,1,10,1,10,1,10,
        1,10,1,10,5,10,113,8,10,10,10,12,10,116,9,10,1,11,1,11,1,11,1,11,
        1,11,1,11,5,11,124,8,11,10,11,12,11,127,9,11,1,12,1,12,1,12,1,12,
        1,12,1,12,5,12,135,8,12,10,12,12,12,138,9,12,1,13,1,13,1,13,1,13,
        1,13,1,13,5,13,146,8,13,10,13,12,13,149,9,13,1,14,1,14,1,14,1,14,
        1,14,1,14,5,14,157,8,14,10,14,12,14,160,9,14,1,15,1,15,1,15,1,15,
        1,15,1,15,5,15,168,8,15,10,15,12,15,171,9,15,1,16,1,16,1,16,1,16,
        1,16,3,16,178,8,16,1,17,1,17,1,17,1,17,1,18,1,18,1,19,1,19,1,19,
        0,10,12,14,16,18,20,22,24,26,28,30,20,0,2,4,6,8,10,12,14,16,18,20,
        22,24,26,28,30,32,34,36,38,0,6,1,0,14,15,1,0,10,13,1,0,23,24,1,0,
        4,5,1,0,6,8,3,0,4,5,18,18,21,21,181,0,43,1,0,0,0,2,52,1,0,0,0,4,
        54,1,0,0,0,6,56,1,0,0,0,8,58,1,0,0,0,10,60,1,0,0,0,12,62,1,0,0,0,
        14,73,1,0,0,0,16,84,1,0,0,0,18,95,1,0,0,0,20,106,1,0,0,0,22,117,
        1,0,0,0,24,128,1,0,0,0,26,139,1,0,0,0,28,150,1,0,0,0,30,161,1,0,
        0,0,32,177,1,0,0,0,34,179,1,0,0,0,36,183,1,0,0,0,38,185,1,0,0,0,
        40,42,3,2,1,0,41,40,1,0,0,0,42,45,1,0,0,0,43,41,1,0,0,0,43,44,1,
        0,0,0,44,46,1,0,0,0,45,43,1,0,0,0,46,47,5,0,0,1,47,1,1,0,0,0,48,
        49,3,4,2,0,49,50,5,1,0,0,50,53,1,0,0,0,51,53,5,1,0,0,52,48,1,0,0,
        0,52,51,1,0,0,0,53,3,1,0,0,0,54,55,3,6,3,0,55,5,1,0,0,0,56,57,3,
        8,4,0,57,7,1,0,0,0,58,59,3,10,5,0,59,9,1,0,0,0,60,61,3,12,6,0,61,
        11,1,0,0,0,62,63,6,6,-1,0,63,64,3,14,7,0,64,70,1,0,0,0,65,66,10,
        1,0,0,66,67,5,17,0,0,67,69,3,14,7,0,68,65,1,0,0,0,69,72,1,0,0,0,
        70,68,1,0,0,0,70,71,1,0,0,0,71,13,1,0,0,0,72,70,1,0,0,0,73,74,6,
        7,-1,0,74,75,3,16,8,0,75,81,1,0,0,0,76,77,10,1,0,0,77,78,5,16,0,
        0,78,80,3,16,8,0,79,76,1,0,0,0,80,83,1,0,0,0,81,79,1,0,0,0,81,82,
        1,0,0,0,82,15,1,0,0,0,83,81,1,0,0,0,84,85,6,8,-1,0,85,86,3,18,9,
        0,86,92,1,0,0,0,87,88,10,1,0,0,88,89,5,20,0,0,89,91,3,18,9,0,90,
        87,1,0,0,0,91,94,1,0,0,0,92,90,1,0,0,0,92,93,1,0,0,0,93,17,1,0,0,
        0,94,92,1,0,0,0,95,96,6,9,-1,0,96,97,3,20,10,0,97,103,1,0,0,0,98,
        99,10,1,0,0,99,100,5,22,0,0,100,102,3,20,10,0,101,98,1,0,0,0,102,
        105,1,0,0,0,103,101,1,0,0,0,103,104,1,0,0,0,104,19,1,0,0,0,105,103,
        1,0,0,0,106,107,6,10,-1,0,107,108,3,22,11,0,108,114,1,0,0,0,109,
        110,10,1,0,0,110,111,5,19,0,0,111,113,3,22,11,0,112,109,1,0,0,0,
        113,116,1,0,0,0,114,112,1,0,0,0,114,115,1,0,0,0,115,21,1,0,0,0,116,
        114,1,0,0,0,117,118,6,11,-1,0,118,119,3,24,12,0,119,125,1,0,0,0,
        120,121,10,1,0,0,121,122,7,0,0,0,122,124,3,24,12,0,123,120,1,0,0,
        0,124,127,1,0,0,0,125,123,1,0,0,0,125,126,1,0,0,0,126,23,1,0,0,0,
        127,125,1,0,0,0,128,129,6,12,-1,0,129,130,3,26,13,0,130,136,1,0,
        0,0,131,132,10,1,0,0,132,133,7,1,0,0,133,135,3,26,13,0,134,131,1,
        0,0,0,135,138,1,0,0,0,136,134,1,0,0,0,136,137,1,0,0,0,137,25,1,0,
        0,0,138,136,1,0,0,0,139,140,6,13,-1,0,140,141,3,28,14,0,141,147,
        1,0,0,0,142,143,10,1,0,0,143,144,7,2,0,0,144,146,3,28,14,0,145,142,
        1,0,0,0,146,149,1,0,0,0,147,145,1,0,0,0,147,148,1,0,0,0,148,27,1,
        0,0,0,149,147,1,0,0,0,150,151,6,14,-1,0,151,152,3,30,15,0,152,158,
        1,0,0,0,153,154,10,1,0,0,154,155,7,3,0,0,155,157,3,30,15,0,156,153,
        1,0,0,0,157,160,1,0,0,0,158,156,1,0,0,0,158,159,1,0,0,0,159,29,1,
        0,0,0,160,158,1,0,0,0,161,162,6,15,-1,0,162,163,3,32,16,0,163,169,
        1,0,0,0,164,165,10,1,0,0,165,166,7,4,0,0,166,168,3,32,16,0,167,164,
        1,0,0,0,168,171,1,0,0,0,169,167,1,0,0,0,169,170,1,0,0,0,170,31,1,
        0,0,0,171,169,1,0,0,0,172,173,3,36,18,0,173,174,3,6,3,0,174,178,
        1,0,0,0,175,178,3,38,19,0,176,178,3,34,17,0,177,172,1,0,0,0,177,
        175,1,0,0,0,177,176,1,0,0,0,178,33,1,0,0,0,179,180,5,2,0,0,180,181,
        3,6,3,0,181,182,5,3,0,0,182,35,1,0,0,0,183,184,7,5,0,0,184,37,1,
        0,0,0,185,186,5,25,0,0,186,39,1,0,0,0,13,43,52,70,81,92,103,114,
        125,136,147,158,169,177
    ]

class C_ExpressionsParser ( Parser ):

    grammarFileName = "C_Expressions.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "'('", "')'", "'+'", "'-'", "'*'", 
                     "'/'", "'%'", "'='", "'>'", "'<'", "'>='", "'<='", 
                     "'=='", "'!='", "'&&'", "'||'", "'!'", "'&'", "'|'", 
                     "'~'", "'^'", "'<<'", "'>>'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "LPAREN", "RPAREN", "PLUS", 
                      "MINUS", "MUL", "DIV", "MOD", "EQ", "GT", "LT", "GTEQ", 
                      "LTEQ", "ISEQ", "ISNEQ", "AND", "OR", "NOT", "BITAND", 
                      "BITOR", "BITNOT", "BITXOR", "SL", "SR", "INT", "WS" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_exprStatement = 2
    RULE_expr = 3
    RULE_constantExpr = 4
    RULE_conditionalExpr = 5
    RULE_logicalOrExpr = 6
    RULE_logicalAndExpr = 7
    RULE_bitwiseOrExpr = 8
    RULE_logicalXorExpr = 9
    RULE_bitwiseAndExpr = 10
    RULE_equalityExpr = 11
    RULE_relationalExpr = 12
    RULE_shiftExpr = 13
    RULE_addExpr = 14
    RULE_multExpr = 15
    RULE_unaryExpr = 16
    RULE_parenExpr = 17
    RULE_unaryOperator = 18
    RULE_literal = 19

    ruleNames =  [ "program", "statement", "exprStatement", "expr", "constantExpr", 
                   "conditionalExpr", "logicalOrExpr", "logicalAndExpr", 
                   "bitwiseOrExpr", "logicalXorExpr", "bitwiseAndExpr", 
                   "equalityExpr", "relationalExpr", "shiftExpr", "addExpr", 
                   "multExpr", "unaryExpr", "parenExpr", "unaryOperator", 
                   "literal" ]

    EOF = Token.EOF
    T__0=1
    LPAREN=2
    RPAREN=3
    PLUS=4
    MINUS=5
    MUL=6
    DIV=7
    MOD=8
    EQ=9
    GT=10
    LT=11
    GTEQ=12
    LTEQ=13
    ISEQ=14
    ISNEQ=15
    AND=16
    OR=17
    NOT=18
    BITAND=19
    BITOR=20
    BITNOT=21
    BITXOR=22
    SL=23
    SR=24
    INT=25
    WS=26

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(C_ExpressionsParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(C_ExpressionsParser.StatementContext)
            else:
                return self.getTypedRuleContext(C_ExpressionsParser.StatementContext,i)


        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = C_ExpressionsParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 35913782) != 0):
                self.state = 40
                self.statement()
                self.state = 45
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 46
            self.match(C_ExpressionsParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def exprStatement(self):
            return self.getTypedRuleContext(C_ExpressionsParser.ExprStatementContext,0)


        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = C_ExpressionsParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 52
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [2, 4, 5, 18, 21, 25]:
                self.enterOuterAlt(localctx, 1)
                self.state = 48
                self.exprStatement()
                self.state = 49
                self.match(C_ExpressionsParser.T__0)
                pass
            elif token in [1]:
                self.enterOuterAlt(localctx, 2)
                self.state = 51
                self.match(C_ExpressionsParser.T__0)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.ExprContext,0)


        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_exprStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprStatement" ):
                listener.enterExprStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprStatement" ):
                listener.exitExprStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprStatement" ):
                return visitor.visitExprStatement(self)
            else:
                return visitor.visitChildren(self)




    def exprStatement(self):

        localctx = C_ExpressionsParser.ExprStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_exprStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 54
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def constantExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.ConstantExprContext,0)


        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = C_ExpressionsParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 56
            self.constantExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstantExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def conditionalExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.ConditionalExprContext,0)


        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_constantExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstantExpr" ):
                listener.enterConstantExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstantExpr" ):
                listener.exitConstantExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstantExpr" ):
                return visitor.visitConstantExpr(self)
            else:
                return visitor.visitChildren(self)




    def constantExpr(self):

        localctx = C_ExpressionsParser.ConstantExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_constantExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 58
            self.conditionalExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionalExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logicalOrExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.LogicalOrExprContext,0)


        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_conditionalExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConditionalExpr" ):
                listener.enterConditionalExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConditionalExpr" ):
                listener.exitConditionalExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConditionalExpr" ):
                return visitor.visitConditionalExpr(self)
            else:
                return visitor.visitChildren(self)




    def conditionalExpr(self):

        localctx = C_ExpressionsParser.ConditionalExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_conditionalExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self.logicalOrExpr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LogicalOrExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logicalAndExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.LogicalAndExprContext,0)


        def logicalOrExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.LogicalOrExprContext,0)


        def OR(self):
            return self.getToken(C_ExpressionsParser.OR, 0)

        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_logicalOrExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogicalOrExpr" ):
                listener.enterLogicalOrExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogicalOrExpr" ):
                listener.exitLogicalOrExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicalOrExpr" ):
                return visitor.visitLogicalOrExpr(self)
            else:
                return visitor.visitChildren(self)



    def logicalOrExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = C_ExpressionsParser.LogicalOrExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 12
        self.enterRecursionRule(localctx, 12, self.RULE_logicalOrExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self.logicalAndExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 70
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.LogicalOrExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_logicalOrExpr)
                    self.state = 65
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 66
                    self.match(C_ExpressionsParser.OR)
                    self.state = 67
                    self.logicalAndExpr(0) 
                self.state = 72
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class LogicalAndExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def bitwiseOrExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.BitwiseOrExprContext,0)


        def logicalAndExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.LogicalAndExprContext,0)


        def AND(self):
            return self.getToken(C_ExpressionsParser.AND, 0)

        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_logicalAndExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogicalAndExpr" ):
                listener.enterLogicalAndExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogicalAndExpr" ):
                listener.exitLogicalAndExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicalAndExpr" ):
                return visitor.visitLogicalAndExpr(self)
            else:
                return visitor.visitChildren(self)



    def logicalAndExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = C_ExpressionsParser.LogicalAndExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 14
        self.enterRecursionRule(localctx, 14, self.RULE_logicalAndExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 74
            self.bitwiseOrExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 81
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.LogicalAndExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_logicalAndExpr)
                    self.state = 76
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 77
                    self.match(C_ExpressionsParser.AND)
                    self.state = 78
                    self.bitwiseOrExpr(0) 
                self.state = 83
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class BitwiseOrExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logicalXorExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.LogicalXorExprContext,0)


        def bitwiseOrExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.BitwiseOrExprContext,0)


        def BITOR(self):
            return self.getToken(C_ExpressionsParser.BITOR, 0)

        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_bitwiseOrExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBitwiseOrExpr" ):
                listener.enterBitwiseOrExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBitwiseOrExpr" ):
                listener.exitBitwiseOrExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBitwiseOrExpr" ):
                return visitor.visitBitwiseOrExpr(self)
            else:
                return visitor.visitChildren(self)



    def bitwiseOrExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = C_ExpressionsParser.BitwiseOrExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 16
        self.enterRecursionRule(localctx, 16, self.RULE_bitwiseOrExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            self.logicalXorExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 92
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.BitwiseOrExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_bitwiseOrExpr)
                    self.state = 87
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 88
                    self.match(C_ExpressionsParser.BITOR)
                    self.state = 89
                    self.logicalXorExpr(0) 
                self.state = 94
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class LogicalXorExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def bitwiseAndExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.BitwiseAndExprContext,0)


        def logicalXorExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.LogicalXorExprContext,0)


        def BITXOR(self):
            return self.getToken(C_ExpressionsParser.BITXOR, 0)

        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_logicalXorExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogicalXorExpr" ):
                listener.enterLogicalXorExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogicalXorExpr" ):
                listener.exitLogicalXorExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicalXorExpr" ):
                return visitor.visitLogicalXorExpr(self)
            else:
                return visitor.visitChildren(self)



    def logicalXorExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = C_ExpressionsParser.LogicalXorExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 18
        self.enterRecursionRule(localctx, 18, self.RULE_logicalXorExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 96
            self.bitwiseAndExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 103
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.LogicalXorExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_logicalXorExpr)
                    self.state = 98
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 99
                    self.match(C_ExpressionsParser.BITXOR)
                    self.state = 100
                    self.bitwiseAndExpr(0) 
                self.state = 105
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class BitwiseAndExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def equalityExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.EqualityExprContext,0)


        def bitwiseAndExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.BitwiseAndExprContext,0)


        def BITAND(self):
            return self.getToken(C_ExpressionsParser.BITAND, 0)

        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_bitwiseAndExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBitwiseAndExpr" ):
                listener.enterBitwiseAndExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBitwiseAndExpr" ):
                listener.exitBitwiseAndExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBitwiseAndExpr" ):
                return visitor.visitBitwiseAndExpr(self)
            else:
                return visitor.visitChildren(self)



    def bitwiseAndExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = C_ExpressionsParser.BitwiseAndExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 20
        self.enterRecursionRule(localctx, 20, self.RULE_bitwiseAndExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self.equalityExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 114
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.BitwiseAndExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_bitwiseAndExpr)
                    self.state = 109
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 110
                    self.match(C_ExpressionsParser.BITAND)
                    self.state = 111
                    self.equalityExpr(0) 
                self.state = 116
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class EqualityExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def relationalExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.RelationalExprContext,0)


        def equalityExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.EqualityExprContext,0)


        def ISEQ(self):
            return self.getToken(C_ExpressionsParser.ISEQ, 0)

        def ISNEQ(self):
            return self.getToken(C_ExpressionsParser.ISNEQ, 0)

        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_equalityExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEqualityExpr" ):
                listener.enterEqualityExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEqualityExpr" ):
                listener.exitEqualityExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEqualityExpr" ):
                return visitor.visitEqualityExpr(self)
            else:
                return visitor.visitChildren(self)



    def equalityExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = C_ExpressionsParser.EqualityExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 22
        self.enterRecursionRule(localctx, 22, self.RULE_equalityExpr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            self.relationalExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 125
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.EqualityExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_equalityExpr)
                    self.state = 120
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 121
                    _la = self._input.LA(1)
                    if not(_la==14 or _la==15):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 122
                    self.relationalExpr(0) 
                self.state = 127
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class RelationalExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def shiftExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.ShiftExprContext,0)


        def relationalExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.RelationalExprContext,0)


        def GT(self):
            return self.getToken(C_ExpressionsParser.GT, 0)

        def LT(self):
            return self.getToken(C_ExpressionsParser.LT, 0)

        def GTEQ(self):
            return self.getToken(C_ExpressionsParser.GTEQ, 0)

        def LTEQ(self):
            return self.getToken(C_ExpressionsParser.LTEQ, 0)

        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_relationalExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelationalExpr" ):
                listener.enterRelationalExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelationalExpr" ):
                listener.exitRelationalExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelationalExpr" ):
                return visitor.visitRelationalExpr(self)
            else:
                return visitor.visitChildren(self)



    def relationalExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = C_ExpressionsParser.RelationalExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 24
        self.enterRecursionRule(localctx, 24, self.RULE_relationalExpr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 129
            self.shiftExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 136
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.RelationalExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_relationalExpr)
                    self.state = 131
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 132
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 15360) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 133
                    self.shiftExpr(0) 
                self.state = 138
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ShiftExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def addExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.AddExprContext,0)


        def shiftExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.ShiftExprContext,0)


        def SL(self):
            return self.getToken(C_ExpressionsParser.SL, 0)

        def SR(self):
            return self.getToken(C_ExpressionsParser.SR, 0)

        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_shiftExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterShiftExpr" ):
                listener.enterShiftExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitShiftExpr" ):
                listener.exitShiftExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitShiftExpr" ):
                return visitor.visitShiftExpr(self)
            else:
                return visitor.visitChildren(self)



    def shiftExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = C_ExpressionsParser.ShiftExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 26
        self.enterRecursionRule(localctx, 26, self.RULE_shiftExpr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 140
            self.addExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 147
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,9,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.ShiftExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_shiftExpr)
                    self.state = 142
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 143
                    _la = self._input.LA(1)
                    if not(_la==23 or _la==24):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 144
                    self.addExpr(0) 
                self.state = 149
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,9,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class AddExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def multExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.MultExprContext,0)


        def addExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.AddExprContext,0)


        def PLUS(self):
            return self.getToken(C_ExpressionsParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(C_ExpressionsParser.MINUS, 0)

        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_addExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddExpr" ):
                listener.enterAddExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddExpr" ):
                listener.exitAddExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddExpr" ):
                return visitor.visitAddExpr(self)
            else:
                return visitor.visitChildren(self)



    def addExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = C_ExpressionsParser.AddExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 28
        self.enterRecursionRule(localctx, 28, self.RULE_addExpr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            self.multExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 158
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.AddExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_addExpr)
                    self.state = 153
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 154
                    _la = self._input.LA(1)
                    if not(_la==4 or _la==5):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 155
                    self.multExpr(0) 
                self.state = 160
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class MultExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unaryExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.UnaryExprContext,0)


        def multExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.MultExprContext,0)


        def MUL(self):
            return self.getToken(C_ExpressionsParser.MUL, 0)

        def DIV(self):
            return self.getToken(C_ExpressionsParser.DIV, 0)

        def MOD(self):
            return self.getToken(C_ExpressionsParser.MOD, 0)

        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_multExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultExpr" ):
                listener.enterMultExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultExpr" ):
                listener.exitMultExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultExpr" ):
                return visitor.visitMultExpr(self)
            else:
                return visitor.visitChildren(self)



    def multExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = C_ExpressionsParser.MultExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 30
        self.enterRecursionRule(localctx, 30, self.RULE_multExpr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 162
            self.unaryExpr()
            self._ctx.stop = self._input.LT(-1)
            self.state = 169
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,11,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.MultExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_multExpr)
                    self.state = 164
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 165
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 448) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 166
                    self.unaryExpr() 
                self.state = 171
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,11,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class UnaryExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unaryOperator(self):
            return self.getTypedRuleContext(C_ExpressionsParser.UnaryOperatorContext,0)


        def expr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.ExprContext,0)


        def literal(self):
            return self.getTypedRuleContext(C_ExpressionsParser.LiteralContext,0)


        def parenExpr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.ParenExprContext,0)


        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_unaryExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryExpr" ):
                listener.enterUnaryExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryExpr" ):
                listener.exitUnaryExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryExpr" ):
                return visitor.visitUnaryExpr(self)
            else:
                return visitor.visitChildren(self)




    def unaryExpr(self):

        localctx = C_ExpressionsParser.UnaryExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_unaryExpr)
        try:
            self.state = 177
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4, 5, 18, 21]:
                self.enterOuterAlt(localctx, 1)
                self.state = 172
                self.unaryOperator()
                self.state = 173
                self.expr()
                pass
            elif token in [25]:
                self.enterOuterAlt(localctx, 2)
                self.state = 175
                self.literal()
                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 3)
                self.state = 176
                self.parenExpr()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParenExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(C_ExpressionsParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(C_ExpressionsParser.ExprContext,0)


        def RPAREN(self):
            return self.getToken(C_ExpressionsParser.RPAREN, 0)

        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_parenExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenExpr" ):
                listener.enterParenExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenExpr" ):
                listener.exitParenExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpr" ):
                return visitor.visitParenExpr(self)
            else:
                return visitor.visitChildren(self)




    def parenExpr(self):

        localctx = C_ExpressionsParser.ParenExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_parenExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 179
            self.match(C_ExpressionsParser.LPAREN)
            self.state = 180
            self.expr()
            self.state = 181
            self.match(C_ExpressionsParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryOperatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLUS(self):
            return self.getToken(C_ExpressionsParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(C_ExpressionsParser.MINUS, 0)

        def NOT(self):
            return self.getToken(C_ExpressionsParser.NOT, 0)

        def BITNOT(self):
            return self.getToken(C_ExpressionsParser.BITNOT, 0)

        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_unaryOperator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryOperator" ):
                listener.enterUnaryOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryOperator" ):
                listener.exitUnaryOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryOperator" ):
                return visitor.visitUnaryOperator(self)
            else:
                return visitor.visitChildren(self)




    def unaryOperator(self):

        localctx = C_ExpressionsParser.UnaryOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_unaryOperator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 183
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 2359344) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(C_ExpressionsParser.INT, 0)

        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteral" ):
                return visitor.visitLiteral(self)
            else:
                return visitor.visitChildren(self)




    def literal(self):

        localctx = C_ExpressionsParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_literal)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 185
            self.match(C_ExpressionsParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[6] = self.logicalOrExpr_sempred
        self._predicates[7] = self.logicalAndExpr_sempred
        self._predicates[8] = self.bitwiseOrExpr_sempred
        self._predicates[9] = self.logicalXorExpr_sempred
        self._predicates[10] = self.bitwiseAndExpr_sempred
        self._predicates[11] = self.equalityExpr_sempred
        self._predicates[12] = self.relationalExpr_sempred
        self._predicates[13] = self.shiftExpr_sempred
        self._predicates[14] = self.addExpr_sempred
        self._predicates[15] = self.multExpr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def logicalOrExpr_sempred(self, localctx:LogicalOrExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         

    def logicalAndExpr_sempred(self, localctx:LogicalAndExprContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 1)
         

    def bitwiseOrExpr_sempred(self, localctx:BitwiseOrExprContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 1)
         

    def logicalXorExpr_sempred(self, localctx:LogicalXorExprContext, predIndex:int):
            if predIndex == 3:
                return self.precpred(self._ctx, 1)
         

    def bitwiseAndExpr_sempred(self, localctx:BitwiseAndExprContext, predIndex:int):
            if predIndex == 4:
                return self.precpred(self._ctx, 1)
         

    def equalityExpr_sempred(self, localctx:EqualityExprContext, predIndex:int):
            if predIndex == 5:
                return self.precpred(self._ctx, 1)
         

    def relationalExpr_sempred(self, localctx:RelationalExprContext, predIndex:int):
            if predIndex == 6:
                return self.precpred(self._ctx, 1)
         

    def shiftExpr_sempred(self, localctx:ShiftExprContext, predIndex:int):
            if predIndex == 7:
                return self.precpred(self._ctx, 1)
         

    def addExpr_sempred(self, localctx:AddExprContext, predIndex:int):
            if predIndex == 8:
                return self.precpred(self._ctx, 1)
         

    def multExpr_sempred(self, localctx:MultExprContext, predIndex:int):
            if predIndex == 9:
                return self.precpred(self._ctx, 1)
         




