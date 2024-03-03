import sys
import os
from pathlib import Path


from src.parser.visitor.CST_visitor.cst_to_ast_visitor import CSTToASTVisitor
from src.parser.visitor.CST_visitor.visualization_visitor import VisualizationVisitor

from src.parser.ast import Ast
from src.parser import optimizations as optim
from src.antlr_files.C_GrammarLexer import *
from src.antlr_files.C_GrammarParser import *
from src.antlr_files.C_GrammarVisitor import *
from src.parser.visitor.AST_visitor import *

"""
flags to implement: 
disable-cfold : disable constant folding (should be enabled by default)
disable-cprog: disable constant propagation (should be enabled by default)
viz-cst: visualize CST
viz-ast visualize AST and symbol tables
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


'''
TODO: 
    * Documentation
    * Add constant propagation in adherence to const casting
    * Add derefencing detection so the pointerConstReassignment test passes
    * Explicit conversions
'''
def main(argv):
    pass_tests = Path("example_source_files").glob('proj2_*_pass_*.c')
    #syntaxErr_tests = Path("../../example_source_files").glob('proj2_*_syntaxErr_*.c')
    for path in pass_tests:
        path_in_str = str(path)
        tokens = getTokens(path_in_str)
        parser = C_GrammarParser(tokens)
        #parser.addErrorListener(MyErrorListener())
        tree = parser.program()

        #visualizeCST(tree, parser.ruleNames, os.path.basename(path))

        ast = getAST(tree)
        applyConstantFolding(ast)
        try:
            SymbolTableVisitor(ast)
            TypeCheckerVisitor(ast)
        except SemanticError as e:
            print(f"{e}")
        visualizeAST(ast, os.path.basename(path) + ".gv")



if __name__ == '__main__':
    main(sys.argv)
