from src.antlr_files.C_GrammarParser import *
from graphviz import Digraph
from antlr4.tree.Trees import Trees
from src.antlr_files.C_GrammarVisitor import *

class VisualizationVisitor(C_GrammarVisitor):
    def visit(self, tree):
        return tree.visitChildren(self)
    def visualize(self, root: ParserRuleContext, rules, filename: str):
        dot = Digraph()
        dot.node_attr['shape'] = 'box'
        def add_nodes(node: ParserRuleContext):
            currentName = Trees.getNodeText(node, rules)
            dot.node(str(id(node)), currentName, fillcolor= 'lightblue' if not isinstance(node, TerminalNode) else 'lightgreen', style='filled')
            if node.getChildCount():
                for child in node.getChildren():
                    child_id = id(child)
                    dot.node(str(child_id), str(child), fillcolor='lightblue', style='filled')
                    dot.edge(str(id(node)), str(child_id))
                    add_nodes(child)

        add_nodes(root)
        dot.render(filename, format='png', cleanup=True)