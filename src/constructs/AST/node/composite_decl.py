from .variable_decl import *
from src.constructs.symbols.symbol_type import *
class CompositeDeclaration(VariableDeclaration):
    def __init__(self, type: CompositeType):
        super().__init__(type.name, type)
