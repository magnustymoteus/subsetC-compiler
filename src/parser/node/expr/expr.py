from ..basic import Basic, UUID, Digraph
from src.symbol_table.symbol_type import PrimitiveType
class Expression(Basic):
    def __init__(self):
        self.type: PrimitiveType | None = None
        super().__init__()
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
    def get_typed_str(self, repr_str: str):
        if self.type is not None:
            return f"{repr_str} ({self.type})"
        return str(repr_str)
