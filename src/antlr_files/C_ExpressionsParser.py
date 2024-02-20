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
        4,1,26,184,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,1,0,1,0,1,0,1,0,1,0,1,0,
        1,0,1,0,5,0,45,8,0,10,0,12,0,48,9,0,1,1,1,1,1,2,1,2,3,2,54,8,2,1,
        3,1,3,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,5,5,5,66,8,5,10,5,12,5,69,9,
        5,1,6,1,6,1,6,1,6,1,6,1,6,5,6,77,8,6,10,6,12,6,80,9,6,1,7,1,7,1,
        7,1,7,1,7,1,7,5,7,88,8,7,10,7,12,7,91,9,7,1,8,1,8,1,8,1,8,1,8,1,
        8,5,8,99,8,8,10,8,12,8,102,9,8,1,9,1,9,1,9,1,9,1,9,1,9,5,9,110,8,
        9,10,9,12,9,113,9,9,1,10,1,10,1,10,1,10,1,10,1,10,5,10,121,8,10,
        10,10,12,10,124,9,10,1,11,1,11,1,11,1,11,1,11,1,11,5,11,132,8,11,
        10,11,12,11,135,9,11,1,12,1,12,1,12,1,12,1,12,1,12,5,12,143,8,12,
        10,12,12,12,146,9,12,1,13,1,13,1,13,1,13,1,13,1,13,5,13,154,8,13,
        10,13,12,13,157,9,13,1,14,1,14,1,14,1,14,1,14,1,14,5,14,165,8,14,
        10,14,12,14,168,9,14,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,15,3,15,
        178,8,15,1,16,1,16,1,17,1,17,1,17,0,11,0,10,12,14,16,18,20,22,24,
        26,28,18,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,0,6,1,
        0,14,15,1,0,10,13,1,0,23,24,1,0,4,5,1,0,6,8,3,0,4,5,18,18,21,21,
        179,0,36,1,0,0,0,2,49,1,0,0,0,4,53,1,0,0,0,6,55,1,0,0,0,8,57,1,0,
        0,0,10,59,1,0,0,0,12,70,1,0,0,0,14,81,1,0,0,0,16,92,1,0,0,0,18,103,
        1,0,0,0,20,114,1,0,0,0,22,125,1,0,0,0,24,136,1,0,0,0,26,147,1,0,
        0,0,28,158,1,0,0,0,30,177,1,0,0,0,32,179,1,0,0,0,34,181,1,0,0,0,
        36,37,6,0,-1,0,37,38,3,2,1,0,38,39,5,1,0,0,39,46,1,0,0,0,40,41,10,
        1,0,0,41,42,3,2,1,0,42,43,5,1,0,0,43,45,1,0,0,0,44,40,1,0,0,0,45,
        48,1,0,0,0,46,44,1,0,0,0,46,47,1,0,0,0,47,1,1,0,0,0,48,46,1,0,0,
        0,49,50,3,4,2,0,50,3,1,0,0,0,51,54,3,6,3,0,52,54,3,34,17,0,53,51,
        1,0,0,0,53,52,1,0,0,0,54,5,1,0,0,0,55,56,3,8,4,0,56,7,1,0,0,0,57,
        58,3,10,5,0,58,9,1,0,0,0,59,60,6,5,-1,0,60,61,3,12,6,0,61,67,1,0,
        0,0,62,63,10,1,0,0,63,64,5,17,0,0,64,66,3,12,6,0,65,62,1,0,0,0,66,
        69,1,0,0,0,67,65,1,0,0,0,67,68,1,0,0,0,68,11,1,0,0,0,69,67,1,0,0,
        0,70,71,6,6,-1,0,71,72,3,14,7,0,72,78,1,0,0,0,73,74,10,1,0,0,74,
        75,5,16,0,0,75,77,3,14,7,0,76,73,1,0,0,0,77,80,1,0,0,0,78,76,1,0,
        0,0,78,79,1,0,0,0,79,13,1,0,0,0,80,78,1,0,0,0,81,82,6,7,-1,0,82,
        83,3,16,8,0,83,89,1,0,0,0,84,85,10,1,0,0,85,86,5,20,0,0,86,88,3,
        16,8,0,87,84,1,0,0,0,88,91,1,0,0,0,89,87,1,0,0,0,89,90,1,0,0,0,90,
        15,1,0,0,0,91,89,1,0,0,0,92,93,6,8,-1,0,93,94,3,18,9,0,94,100,1,
        0,0,0,95,96,10,1,0,0,96,97,5,22,0,0,97,99,3,18,9,0,98,95,1,0,0,0,
        99,102,1,0,0,0,100,98,1,0,0,0,100,101,1,0,0,0,101,17,1,0,0,0,102,
        100,1,0,0,0,103,104,6,9,-1,0,104,105,3,20,10,0,105,111,1,0,0,0,106,
        107,10,1,0,0,107,108,5,19,0,0,108,110,3,20,10,0,109,106,1,0,0,0,
        110,113,1,0,0,0,111,109,1,0,0,0,111,112,1,0,0,0,112,19,1,0,0,0,113,
        111,1,0,0,0,114,115,6,10,-1,0,115,116,3,22,11,0,116,122,1,0,0,0,
        117,118,10,1,0,0,118,119,7,0,0,0,119,121,3,22,11,0,120,117,1,0,0,
        0,121,124,1,0,0,0,122,120,1,0,0,0,122,123,1,0,0,0,123,21,1,0,0,0,
        124,122,1,0,0,0,125,126,6,11,-1,0,126,127,3,24,12,0,127,133,1,0,
        0,0,128,129,10,1,0,0,129,130,7,1,0,0,130,132,3,24,12,0,131,128,1,
        0,0,0,132,135,1,0,0,0,133,131,1,0,0,0,133,134,1,0,0,0,134,23,1,0,
        0,0,135,133,1,0,0,0,136,137,6,12,-1,0,137,138,3,26,13,0,138,144,
        1,0,0,0,139,140,10,1,0,0,140,141,7,2,0,0,141,143,3,26,13,0,142,139,
        1,0,0,0,143,146,1,0,0,0,144,142,1,0,0,0,144,145,1,0,0,0,145,25,1,
        0,0,0,146,144,1,0,0,0,147,148,6,13,-1,0,148,149,3,28,14,0,149,155,
        1,0,0,0,150,151,10,1,0,0,151,152,7,3,0,0,152,154,3,28,14,0,153,150,
        1,0,0,0,154,157,1,0,0,0,155,153,1,0,0,0,155,156,1,0,0,0,156,27,1,
        0,0,0,157,155,1,0,0,0,158,159,6,14,-1,0,159,160,3,30,15,0,160,166,
        1,0,0,0,161,162,10,1,0,0,162,163,7,4,0,0,163,165,3,30,15,0,164,161,
        1,0,0,0,165,168,1,0,0,0,166,164,1,0,0,0,166,167,1,0,0,0,167,29,1,
        0,0,0,168,166,1,0,0,0,169,170,3,32,16,0,170,171,3,4,2,0,171,178,
        1,0,0,0,172,173,5,2,0,0,173,174,3,4,2,0,174,175,5,3,0,0,175,178,
        1,0,0,0,176,178,3,34,17,0,177,169,1,0,0,0,177,172,1,0,0,0,177,176,
        1,0,0,0,178,31,1,0,0,0,179,180,7,5,0,0,180,33,1,0,0,0,181,182,5,
        25,0,0,182,35,1,0,0,0,13,46,53,67,78,89,100,111,122,133,144,155,
        166,177
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

    RULE_statement = 0
    RULE_exprStatement = 1
    RULE_expr = 2
    RULE_constantExpr = 3
    RULE_conditionalExpr = 4
    RULE_logicalOrExpr = 5
    RULE_logicalAndExpr = 6
    RULE_bitwiseOrExpr = 7
    RULE_logicalXorExpr = 8
    RULE_bitwiseAndExpr = 9
    RULE_equalityExpr = 10
    RULE_relationalExpr = 11
    RULE_shiftExpr = 12
    RULE_addExpr = 13
    RULE_multExpr = 14
    RULE_unaryExpr = 15
    RULE_unaryOperator = 16
    RULE_constant = 17

    ruleNames =  [ "statement", "exprStatement", "expr", "constantExpr", 
                   "conditionalExpr", "logicalOrExpr", "logicalAndExpr", 
                   "bitwiseOrExpr", "logicalXorExpr", "bitwiseAndExpr", 
                   "equalityExpr", "relationalExpr", "shiftExpr", "addExpr", 
                   "multExpr", "unaryExpr", "unaryOperator", "constant" ]

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




    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def exprStatement(self):
            return self.getTypedRuleContext(C_ExpressionsParser.ExprStatementContext,0)


        def statement(self):
            return self.getTypedRuleContext(C_ExpressionsParser.StatementContext,0)


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



    def statement(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = C_ExpressionsParser.StatementContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 0
        self.enterRecursionRule(localctx, 0, self.RULE_statement, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self.exprStatement()
            self.state = 38
            self.match(C_ExpressionsParser.T__0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 46
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.StatementContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_statement)
                    self.state = 40
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 41
                    self.exprStatement()
                    self.state = 42
                    self.match(C_ExpressionsParser.T__0) 
                self.state = 48
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
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
        self.enterRule(localctx, 2, self.RULE_exprStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 49
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


        def constant(self):
            return self.getTypedRuleContext(C_ExpressionsParser.ConstantContext,0)


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
        self.enterRule(localctx, 4, self.RULE_expr)
        try:
            self.state = 53
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 51
                self.constantExpr()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 52
                self.constant()
                pass


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
        self.enterRule(localctx, 6, self.RULE_constantExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 55
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
        self.enterRule(localctx, 8, self.RULE_conditionalExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
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
        _startState = 10
        self.enterRecursionRule(localctx, 10, self.RULE_logicalOrExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self.logicalAndExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 67
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.LogicalOrExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_logicalOrExpr)
                    self.state = 62
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 63
                    self.match(C_ExpressionsParser.OR)
                    self.state = 64
                    self.logicalAndExpr(0) 
                self.state = 69
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
        _startState = 12
        self.enterRecursionRule(localctx, 12, self.RULE_logicalAndExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            self.bitwiseOrExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 78
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.LogicalAndExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_logicalAndExpr)
                    self.state = 73
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 74
                    self.match(C_ExpressionsParser.AND)
                    self.state = 75
                    self.bitwiseOrExpr(0) 
                self.state = 80
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
        _startState = 14
        self.enterRecursionRule(localctx, 14, self.RULE_bitwiseOrExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.logicalXorExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 89
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.BitwiseOrExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_bitwiseOrExpr)
                    self.state = 84
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 85
                    self.match(C_ExpressionsParser.BITOR)
                    self.state = 86
                    self.logicalXorExpr(0) 
                self.state = 91
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
        _startState = 16
        self.enterRecursionRule(localctx, 16, self.RULE_logicalXorExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 93
            self.bitwiseAndExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 100
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.LogicalXorExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_logicalXorExpr)
                    self.state = 95
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 96
                    self.match(C_ExpressionsParser.BITXOR)
                    self.state = 97
                    self.bitwiseAndExpr(0) 
                self.state = 102
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
        _startState = 18
        self.enterRecursionRule(localctx, 18, self.RULE_bitwiseAndExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 104
            self.equalityExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 111
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.BitwiseAndExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_bitwiseAndExpr)
                    self.state = 106
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 107
                    self.match(C_ExpressionsParser.BITAND)
                    self.state = 108
                    self.equalityExpr(0) 
                self.state = 113
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
        _startState = 20
        self.enterRecursionRule(localctx, 20, self.RULE_equalityExpr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.relationalExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 122
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.EqualityExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_equalityExpr)
                    self.state = 117
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 118
                    _la = self._input.LA(1)
                    if not(_la==14 or _la==15):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 119
                    self.relationalExpr(0) 
                self.state = 124
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
        _startState = 22
        self.enterRecursionRule(localctx, 22, self.RULE_relationalExpr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 126
            self.shiftExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 133
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.RelationalExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_relationalExpr)
                    self.state = 128
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 129
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 15360) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 130
                    self.shiftExpr(0) 
                self.state = 135
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
        _startState = 24
        self.enterRecursionRule(localctx, 24, self.RULE_shiftExpr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 137
            self.addExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 144
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,9,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.ShiftExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_shiftExpr)
                    self.state = 139
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 140
                    _la = self._input.LA(1)
                    if not(_la==23 or _la==24):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 141
                    self.addExpr(0) 
                self.state = 146
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
        _startState = 26
        self.enterRecursionRule(localctx, 26, self.RULE_addExpr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 148
            self.multExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 155
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.AddExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_addExpr)
                    self.state = 150
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 151
                    _la = self._input.LA(1)
                    if not(_la==4 or _la==5):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 152
                    self.multExpr(0) 
                self.state = 157
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
        _startState = 28
        self.enterRecursionRule(localctx, 28, self.RULE_multExpr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 159
            self.unaryExpr()
            self._ctx.stop = self._input.LT(-1)
            self.state = 166
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,11,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = C_ExpressionsParser.MultExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_multExpr)
                    self.state = 161
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 162
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 448) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 163
                    self.unaryExpr() 
                self.state = 168
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


        def LPAREN(self):
            return self.getToken(C_ExpressionsParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(C_ExpressionsParser.RPAREN, 0)

        def constant(self):
            return self.getTypedRuleContext(C_ExpressionsParser.ConstantContext,0)


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
        self.enterRule(localctx, 30, self.RULE_unaryExpr)
        try:
            self.state = 177
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4, 5, 18, 21]:
                self.enterOuterAlt(localctx, 1)
                self.state = 169
                self.unaryOperator()
                self.state = 170
                self.expr()
                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 2)
                self.state = 172
                self.match(C_ExpressionsParser.LPAREN)
                self.state = 173
                self.expr()
                self.state = 174
                self.match(C_ExpressionsParser.RPAREN)
                pass
            elif token in [25]:
                self.enterOuterAlt(localctx, 3)
                self.state = 176
                self.constant()
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
        self.enterRule(localctx, 32, self.RULE_unaryOperator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 179
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


    class ConstantContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(C_ExpressionsParser.INT, 0)

        def getRuleIndex(self):
            return C_ExpressionsParser.RULE_constant

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstant" ):
                listener.enterConstant(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstant" ):
                listener.exitConstant(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstant" ):
                return visitor.visitConstant(self)
            else:
                return visitor.visitChildren(self)




    def constant(self):

        localctx = C_ExpressionsParser.ConstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_constant)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 181
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
        self._predicates[0] = self.statement_sempred
        self._predicates[5] = self.logicalOrExpr_sempred
        self._predicates[6] = self.logicalAndExpr_sempred
        self._predicates[7] = self.bitwiseOrExpr_sempred
        self._predicates[8] = self.logicalXorExpr_sempred
        self._predicates[9] = self.bitwiseAndExpr_sempred
        self._predicates[10] = self.equalityExpr_sempred
        self._predicates[11] = self.relationalExpr_sempred
        self._predicates[12] = self.shiftExpr_sempred
        self._predicates[13] = self.addExpr_sempred
        self._predicates[14] = self.multExpr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def statement_sempred(self, localctx:StatementContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         

    def logicalOrExpr_sempred(self, localctx:LogicalOrExprContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 1)
         

    def logicalAndExpr_sempred(self, localctx:LogicalAndExprContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 1)
         

    def bitwiseOrExpr_sempred(self, localctx:BitwiseOrExprContext, predIndex:int):
            if predIndex == 3:
                return self.precpred(self._ctx, 1)
         

    def logicalXorExpr_sempred(self, localctx:LogicalXorExprContext, predIndex:int):
            if predIndex == 4:
                return self.precpred(self._ctx, 1)
         

    def bitwiseAndExpr_sempred(self, localctx:BitwiseAndExprContext, predIndex:int):
            if predIndex == 5:
                return self.precpred(self._ctx, 1)
         

    def equalityExpr_sempred(self, localctx:EqualityExprContext, predIndex:int):
            if predIndex == 6:
                return self.precpred(self._ctx, 1)
         

    def relationalExpr_sempred(self, localctx:RelationalExprContext, predIndex:int):
            if predIndex == 7:
                return self.precpred(self._ctx, 1)
         

    def shiftExpr_sempred(self, localctx:ShiftExprContext, predIndex:int):
            if predIndex == 8:
                return self.precpred(self._ctx, 1)
         

    def addExpr_sempred(self, localctx:AddExprContext, predIndex:int):
            if predIndex == 9:
                return self.precpred(self._ctx, 1)
         

    def multExpr_sempred(self, localctx:MultExprContext, predIndex:int):
            if predIndex == 10:
                return self.precpred(self._ctx, 1)
         




