from src.compilation import *
from src.constructs import *
from src.constructs.mips_program import MipsProgram
from src.compilation.visualization import CSTVisualizer, SymbolTablesVisualizer

from src.antlr_files.C_GrammarLexer import *
from src.antlr_files.C_GrammarVisitor import *

from llvmlite.binding import *
from pathlib import Path

import graphviz
import subprocess


class Compiler:
    @staticmethod
    def getTokens(source_code: str):
        lexer = C_GrammarLexer(InputStream(source_code))
        stream = CommonTokenStream(lexer)
        return stream

    @staticmethod
    def getAST(tree, tokens, environment_root: EnvironmentNode) -> Ast:
        ast = Ast()
        converterVisitor = CSTToASTVisitor(tokens, environment_root)
        root = converterVisitor.visit(tree)
        ast.set_root(root)
        return ast

    @staticmethod
    def visualizeCST(tree, rules, filename):
        visualizer = CSTVisualizer()
        visualizer.visualize(tree, rules, filename)

    @staticmethod
    def visualizeAST(ast: Ast, filename: str):
        graph = ast.to_dot_graph()
        graph.render(filename=filename, format="png", cleanup=True)
        graph.render(filename=filename, format="gv", cleanup=True)

    @staticmethod
    def visualizeSymTabs(ast: Ast, filename: str):
        visualizer = SymbolTablesVisualizer(ast)
        visualizer.graph.render(filename=filename, format="png",  cleanup=True)
        visualizer.graph.render(filename=filename, format="gv",  cleanup=True)

    @staticmethod
    def visualizeCFG(cfg: ControlFlowGraph, filename: str):
        graph = cfg.to_dot_graph()
        graph.render(filename=filename, format="png",  cleanup=True)
        graph.render(filename=filename, format="gv",  cleanup=True)


    @staticmethod
    def getPreprocessor(filepath):
        input_stream = FileStream(filepath)
        lexer = C_PreprocessorLexer(input_stream)
        stream = CommonTokenStream(lexer)
        tree = C_PreprocessorParser(stream).program()
        preprocessor = PreprocessorVisitor(stream, filepath)
        preprocessor.visit(tree)
        return preprocessor

    def __init__(self, disable=None, viz=None):
        self.disable: set[str] = disable if disable is not None else set()
        self.viz: set[str] = viz if viz is not None else set()

    def do_viz(self, what: str):
        return "all" in self.viz or what in self.viz

    def is_disabled(self, what: str):
        return what in self.disable

    def compile_mips(self, llvm_module: ir.Module) -> MipsProgram:
        mips_visitor = MipsVisitor()
        mips_visitor.visit(llvm_module)
        return mips_visitor.tree

    def compile_llvm(self, filepath: Path) -> ir.Module:
        filename = str(os.path.splitext(os.path.basename(filepath))[0])
        preprocessor = Compiler.getPreprocessor(filepath)
        # Lexes the input file
        tokens = Compiler.getTokens(preprocessor.get_processed_result())
        parser = C_GrammarParser(tokens)
        parser.addErrorListener(MyErrorListener(preprocessor.environment_node))

        # tree: list[ProgramContext]
        tree = parser.program()

        if self.do_viz("cst"):
            Compiler.visualizeCST(tree, parser.ruleNames, f"./{filename}/viz/cst")
        # conversion from CST to AST
        ast = Compiler.getAST(tree, tokens, preprocessor.environment_node)
        ResolverVisitor(ast, preprocessor.included_stdio)

        SimplifierVisitor(ast)

        # Makes symbol table entries of the ast nodes
        SymbolTableVisitor(ast)
        TypeCheckerVisitor(ast)

        if not self.is_disabled("cprop"):
            ConstantPropagationVisitor(ast)

        if not self.is_disabled("cfold"):
            ConstantFoldingVisitor(ast)

        if not self.is_disabled("dcode"):
            DeadCodeVisitor(ast)

        if self.do_viz("ast"):
            Compiler.visualizeAST(ast, f"./{filename}/viz/ast")
        if self.do_viz("symtab"):
            Compiler.visualizeSymTabs(ast, f"./{filename}/viz/symtab")

        cfg: ControlFlowGraph = BasicBlockVisitor(ast).cfg

        TACVisitor(cfg)

        if self.do_viz("cfg"):
            Compiler.visualizeCFG(cfg, f"./{filename}/viz/cfg")

        llvm = LLVMVisitor(ast, filename, self.is_disabled("comments"), preprocessor.included_stdio)

        if self.do_viz("cfg"):
            for function in llvm.module.functions:
                s = graphviz.Source(
                    get_function_cfg(function), filename=f"./{filename}/viz/{function.name}_llvm_cfg.gv"
                )
                s.save()
        return llvm.module

    def export_llvm(self, llvm_module: ir.Module, filepath: Path):
        filepath.parent.mkdir(parents=True, exist_ok=True)
        f = open(f"{str(filepath)}", "w")
        f.write(str(llvm_module))
        f.close()

    def export_mips(self, program: MipsProgram, filepath: Path):
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(f"{str(filepath)}", "w") as f:
            f.write(program.to_asm())
        f.close()
