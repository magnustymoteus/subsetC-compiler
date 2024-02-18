import sys
from antlr4.tree.Trees import Trees
from antlr4 import *
from src.antlr_files.C_ExpressionsParser import *
from src.antlr_files.C_ExpressionsLexer import *

def tokenizeInput(input_stream):
    lexer = C_ExpressionsLexer(input_stream)
    stream = CommonTokenStream(lexer)
    return stream


def parseTokens(token_stream):
    parser = C_ExpressionsParser(token_stream)
    return parser


# can run with "python src/main.py 'pathtoCprogram.c' -s"
def main(argv):
    input_stream = FileStream("example_source_files/proj1_man_pass_constantFolding.c")
    tokens = tokenizeInput(input_stream)
    parser = parseTokens(tokens)
    tree = parser.expr()
    print(Trees.toStringTree(tree, None, parser))

if __name__ == '__main__':
    main(sys.argv)
