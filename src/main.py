import antlr4.tree.Trees
from antlr4 import *
from C.gen.CLexer import *
from C.gen.CParser import *


def tokenizeInput(input_stream):
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    return stream


def parseTokens(token_stream):
    parser = CParser(token_stream)
    return parser.expression()


# can run with "python src/main.py 'pathtoCprogram.c' -s"
def main(argv):
    input_stream = FileStream(argv[1])
    tokens = tokenizeInput(input_stream)
    tree = parseTokens(tokens)


if __name__ == '__main__':
    main(sys.argv)
