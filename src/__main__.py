import os
from pathlib import Path
import argparse
import warnings

from src.parser.visitor.CST_visitor.cst_to_ast_visitor import CSTToASTVisitor
from src.parser.visitor.CST_visitor.visualization_visitor import VisualizationVisitor

from src.parser import optimizations as optim
from src.antlr_files.C_GrammarLexer import *
from src.antlr_files.C_GrammarParser import *
from src.antlr_files.C_GrammarVisitor import *
from src.parser.listener.error_listener import *
from src.parser.visitor.AST_visitor import *
from src.llvm_target import *
from src.parser.optimizations import *



# Gives filepath to C_GrammarLexer to generate tokens
def getTokens(filepath: str):
    input_stream = FileStream(filepath)
    lexer = C_GrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    return stream


def getAST(tree, tokens) -> Ast:
    ast = Ast()
    converterVisitor = CSTToASTVisitor(tokens)
    root = converterVisitor.visit(tree)
    ast.set_root(root)
    return ast


def applyConstantFolding(ast: Ast):
    optim.constant_folding(ast)

def visualizeCST(tree, rules, filename):
    visualizationVisitor = VisualizationVisitor()
    visualizationVisitor.visualize(tree, rules, filename)

def visualizeAST(ast: Ast, filename: str):
    graph = ast.to_dot_graph()
    graph.save(filename=filename)

def visualizeCFG(cfg: ControlFlowGraph, filename: str):
    graph = cfg.to_dot_graph()
    graph.save(filename=filename)

def c_file(param):
    base, ext = os.path.splitext(param)
    if ext.lower() not in ('.c'):
        raise argparse.ArgumentTypeError('File must be a .c file')
    return param

# TODO: put visit() in node classes themselves instead of in visitors
def main(argv):
    # Flags
    """
    disable-cfold : disable constant folding (should be enabled by default)
    disable-cprop: disable constant propagation (should be enabled by default)
    viz: visualize CST, AST, CFG, symbol tables
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--disable-cfold', action='store_true',
                            help='disable constant folding')
    arg_parser.add_argument('--disable-cprop', action='store_true',
                            help='disable constant propagation')

    arg_parser.add_argument('--disable-warnings', action='store_true')


    arg_parser.add_argument( '--viz', action='store_true', help='visualize CST, AST, CFG, symbol tables')

    arg_parser.add_argument('--path', type=c_file, required=True, help="glob path of the .c file(s) to be compiled")

    target = arg_parser.add_mutually_exclusive_group(required=True)
    target.add_argument('--target-llvm', action='store_true')
    target.add_argument('--target-mips', action='store_true')
    args = arg_parser.parse_args(argv[1:])

    warnings.filterwarnings("error")
    pass_tests = Path.cwd().glob(args.path)
    for path in pass_tests:
        path_in_str = str(path)
        filename = str(os.path.splitext(os.path.basename(path))[0])
        try:
            # Lexes the input file
            tokens = getTokens(path_in_str)
            parser = C_GrammarParser(tokens)
            parser.addErrorListener(MyErrorListener())

            # tree: list[ProgramContext]
            tree = parser.program()

            if args.viz:
                visualizeCST(tree, parser.ruleNames, f"./{filename}-viz/cst")

            # conversion from CST to AST
            ast = getAST(tree, tokens)

            # Makes symbol table entries of the ast nodes
            SymbolTableVisitor(ast)
            TypeCheckerVisitor(ast)

            if not args.disable_cprop:
                OptimizationVisitor(ast)

            if not args.disable_cfold:
                ConstantFoldingVisitor(ast)

            if args.viz:
                visualizeAST(ast, f"./{filename}-viz/ast.gv")

            cfg: ControlFlowGraph = BasicBlockVisitor(ast).cfg

            if args.viz:
                visualizeCFG(cfg, f"./{filename}-viz/ast_cfg.gv")

            TACVisitor(cfg)

            if args.viz:
                visualizeCFG(cfg, f"./{filename}-viz/ast_tac.gv")

            llvm = LLVMVisitor(cfg, filename)

            if args.target_llvm:
                llvm_file = Path(f"{filename}.ll")
                llvm_file.parent.mkdir(parents=True, exist_ok=True)
                f = open(f"./{filename}.ll", "w")
                f.write(str(llvm.module))
                f.close()
            elif args.target_mips:
                warnings.warn("compiling to MIPS is currently not supported")

        except SyntaxError as e:
            print(f"{path_in_str}:{e}")
        except SemanticError as e:
            print(f"{path_in_str}:{e}")
        except Warning as w:
            if not args.disable_warnings:
                print(f"{path_in_str}:{w}")


if __name__ == '__main__':
    main(sys.argv)
