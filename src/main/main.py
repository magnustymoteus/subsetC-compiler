import sys

from src.parser.visitor.CST_visitor.cst_to_ast_visitor import CSTToASTVisitor
from src.parser.visitor.CST_visitor.visualization_visitor import VisualizationVisitor

from src.parser import *
from src.parser import optimizations as optim
from src.antlr_files.C_GrammarLexer import *
from src.antlr_files.C_GrammarParser import *
from src.antlr_files.C_GrammarVisitor import *

"""
flags to implement: 
main : main() required
cfold : enable constant folding
"""

def getTokens(filepath: str):
    input_stream = FileStream(filepath)
    lexer = C_GrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    return stream

def visualizeCST(tree, rules, filename):
    visualizationVisitor = VisualizationVisitor()
    visualizationVisitor.visualize(tree, rules, filename)

def getAST(tree) -> Ast:
    ast = Ast()
    converterVisitor = CSTToASTVisitor()
    root = converterVisitor.visit(tree)
    ast.set_root(root)
    return ast
def applyConstantFolding(ast: Ast):
    optim.constant_folding(ast)

def visualizeAST(ast: Ast, filename: str):
    graph = ast.to_dot_graph()
    graph.save(filename=filename)




def main(argv):
    pass


if __name__ == '__main__':
    main(sys.argv)
