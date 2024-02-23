import sys

from src.main.visitor.CST_visitor.cst_to_ast_visitor import CSTToASTVisitor
from src.main.visitor.CST_visitor.visualization_visitor import VisualizationVisitor

from src.parser import *
from src.parser import optimizations as optim
from src.antlr_files.C_ExpressionsLexer import *
from src.antlr_files.C_ExpressionsParser import *
from src.antlr_files.C_ExpressionsVisitor import *

def getTokens(filepath: str):
    input_stream = FileStream(filepath)
    lexer = C_ExpressionsLexer(input_stream)
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
