import sys

from src.main.visitor.CST_visitor.cst_to_ast_visitor import CSTToASTVisitor
from src.main.visitor.CST_visitor.visualization_visitor import VisualizationVisitor

from src.parser import *
from src.parser import optimizations as optim
from src.antlr_files.C_ExpressionsLexer import *
from src.antlr_files.C_ExpressionsParser import *
from src.antlr_files.C_ExpressionsVisitor import *

def tokenizeInput(input_stream):
    lexer = C_ExpressionsLexer(input_stream)
    stream = CommonTokenStream(lexer)
    return stream


def parseTokens(token_stream):
    parser = C_ExpressionsParser(token_stream)
    return parser


def main(argv):
    input_stream = FileStream("example_source_files/proj1_man_pass_operators.c")
    tokens = tokenizeInput(input_stream)
    parser = parseTokens(tokens)
    tree = parser.program()
    rules = parser.ruleNames

    visualizationVisitor = VisualizationVisitor()
    visualizationVisitor.visualize(tree, rules, "raw-CST")

    converterVisitor = CSTToASTVisitor()
    ast = Ast()
    root = converterVisitor.visit(tree)
    ast.set_root(root)
    graph = ast.to_dot_graph()
    graph.save(filename="AST.gv")

    optim.constant_folding(ast)


    graph = ast.to_dot_graph()
    graph.save(filename="AST_constant_fold.gv")

    #for node in ast.iter(AstIterPostorder):
    #     print(node.n)


if __name__ == '__main__':
    main(sys.argv)
