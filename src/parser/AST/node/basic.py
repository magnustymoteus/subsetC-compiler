from src.parser.node import *
from src.symbol_table.symbol_table import SymbolTable


class Basic(AbstractNode):
    """
    Basic node. Contains attributes shared by all nodes.
    """

    def __init__(self) -> None:
        super().__init__()
        self.line_nr: int | None = None
        self.col_nr: int | None = None
        self.comments = []
        self.local_symtab_w: Wrapper[SymbolTable] = wrap()



    def set_line_col_nr(self, line_nr: int, col_nr: int):
        self.line_nr = line_nr
        self.col_nr = col_nr

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        """
        Add the node to the dot graph. The name is determined by the node's repr.
        """
        super().append_to_graph(graph, parent_id)
        if self.local_symtab_w.n is not None:
            self.local_symtab_w.n.append_to_graph(graph, self.id)







