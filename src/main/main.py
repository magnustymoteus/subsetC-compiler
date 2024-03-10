import os
from pathlib import Path


from src.parser.visitor.CST_visitor.cst_to_ast_visitor import CSTToASTVisitor
from src.parser.visitor.CST_visitor.visualization_visitor import VisualizationVisitor

from src.parser.AST.ast import Ast
from src.parser import optimizations as optim
from src.antlr_files.C_GrammarLexer import *
from src.antlr_files.C_GrammarParser import *
from src.antlr_files.C_GrammarVisitor import *
from src.parser.visitor.AST_visitor import *
from src.llvm_target import *
from src.parser.optimizations import *

"""
flags to implement: 
disable-cfold : disable constant folding (should be enabled by default)
disable-cprog: disable constant propagation (should be enabled by default)
viz-cst: visualize CST
viz-ast visualize AST and symbol tables
"""

# Gives filepath to C_GrammarLexer to generate tokens
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

def visualizeCFG(cfg: ControlFlowGraph, filename: str):
    graph = cfg.to_dot_graph()
    graph.save(filename=filename)


'''
TODO: 
    * Documentation
    * Add constant propagation in adherence to const casting
    * AST to Control Flow Graph (useful for dead code analysis, constant propagation, ...)
    * AST node has a line and a column
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
        try:
            SymbolTableVisitor(ast)
            TypeCheckerVisitor(ast)
        except SemanticError as e:
            print(f"{e}")
        OptimizationVisitor(ast)
        applyConstantFolding(ast)
        #visualizeAST(ast, os.path.basename(path) + ".gv")
        cfg: ControlFlowGraph = BasicBlockVisitor(ast).cfg
        TACVisitor(cfg)
        visualizeCFG(cfg, "cfg-viz/" + str(os.path.basename(path)) + ".gv")



if __name__ == '__main__':
    main(sys.argv)
