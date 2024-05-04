from antlr4.error.ErrorListener import ErrorListener
from src.compilation.preprocessor.preprocessor_visitor import EnvironmentNode

class MyErrorListener(ErrorListener):
    def __init__(self, env_root: EnvironmentNode):
        self.env_root: EnvironmentNode = env_root
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        env_node, translated_line = self.env_root.get_env(line)
        raise SyntaxError(f"{env_node.filename}:{translated_line}:{column}:syntax_error:{msg}")