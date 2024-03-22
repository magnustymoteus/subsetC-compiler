from __future__ import annotations
from src.symbol_table import SymbolType
from src.parser.AST.node import *
from src.parser.node import *


class SymbolTableEntry:
    def __init__(self, name: str, symbolType: SymbolType):
        self.name = name
        self.type = symbolType
        self.definition_w: Wrapper = wrap()
        self.has_changed: bool = False
        self.value_w: Wrapper = wrap()

    def __repr__(self):
        return f"symbol: {self.name}, type: {self.type}"


class SymbolTable(AbstractNode):
    def __init__(self, parent: Wrapper[SymbolTable] | None = None):
        # [a, SymbolTableEntry]
        self.lookup_table: dict[str, SymbolTableEntry] = dict()  # identifier (symbol) mapped to symbol table entry
        self.parent: Wrapper[SymbolTable] | None = parent
        super().__init__()

    def __repr__(self):
        result: str = str()
        for symbol in self.lookup_table:
            result += "\n" + self.lookup_table[symbol].__repr__()
        return "Symbol Table:" + result

    def lookup_symbol(self, name: str) -> SymbolTableEntry | None:
        """
        Look up a symbol in the symbol table. If the symbol is not found in the current symbol table, look in the parent.
        :param name: the name of the symbol to look up
        :return: the symbol table entry if found, None otherwise
        """
        if self.lookup_table.get(name, None) is None:
            if self.parent is not None:
                return self.parent.n.lookup_symbol(name)
        else:
            return self.lookup_table.get(name)
        return None

    def symbol_exists(self, name: str) -> bool:
        """
        Check if a symbol exists in the symbol table. Only checks most local scope.
        :param name: the name of the symbol to check
        :return: True if the symbol exists, False otherwise
        """
        return True if self.lookup_table.get(name, False) else False

    def add_symbol(self, entry: SymbolTableEntry):
        self.lookup_table[entry.name] = entry

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None):
        table_contents_str = ''
        for symbol_entry in self.lookup_table.values():
            table_contents_str += f'<tr><td>{symbol_entry.name}</td><td>{symbol_entry.type}</td></tr>'
        table_str = (f'<<table border="0" cellborder="1" cellspacing="0"><tr>  '
                     f'<td><i>Symbol</i></td><td><i>Type</i></td></tr>{table_contents_str}</table>>')
        with graph.subgraph(name="symtab", graph_attr={"rank": "same"}) as subgraph:
            subgraph.node(str(self.id), label=table_str, shape='plain')
            if self.parent is not None:
                subgraph.edge(str(self.id), str(self.parent.n.id), dir="back")
