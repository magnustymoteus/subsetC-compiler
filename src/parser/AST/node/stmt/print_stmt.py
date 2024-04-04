from src.parser.AST.node.stmt.statement import Statement
from src.parser.AST.node.basic import Basic, Wrapper


class PrintStatement(Statement):
    '''
    This a temporary class and will (probably) be removed when function calls are implemented.
    '''
    def __init__(self, format: str, argument_w: Wrapper[Basic]):
        super().__init__()
        self.format: str = format
        self.argument_w: Wrapper[Basic] = argument_w

    def __repr__(self):
        return f"print {self.argument_w.n}"