from src.compilation import *
from src.constructs import *

from src.antlr_files.C_GrammarLexer import *
from src.antlr_files.C_GrammarVisitor import *

from llvmlite.binding import *
from pathlib import Path
from argparse import Namespace
import graphviz

class Compiler():
    @staticmethod
    def getTokens(source_code: str):
        lexer = C_GrammarLexer(InputStream(source_code))
        stream = CommonTokenStream(lexer)
        return stream
    @staticmethod
    def getAST(tree, tokens) -> Ast:
        ast = Ast()
        converterVisitor = CSTToASTVisitor(tokens)
        root = converterVisitor.visit(tree)
        ast.set_root(root)
        return ast
    @staticmethod
    def visualizeCST(tree, rules, filename):
        visualizationVisitor = VisualizationVisitor()
        visualizationVisitor.visualize(tree, rules, filename)
    @staticmethod
    def visualizeAST(ast: Ast, filename: str):
        graph = ast.to_dot_graph()
        graph.save(filename=filename)
    @staticmethod
    def visualizeCFG(cfg: ControlFlowGraph, filename: str):
        graph = cfg.to_dot_graph()
        graph.save(filename=filename)
    @staticmethod
    def getPreprocessor(filepath):
        input_stream = FileStream(filepath)
        lexer = C_PreprocessorLexer(input_stream)
        stream = CommonTokenStream(lexer)
        tree = C_PreprocessorParser(stream).program()
        preprocessor = PreprocessorVisitor(stream, filepath)
        preprocessor.visit(tree)
        return preprocessor

    def __init__(self):
        self.disable: set[str] = set()
        self.viz: set[str] = set()

    def do_viz(self, what: str):
        return "all" in self.viz or what in self.viz
    def is_disabled(self, what: str):
        return what in self.disable

    def compile_mips(self, llvm_module: ir.Module,filepath: Path):
        pass

    def compile_llvm(self, filepath: Path) -> ir.Module:
        filename = str(os.path.splitext(os.path.basename(filepath))[0])
        preprocessor = Compiler.getPreprocessor(filepath)
        # Lexes the input file
        tokens = Compiler.getTokens(preprocessor.get_processed_result())
        parser = C_GrammarParser(tokens)
        parser.addErrorListener(MyErrorListener())

        # tree: list[ProgramContext]
        tree = parser.program()

        if self.do_viz("cst"):
            Compiler.visualizeCST(tree, parser.ruleNames, f"./{filename}-viz/cst")
        # conversion from CST to AST
        ast = Compiler.getAST(tree, tokens)
        ResolverVisitor(ast, preprocessor.included_stdio)


        if self.do_viz("ast"):
            Compiler.visualizeAST(ast, f"./{filename}-viz/ast.gv")

        # Makes symbol table entries of the ast nodes
        SymbolTableVisitor(ast)
        if self.do_viz("ast"):
            Compiler.visualizeAST(ast, f"./{filename}-viz/ast.gv")
        TypeCheckerVisitor(ast)

        SimplifierVisitor(ast)

        if not self.is_disabled("cprop"):
            ConstantPropagationVisitor(ast)

        if not self.is_disabled("cfold"):
            ConstantFoldingVisitor(ast)

        DeadCodeVisitor(ast)

        MainChecker(ast)

        if self.do_viz("ast"):
            Compiler.visualizeAST(ast, f"./{filename}-viz/ast.gv")

        cfg: ControlFlowGraph = BasicBlockVisitor(ast).cfg

        TACVisitor(cfg)

        if self.do_viz("ast"):
            Compiler.visualizeAST(ast, f"./{filename}-viz/tac.gv")

        if self.do_viz("cfg"):
            Compiler.visualizeCFG(cfg, f"./{filename}-viz/cfg.gv")

        llvm = LLVMVisitor(ast, filename, self.is_disabled("comments"))

        if self.do_viz("cfg"):
            for function in llvm.module.functions:
                pass
                '''s = graphviz.Source(get_function_cfg(function), filename=f"./{filename}-viz/{function.name}_llvm_cfg.gv")
                s.save()'''

        return llvm.module


    def export_llvm(self, llvm_module: ir.Module, filepath: Path):
        output_path = str(os.path.splitext(os.path.basename(filepath))[0])
        llvm_file = Path(f"{output_path}.ll")
        llvm_file.parent.mkdir(parents=True, exist_ok=True)
        f = open(f"./{output_path}.ll", "w")
        f.write(str(llvm_module))
        f.close()