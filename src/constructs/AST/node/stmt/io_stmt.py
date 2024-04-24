from src.constructs.AST.node.stmt.statement import *
from src.constructs.AST.node.expr import *

class IOStatement(Statement):
    def __init__(self, name: str, contents_w: Wrapper[StringLiteral], arguments: list[Wrapper[Expression]]):
        super().__init__()
        self.name: str = name
        self.contents_w: Wrapper[StringLiteral] = contents_w
        self.arguments: list[Wrapper[Expression]] = arguments

    def __repr__(self):
        return f'{self.name} "{self.contents_w.n.string}" {[arg_w.n for arg_w in self.arguments]}'