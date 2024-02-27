from .basic import Basic, Digraph
from uuid import UUID
from src.symbol_table import SymbolType
class VariableDeclaration(Basic):

    def __init__(self, identifier: str, type: SymbolType, definition: None | str | int | float = None):
        self.identifier: str = identifier
        self.type: SymbolType = type
        self.definition: None | str | int | float = definition
        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)

    def __repr__(self) -> str:
        return f"{self.identifier} = {self.definition}"
