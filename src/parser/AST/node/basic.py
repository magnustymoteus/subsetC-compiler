from src.parser.node import *


class Basic(AbstractNode):
    """
    Basic node. Contains attributes shared by all nodes.
    """

    def __init__(self) -> None:
        super().__init__()
        self.line_nr: int | None = None
        self.col_nr: int | None = None
        self.comments = []
        self.source_code_line: str | None = None
        self.local_symtab_w: Wrapper[SymbolTable] = wrap()
        self.basic_block_w: Wrapper[BasicBlock] | None = None



    def set_line_col_nr(self, line_nr: int, col_nr: int):
        self.line_nr = line_nr
        self.col_nr = col_nr

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        """
        Add the node to the dot graph. The name is determined by the node's repr.
        """
        if self.basic_block_w is not None:
            with graph.subgraph(name=f"cluster_{self.basic_block_w.n.id}", graph_attr={"margin": "30"}) as subgraph:
                super().append_to_graph(subgraph, parent_id, label)
        else:
            super().append_to_graph(graph, parent_id, label)
        if self.local_symtab_w.n is not None:
            self.local_symtab_w.n.append_to_graph(graph, self.id)



from src.symbol_table.symbol_table import SymbolTable
from src.parser.CFG.node import BasicBlock



