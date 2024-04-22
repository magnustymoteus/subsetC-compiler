from src.constructs.AST.node.stmt.statement import *
from src.constructs.AST.node.expr.expr import *

class IOStatement(Statement):
    def __init__(self, name: str, contents: str, arguments: list[Wrapper[Expression]]):
        super().__init__()
        self.name: str = name
        self.contents: str = contents
        self.arguments: list[Wrapper[Expression]] = arguments

    def __repr__(self):
        return f'{self.name} "{self.contents}" {[arg_w.n for arg_w in self.arguments]}'