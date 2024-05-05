from __future__ import annotations
from src.constructs.AST.node.basic import *
from src.constructs.symbols.symbol_table import SymbolTable

class CFGNode(Basic):
    def __init__(self):
        super().__init__()
        self.local_symtab_w: Wrapper[SymbolTable] = wrap()

