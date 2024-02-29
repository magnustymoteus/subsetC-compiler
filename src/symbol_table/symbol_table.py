from __future__ import annotations
from src.symbol_table import SymbolType

class SymbolTableEntry:
    def __init__(self, name: str, symbolType: SymbolType, definition_line=None, usage_lines=None):
        self.name = name
        self.type = symbolType
        self.definition_line = definition_line
        self.usage_lines = usage_lines


class SymbolTable:
    def __init__(self, parent: SymbolTable | None = None):
        self.lookup_table: dict[str, SymbolTableEntry] = dict()  # identifier (symbol) mapped to symbol table entry
        self.parent: None | SymbolTable = parent

    def lookup_symbol(self, name: str) -> SymbolTableEntry | None:
        return self.lookup_table.get(name, None)

    def symbol_exists(self, name: str) -> bool:
        return True if self.lookup_table.get(name, False) else False

    def declare_symbol(self, entry: SymbolTableEntry):
        if self.symbol_exists(entry.name):
            return  # raise redeclaration error
        self.lookup_table[entry.name] = entry

    def define_symbol(self, entry: SymbolTableEntry):
        assert entry.definition_line is not None
        if self.symbol_exists(entry.name):
            return  # raise redefinition error
        self.lookup_table[entry.name] = entry
