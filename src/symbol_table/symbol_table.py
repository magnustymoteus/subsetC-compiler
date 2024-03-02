from __future__ import annotations
from src.symbol_table import SymbolType
from src.parser.node.basic import *

class SymbolTableEntry:
    def __init__(self, name: str, symbolType: SymbolType, definition_line=None, usage_lines=None):
        self.name = name
        self.type = symbolType
        self.definition_line = definition_line
        self.usage_lines = usage_lines
    def __repr__(self):
        return f"symbol: {self.name}, type: {self.type}"


class SymbolTable(Basic):
    def __init__(self, parent: Wrapper[SymbolTable] | None = None):
        self.lookup_table: dict[str, SymbolTableEntry] = dict()  # identifier (symbol) mapped to symbol table entry
        self.parent: None | Wrapper[SymbolTable] = parent
        super().__init__()

    def __repr__(self):
        result: str = str()
        for symbol in self.lookup_table:
            result += "\n"+self.lookup_table[symbol].__repr__()
        return "Symbol Table:"+result

    def lookup_symbol(self, name: str) -> SymbolTableEntry | None:
        if self.lookup_table.get(name, None) is None:
            if self.parent is not None:
                return self.parent.n.lookup_symbol(name)
        else:
            return self.lookup_table.get(name)
        return None


    def symbol_exists(self, name: str) -> bool:
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

