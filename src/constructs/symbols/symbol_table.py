from __future__ import annotations
from src.constructs.node import *
from .symbol_type import *
import html
class SymbolTableEntry:
    def __init__(self, name: str, symbolType: SymbolType):
        self.name = name
        self.type = symbolType
        self.stopped_propagating: bool = False
        self.value_w: Wrapper = wrap()
        self.used: bool = False
    @property
    def __repr__(self):
        return f"symbol: {self.name}, type: {self.type}"


class SymbolTable(AbstractNode):
    def __init__(self, parent: Wrapper[SymbolTable] | None = None):
        """
        Initialize a SymbolTable object.

        :param parent: The parent symbol table.
        """
        self.lookup_table: dict[str, SymbolTableEntry] = dict()  # identifier (symbol) mapped to symbol table entry
        self.parent: None | Wrapper[SymbolTable] = parent
        super().__init__()

    def __repr__(self):
        result: str = str()
        for symbol in self.lookup_table:
            result += "\n"+self.lookup_table[symbol].__repr__()
        return "Symbol Table:"+result
    def has_parent(self) -> bool:
        return self.parent is not None

    def get_corresponding_table(self, symbol: str) -> SymbolTable | None:
        """
        Get the symbol table that contains the given symbol.

        :param symbol: The name of the symbol to look up.
        :return: The symbol table if found, None otherwise.
        """
        if self.lookup_table.get(symbol, None) is None:
            if self.parent is not None:
                return self.parent.n.get_corresponding_table(symbol)
        else:
            return self
        return None

    def lookup_symbol(self, symbol: str) -> SymbolTableEntry | None:
        """
        Look up a symbol in the symbol table. If the symbol is not found in the current symbol table, look in the parent.

        :param symbol: The name of the symbol to look up.
        :return: The symbol table entry if found, None otherwise.
        """
        table = self.get_corresponding_table(symbol)
        return table.lookup_table[symbol] if table is not None else None

    def symbol_exists(self, name: str) -> bool:
        """
        Check if a symbol exists in the symbol table.

        :param name: The name of the symbol to check.
        :return: True if the symbol exists, False otherwise.
        """
        return True if self.lookup_symbol(name) is not None else False

    def symbol_exists_in_scope(self, name: str) -> bool:
        """
        Check if a symbol exists in the current symbol table.  Only checks most local scope.

        :param name: The name of the symbol to check.
        :return: True if the symbol exists, False otherwise.
        """
        return True if self.lookup_table.get(name, None) is not None else False

    def add_symbol(self, entry: SymbolTableEntry):
        """
        Add a symbol to the symbol table.

        :param entry: The symbol table entry to add.
        """
        self.lookup_table[entry.name] = entry
    def get_enclosing_function_type(self) -> SymbolTable | None:
        if not isinstance(self, FunctionEncloser):
            if self.parent is not None:
                return self.parent.n.get_enclosing_function_type()
        else:
            return self.func_signature
        return None

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None):
        table_contents_str = ''
        for symbol_entry in self.lookup_table.values():
            table_contents_str += f'<tr><td>{html.escape(str(symbol_entry.name))}</td><td>{html.escape(str(symbol_entry.type))}</td><td>{html.escape(str(symbol_entry.value_w.n))}</td></tr>'
        table_str = (f'<<table border="0" cellborder="1" cellspacing="0"><tr>  '
                     f'<td><i>Symbol</i></td><td><i>Type</i></td><td><i>Value</i></td></tr>{html.escape(str(table_contents_str))}</table>>')
        graph.node(str(self.id), label=table_str, shape='plain')
        if self.parent is not None:
            graph.edge(str(self.parent.n.id), str(self.id))

class FunctionEncloser(SymbolTable):
    def __init__(self, parent: Wrapper[SymbolTable], func_signature: FunctionType):
        super().__init__(parent)
        self.func_signature: FunctionType = func_signature


