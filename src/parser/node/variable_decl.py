from .basic import Basic, Digraph, Wrapper, wrap
from uuid import UUID
from src.symbol_table import SymbolType
class VariableDeclaration(Basic):

    def __init__(self, identifier: str, type: SymbolType):
        self.identifier: str = identifier
        self.type: SymbolType = type
        self.definition_w: Wrapper = wrap()
        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
        if self.definition_w.n is not None:
            self.definition_w.n.append_to_graph(graph, self.id)

    def __repr__(self) -> str:
        str1 = f"definition: {self.identifier}" if self.definition_w.n is not None \
            else f"declaration: {self.identifier}"
        return str1+f" ({self.type.__repr__()})"
