import os
from pathlib import Path
import argparse

from src.parser.visitor.CST_visitor.cst_to_ast_visitor import CSTToASTVisitor
from src.parser.visitor.CST_visitor.visualization_visitor import VisualizationVisitor

from src.parser import optimizations as optim
from src.antlr_files.C_GrammarLexer import *
from src.antlr_files.C_GrammarParser import *
from src.antlr_files.C_GrammarVisitor import *
from src.parser.visitor.AST_visitor import *
from src.llvm_target import *
from src.parser.optimizations import *


# Gives filepath to C_GrammarLexer to generate tokens
def getTokens(filepath: str):
    input_stream = FileStream(filepath)
    lexer = C_GrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    return stream


def visualizeCST(tree, rules, filename):
    visualizationVisitor = VisualizationVisitor()
    visualizationVisitor.visualize(tree, rules, filename)


def getAST(tree, tokens) -> Ast:
    ast = Ast()
    converterVisitor = CSTToASTVisitor(tokens)
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


def main(argv):
    # Flags
    """
    disable-cfold : disable constant folding (should be enabled by default)
    disable-cprog: disable constant propagation (should be enabled by default)
    viz-cst: visualize CST
    viz-ast: visualize AST and symbol tables
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--disable-cfold', action='store_true',
                            help='disable constant folding (enabled by default)')
    arg_parser.add_argument('--disable-cprog', action='store_true',
                            help='disable constant propagation (enabled by default)')
    arg_parser.add_argument('--viz-cst', action='store_true', help='visualize CST')
    arg_parser.add_argument('--viz-ast', action='store_true', help='visualize AST and symbol tables')
    args = arg_parser.parse_args(argv[1:])

    # pass_tests = Path("example_source_files").glob('proj2_*_pass_*.c')
    pass_tests = Path("example_source_files").glob('*pass*.c')
    # syntaxErr_tests = Path("../../example_source_files").glob('proj2_*_syntaxErr_*.c')
    for path in pass_tests:
        path_in_str = str(path)
        # Lexes the input file
        tokens = getTokens(path_in_str)

        parser = C_GrammarParser(tokens)

        # parser.addErrorListener(MyErrorListener())

        # tree: list[ProgramContext]
        tree = parser.program()

        if args.viz_cst:
            visualizeCST(tree, parser.ruleNames, os.path.basename(path))

        # conversion from CST to AST
        ast = getAST(tree, tokens)

        try:
            # Makes symbol table entries of the ast nodes
            SymbolTableVisitor(ast)
            TypeCheckerVisitor(ast)

        except SemanticError as e:
            print(f"{e}")

        if not args.disable_cprog:
            OptimizationVisitor(ast)

        if not args.disable_cfold:
            applyConstantFolding(ast)

        if args.viz_ast:
            visualizeAST(ast, os.path.basename(path) + ".gv")

        cfg: ControlFlowGraph = BasicBlockVisitor(ast).cfg
        visualizeCFG(cfg, "viz/cfg-processed/" + str(os.path.basename(path)) + ".gv")
        TACVisitor(cfg)
        visualizeCFG(cfg, "viz/tac-processed/" + str(os.path.basename(path)) + ".gv")
        llvm = LLVMVisitor(cfg, os.path.basename(path))
        visualizeCFG(cfg, "viz/llvm-processed/" + str(os.path.basename(path)) + ".gv")

        llvm_file = Path(f"src/llvm_target/output/{str(os.path.basename(path))}.ll")
        llvm_file.parent.mkdir(parents=True, exist_ok=True)
        f = open(f"src/llvm_target/output/{str(os.path.basename(path))}.ll", "w")
        f.write(str(llvm.module))
        f.close()


if __name__ == '__main__':
    main(sys.argv)
