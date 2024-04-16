from src.antlr_files.C_PreprocessorParser import *
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
    def __init__(self, buffered_tokens_stream: BufferedTokenStream, filepath: str):
        self.filepath = filepath
        self.defines: dict[str, str] = {}
        self.rewriter = TokenStreamRewriter(buffered_tokens_stream)
        self.included_paths: set[str] = {filepath}
        self.ifndef_stack: list[int] # contains line for the end of the endif directive token
    def visitProgram(self, ctx: C_PreprocessorParser.ProgramContext):
        super().visitProgram(ctx)
        if self.if_counter != 0:
            self.raise_preprocessing_error("Unterminated #if", ctx)
    def visitLine(self, ctx:C_PreprocessorParser.LineContext):
        self.visitChildren(ctx)
    def visitDefineDirective(self, ctx:C_PreprocessorParser.DefineDirectiveContext):
        self.defines[ctx.getChild(1).getText()] = PreprocessorVisitor.get_original_text(ctx.getChild(2))
        self.rewriter.delete("default", ctx.start.tokenIndex, ctx.stop.tokenIndex)
    def visitIncludeDirective(self, ctx:C_PreprocessorParser.IncludeDirectiveContext):
        is_library: bool = ctx.getChild(1).getText()[0] == '<'
        if not is_library:
            incomplete_path: str = ctx.getChild(1).getText()[1:-1]
            included_path = os.path.join(os.path.dirname(self.filepath), incomplete_path)
            if not os.path.exists(included_path):
                self.raise_preprocessing_error(f"{included_path}: No such file", ctx)
            included_contents = open(included_path, 'r').read()
            self.rewriter.replace("default", ctx.start.tokenIndex, ctx.stop.tokenIndex, included_contents)
            self.included_paths.add(included_path)
        else:
            # TODO: stdio.h => enable printf, scanf, ...
            self.rewriter.delete("default", ctx.start.tokenIndex, ctx.stop.tokenIndex)
    def visitTerminal(self, node):
        defined = self.defines.get(node.getText(), False)
        if defined:
            interval = node.getSourceInterval()
            self.rewriter.replace("default", interval[0], interval[1], defined)
    def get_processed_result(self):
        return self.rewriter.getDefaultText()
    def visitIfndefDirective(self, ctx:C_PreprocessorParser.IfndefDirectiveContext):
        self.if_counter += 1
    def visitEndifDirective(self, ctx:C_PreprocessorParser.EndifDirectiveContext):
        self.if_counter -= 1
        if self.if_counter < 0:
            self.raise_preprocessing_error(f"#endif without #if", ctx)
