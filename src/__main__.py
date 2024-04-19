from pathlib import Path
import argparse
import warnings

from src.antlr_files.C_PreprocessorLexer import C_PreprocessorLexer
from src.compilation import *
from src.constructs import *

from src.antlr_files.C_GrammarLexer import *
from src.antlr_files.C_GrammarParser import *
from src.antlr_files.C_GrammarVisitor import *

from llvmlite.binding import *
import graphviz


# Gives filepath to C_GrammarLexer to generate tokens
def getTokens(source_code: str):
    lexer = C_GrammarLexer(InputStream(source_code))
    stream = CommonTokenStream(lexer)
    return stream


def getAST(tree, tokens) -> Ast:
    ast = Ast()
    converterVisitor = CSTToASTVisitor(tokens)
    root = converterVisitor.visit(tree)
    ast.set_root(root)
    return ast


def visualizeCST(tree, rules, filename):
    visualizationVisitor = VisualizationVisitor()
    visualizationVisitor.visualize(tree, rules, filename)

def visualizeAST(ast: Ast, filename: str):
    graph = ast.to_dot_graph()
    graph.save(filename=filename)

def visualizeCFG(cfg: ControlFlowGraph, filename: str):
    graph = cfg.to_dot_graph()
    graph.save(filename=filename)

def getPreprocessedCode(filepath):
    input_stream = FileStream(filepath)
    lexer = C_PreprocessorLexer(input_stream)
    stream = CommonTokenStream(lexer)
    tree = C_PreprocessorParser(stream).program()
    preprocessor = PreprocessorVisitor(stream, filepath)
    preprocessor.visit(tree)
    return preprocessor.get_processed_result()


def c_file(param):
    base, ext = os.path.splitext(param)
    if ext.lower() not in ('.c'):
        raise argparse.ArgumentTypeError('File must be a .c file')
    return param

# TODO: extra checks for jump statements not in loops or switch
# TODO: line numbers in errors/warnings for source code with includes is off
# TODO: check if return is called for non void functions in all paths

def main(argv):
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--disable-cfold', action='store_true',
                            help='disable constant folding')
    arg_parser.add_argument('--disable-cprop', action='store_true',
                            help='disable constant propagation')
    arg_parser.add_argument('--disable-comments', action='store_true', help="disable comments attached to instructions")

    arg_parser.add_argument('--disable-warnings', action='store_true')

    arg_parser.add_argument('--viz-all', action='store_true', help="visualize everything (CST, AST, CFG, symtabs)")
    arg_parser.add_argument("--viz-cst", action="store_true", help="visualize concrete syntax tree (CST)")
    arg_parser.add_argument("--viz-cfg", action="store_true", help="visualize control flow graph (CFG)")
    arg_parser.add_argument( '--viz-ast', action='store_true', help='visualize abstract syntax tree (AST)')
    arg_parser.add_argument( '--viz-symtab', action='store_true', help='visualize symbol tables (symtabs)')


    arg_parser.add_argument('--path', type=c_file, required=True, help="glob path of the .c file(s) to be compiled")

    arg_parser.add_argument('--targets', choices=["llvm", "mips"], nargs="+", required=True, help="Choose 1 or more languages to compile to")
    args = arg_parser.parse_args(argv[1:])

    #warnings.filterwarnings("error")
    pass_tests = Path.cwd().glob(args.path)
    for path in pass_tests:
        path_in_str = str(path)
        filename = str(os.path.splitext(os.path.basename(path))[0])
        try:
            preprocessed_code = getPreprocessedCode(path_in_str)
            # Lexes the input file
            tokens = getTokens(preprocessed_code)
            parser = C_GrammarParser(tokens)
            parser.addErrorListener(MyErrorListener())

            # tree: list[ProgramContext]
            tree = parser.program()

            if args.viz_cst or args.viz_all:
                visualizeCST(tree, parser.ruleNames, f"./{filename}-viz/cst")
            # conversion from CST to AST
            ast = getAST(tree, tokens)

            ResolverVisitor(ast)

            # Makes symbol table entries of the ast nodes
            SymbolTableVisitor(ast)
            TypeCheckerVisitor(ast)

            if not args.disable_cprop:
                ConstantPropagationVisitor(ast)

            if not args.disable_cfold:
                ConstantFoldingVisitor(ast)

            DeadCodeVisitor(ast)

            if args.viz_ast or args.viz_all:
                visualizeAST(ast, f"./{filename}-viz/ast.gv")

            cfg: ControlFlowGraph = BasicBlockVisitor(ast).cfg

            TACVisitor(cfg)

            if args.viz_cfg or args.viz_all:
                visualizeCFG(cfg, f"./{filename}-viz/cfg.gv")

            llvm = LLVMVisitor(ast, filename, args.disable_comments)

            if args.viz_cfg or args.viz_all:
                for function in llvm.module.functions:
                    pass
                    '''s = graphviz.Source(binding.get_function_cfg(function), filename=f"./{filename}-viz/{function.name}_llvm_cfg.gv")
                    s.save()'''

            for target in args.targets:
                match target:
                    case "llvm":
                        llvm_file = Path(f"{filename}.ll")
                        llvm_file.parent.mkdir(parents=True, exist_ok=True)
                        f = open(f"./{filename}.ll", "w")
                        f.write(str(llvm.module))
                        f.close()
                    case "mips":
                        warnings.warn("compiling to MIPS is currently not supported")
                    case _:
                        warnings.warn("unsupported compilation target")

        except PreprocessingError as e:
            print(f"{path_in_str}:{e}")
        except SyntaxError as e:
            print(f"{path_in_str}:{e}")
        except SemanticError as e:
            print(f"{path_in_str}:{e}")
        except Warning as w:
            if not args.disable_warnings:
                print(f"{path_in_str}:{w}")


if __name__ == '__main__':
    main(sys.argv)
