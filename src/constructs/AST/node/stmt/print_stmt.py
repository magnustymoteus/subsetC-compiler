from .statement import *
from src.constructs.node import *

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