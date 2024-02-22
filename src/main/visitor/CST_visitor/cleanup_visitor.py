from src.antlr_files.C_ExpressionsParser import *
from src.antlr_files.C_ExpressionsVisitor import *

class CleanUpVisitor(C_ExpressionsVisitor):
    def visit(self, tree):
        super().visit(tree)
        self.__getCleanedUpCST(tree)
    def __getCleanedUpCST(self, root: ParserRuleContext) -> ParserRuleContext:
        while root.getChildCount() == 1:
            child = root.getChild(0)
            root = child
        if root.getChildCount():
            for i in range(0, len(root.children)):
                root.children[i] = self.__getCleanedUpCST(root.children[i])
        return root
    def visitParenExpr(self, ctx:C_ExpressionsParser.ParenExprContext):
        ctx.removeLastChild()
        ctx.children.pop(0)
        return self.visitChildren(ctx)
    def visitStatement(self, ctx:C_ExpressionsParser.StatementContext):
        ctx.removeLastChild()
        return self.visitChildren(ctx)