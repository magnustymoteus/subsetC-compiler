from ..basic import Basic, Digraph
from uuid import UUID
from .expr import Expression


class Literal(Expression):
    """
    Literal node. Node containing an actual value. (e.g. string, integer).
    """

    def __init__(self, value) -> None:
        self.value = value
        """
        Value of the literal.
        """

        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)

    def __repr__(self) -> str:
        return self.get_typed_str(self.value)
