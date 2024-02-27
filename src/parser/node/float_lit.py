from .basic import Basic, Digraph
from uuid import UUID


class FloatLiteral(Basic):
    """
    Literal node. Node containing an actual value. (e.g. string, integer).
    """

    def __init__(self, value: float) -> None:
        self.value: float = value  # TODO ensure gets set
        """
        Value of the literal.
        """

        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)

    def __repr__(self) -> str:
        return f"{self.value}"