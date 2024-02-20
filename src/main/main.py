import sys

from src.main.visitor.CST_visitor.visualization_visitor import VisualizationVisitor
from src.parser import Ast, AstBasicNode
from src.antlr_files.C_ExpressionsLexer import *

from src.main.visitor.main_visitor import *
from src.main.visitor.CST_visitor.collapser_visitor import *
from src.main.visitor.CST_visitor.collapser_visitor import *

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
    tree = parser.statement()
    rules = parser.ruleNames
    collapserVisitor = CollapserVisitor()
    collapsed = collapserVisitor.getCollapsedCST(tree)
    visualizationVisitor = VisualizationVisitor()
    visualized = visualizationVisitor.visualize(collapsed, rules, 'collapsed_tree')


if __name__ == '__main__':
    main(sys.argv)
