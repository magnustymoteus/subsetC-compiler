from src.antlr_files.C_ExpressionsParser import *

class CollapserVisitor():
    def getCollapsedCST(self, root: ParserRuleContext) -> ParserRuleContext:
        while root.getChildCount() == 1:
            child = root.getChild(0)
            root = child
        if root.getChildCount():
            for i in range(0, len(root.children)):
                root.children[i] = self.getCollapsedCST(root.children[i])
        return root