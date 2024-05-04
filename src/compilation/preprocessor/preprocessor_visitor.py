from __future__ import annotations
from src.constructs.node import *
from antlr4.Token import CommonToken

from src.antlr_files.C_PreprocessorParser import *
from src.antlr_files.C_PreprocessorLexer import *
from src.antlr_files.C_PreprocessorVisitor import *
from antlr4.TokenStreamRewriter import *
import os

class PreprocessingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class EnvironmentNode():
    def __init__(self, filename: str, line_pair: tuple[int, int]):
        self.filename: str = filename
        self.line_pair : tuple[int, int] = line_pair
        self.children: list[EnvironmentNode] = []
    # returns environment and translated line
    def get_env(self, line: int) -> tuple[EnvironmentNode, int]:
        result_line = line
        for child in self.children:
            if child.line_pair[0] <= line <= child.line_pair[1]:
                return child.get_env(line-child.line_pair[0]+1)
            elif child.line_pair[1] > line:
                break
            result_line -= (child.line_pair[1]-child.line_pair[0])
        return self, result_line


class PreprocessorVisitor(C_PreprocessorVisitor):
    def raise_preprocessing_error(self, message: str, ctx):
        raise PreprocessingError(f"{self.filepath}:{ctx.start.line}:{ctx.start.column}:error: {message}")
    @staticmethod
    def get_original_text(ctx) -> str:
        return ctx.parser.getInputStream().getText(ctx.start, ctx.stop)
    def __init__(self, token_stream: CommonTokenStream, filepath: str, defines: dict[str, str]={}):
        self.filepath = filepath
        self.defines: dict[str, str] = defines
        self.rewriter = TokenStreamRewriter(token_stream)
        self.ifndef_stack: list[tuple[int, bool]] = [] # contains line for the end of the endif directive token

        self.included_stdio = False

        self.include_sizes: list[int] = []


    def visitProgram(self, ctx: C_PreprocessorParser.ProgramContext):
        self.environment_node: EnvironmentNode = EnvironmentNode(self.filepath, (ctx.start.line, ctx.stop.line))
        super().visitProgram(ctx)
        if len(self.ifndef_stack) > 0:
            self.raise_preprocessing_error("Unterminated #if", ctx)


    def visitLine(self, ctx:C_PreprocessorParser.LineContext):
        self.visitChildren(ctx)
    def visitDefineDirective(self, ctx:C_PreprocessorParser.DefineDirectiveContext):
        self.defines[ctx.getChild(1).getText()] = PreprocessorVisitor.get_original_text(ctx.getChild(2))
        self.rewriter.delete("default", ctx.start.tokenIndex, ctx.stop.tokenIndex)
    def visitIncludeDirective(self, ctx:C_PreprocessorParser.IncludeDirectiveContext):
        is_library: bool = ctx.getChild(1).getText()[0] == '<'
        incomplete_path: str = ctx.getChild(1).getText()[1:-1]
        if not is_library:
            included_path = os.path.join(os.path.dirname(self.filepath), incomplete_path)
            if not os.path.exists(included_path):
                self.raise_preprocessing_error(f"{included_path}: No such file", ctx)

            tokens = C_PreprocessorLexer(FileStream(included_path))
            stream = CommonTokenStream(tokens)
            tree = C_PreprocessorParser(stream).program()
            sub_preprocessor = PreprocessorVisitor(stream, included_path, self.defines)
            sub_preprocessor.visit(tree)

            new_include = sub_preprocessor.rewriter.getTokenStream().get(-1).line - len(sub_preprocessor.include_sizes) + sum(sub_preprocessor.include_sizes)
            self.include_sizes.append(new_include)
            start_end: tuple[int, int] = (ctx.start.line + sum(self.include_sizes[:-1]) - (len(self.include_sizes) - 1),
                                          ctx.start.line + sum(self.include_sizes) - len(self.include_sizes))

            sub_preprocessor.environment_node.line_pair = start_end
            self.environment_node.children.append(sub_preprocessor.environment_node)

            self.defines = self.defines | sub_preprocessor.defines
            self.rewriter.replace("default", ctx.start.tokenIndex, ctx.stop.tokenIndex, sub_preprocessor.get_processed_result())

        else:
            self.included_stdio = incomplete_path == "stdio.h"
            if not self.included_stdio:
                self.raise_preprocessing_error(f"library {incomplete_path} not supported", ctx)
            self.rewriter.delete("default", ctx.start.tokenIndex, ctx.stop.tokenIndex)
    def visitTerminal(self, node):
        defined = self.defines.get(node.getText(), False)
        if defined:
            interval = node.getSourceInterval()
            self.rewriter.replace("default", interval[0], interval[1], defined)
    def get_processed_result(self):
        return self.rewriter.getDefaultText()
    def visitIfndefDirective(self, ctx:C_PreprocessorParser.IfndefDirectiveContext):
        is_not_defined: bool = self.defines.get(ctx.getChild(1).getText(), None) is None
        self.ifndef_stack.append((ctx.stop.tokenIndex, is_not_defined))
        self.rewriter.delete("default", ctx.start.tokenIndex, ctx.stop.tokenIndex)
    def visitEndifDirective(self, ctx:C_PreprocessorParser.EndifDirectiveContext):
        if self.ifndef_stack == 0:
            self.raise_preprocessing_error(f"#endif without #if", ctx)
        ifndef = self.ifndef_stack.pop()
        removal_start_index: int = ctx.start.tokenIndex
        if not ifndef[1]:
            removal_start_index = ifndef[0]+1
        self.rewriter.delete("default", removal_start_index, ctx.stop.tokenIndex)
