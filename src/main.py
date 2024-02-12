from antlr4 import *
import sys
import C.gen.CLexer as CLexer
import C.gen.CParser as CParser

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = CLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.start_()

if __name__ == '__main__':
    main(sys.argv)




