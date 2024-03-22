from __future__ import annotations
from src.parser.node import *
from src.symbol_table.symbol_table import SymbolTable

class CFGNode(AbstractNode):
    def __init__(self):
        super().__init__()
        self.local_symtab_w: Wrapper[SymbolTable] = wrap()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        """
        Add the node to the dot graph. The name is determined by the node's repr.
        """
        super().append_to_graph(graph, parent_id)
        if self.local_symtab_w.n is not None:
            self.local_symtab_w.n.append_to_graph(graph, self.id)

