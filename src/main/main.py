import sys

from src.parser import Ast, AstBasicNode
from antlr4.tree.Trees import Trees
from antlr4 import *
from src.antlr_files.C_ExpressionsParser import *
from src.antlr_files.C_ExpressionsLexer import *
from src.main.visitor.main_visitor import *

def tokenizeInput(input_stream):
    lexer = C_ExpressionsLexer(input_stream)
    stream = CommonTokenStream(lexer)
    return stream


def parseTokens(token_stream):
    parser = C_ExpressionsParser(token_stream)
    return parser


def main(argv):
    input_stream = FileStream("example_source_files/proj1_man_pass_constantFolding.c")
    tokens = tokenizeInput(input_stream)
    parser = parseTokens(tokens)
    tree = parser.expr()
    visitor = MainVisitor()
    visitor.visit(tree)


if __name__ == '__main__':
    main(sys.argv)
