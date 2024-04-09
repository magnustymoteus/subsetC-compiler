from .basic import Digraph
from .expr import Literal
from uuid import UUID


class StrLiteral(Literal):
    """
    Literal node. Node containing an actual value. (e.g. string, integer).
    """

    def __init__(self, value: str) -> None:
        super().__init__(value)

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)

    def __repr__(self) -> str:
        return f'"{self.value}"'
