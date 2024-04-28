from src.antlr_files.C_PreprocessorParser import *
from src.antlr_files.C_PreprocessorLexer import *
from src.antlr_files.C_PreprocessorVisitor import *
from antlr4.TokenStreamRewriter import *
import os

class PreprocessingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
class PreprocessorVisitor(C_PreprocessorVisitor):
    def raise_preprocessing_error(self, message: str, ctx):
        raise PreprocessingError(f"{ctx.start.line}:{ctx.start.column}:error: {message}")
    @staticmethod
    def get_original_text(ctx) -> str:
        return ctx.parser.getInputStream().getText(ctx.start, ctx.stop)
    def __init__(self, buffered_tokens_stream: BufferedTokenStream, filepath: str, defines: dict[str, str]={}):
        self.filepath = filepath
        self.defines: dict[str, str] = defines
        self.rewriter = TokenStreamRewriter(buffered_tokens_stream)
        self.ifndef_stack_stack: list[tuple[int, bool]] = [] # contains line for the end of the endif directive token
        self.included_stdio = False
    def visitProgram(self, ctx: C_PreprocessorParser.ProgramContext):
        super().visitProgram(ctx)
        if len(self.ifndef_stack_stack) > 0:
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

            included_contents = open(included_path, 'r').read()
            tokens = C_PreprocessorLexer(InputStream(included_contents))
            stream = CommonTokenStream(tokens)
            tree = C_PreprocessorParser(stream).program()
            sub_preprocessor = PreprocessorVisitor(stream, included_path, self.defines)
            sub_preprocessor.visit(tree)
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
        self.ifndef_stack_stack.append((ctx.stop.tokenIndex, is_not_defined))
        self.rewriter.delete("default", ctx.start.tokenIndex, ctx.stop.tokenIndex)
    def visitEndifDirective(self, ctx:C_PreprocessorParser.EndifDirectiveContext):
        if self.ifndef_stack_stack == 0:
            self.raise_preprocessing_error(f"#endif without #if", ctx)
        ifndef = self.ifndef_stack_stack.pop()
        removal_start_index: int = ctx.start.tokenIndex
        if not ifndef[1]:
            removal_start_index = ifndef[0]+1
        self.rewriter.delete("default", removal_start_index, ctx.stop.tokenIndex)
