from __future__ import annotations


class SymbolTableEntry:
    def __init__(self, name: str, symbolType, definition_line=None, usage_lines=None):
        self.name = name
        self.type = symbolType
        self.definition_line = definition_line
        self.usage_lines = usage_lines


class SymbolTable:
    def __init__(self, parent: SymbolTable | None = None):
        self.lookup_table: dict[str, SymbolTableEntry] = dict()  # identifier (symbol) mapped to symbol table entry
        self.children: list[SymbolTable] = list()
        self.parent: None | SymbolTable = parent

    @property
    def parent(self) -> None | SymbolTable:
        return self.parent

    @parent.setter
    def parent(self, parent: SymbolTable):
        self.parent = parent

    def add_child(self, child: SymbolTable):
        self.children.append(child)

    def remove_child(self, child: SymbolTable):
        self.children.remove(child)

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
