import sys

from src.main.visitor.CST_visitor.visualization_visitor import VisualizationVisitor
from src.parser import *
from src.parser import optimizations as optim
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

    ast = Ast()
    n1: NodeWrapper[AstBinOpNode] = wrap(AstBinOpNode("+"))
    n2: NodeWrapper[AstBinOpNode] = wrap(AstBinOpNode("+"))
    n3: NodeWrapper[AstLiteralNode] = wrap(AstLiteralNode(1))
    n4: NodeWrapper[AstLiteralNode] = wrap(AstLiteralNode(2))
    n5: NodeWrapper[AstUnOpNode] = wrap(AstUnOpNode("-"))
    n6: NodeWrapper[AstLiteralNode] = wrap(AstLiteralNode(3))

    ast.set_root(n1)
    n1.n.lhs_w = n2
    n1.n.rhs_w = n3
    n2.n.lhs_w = n4
    n2.n.rhs_w = n5
    n5.n.operand_w = n6

    optim.constant_folding(ast)

    graph = ast.to_dot_graph()
    graph.save(filename="graph.gv")

    for node in ast.iter(AstIterPostorder):
        print(node.n)


if __name__ == '__main__':
    main(sys.argv)
