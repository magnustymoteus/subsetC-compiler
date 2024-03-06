from ..basic import Digraph
from .lit import Literal
from uuid import UUID


class FloatLiteral(Literal):
    """
    Literal node. Node containing an actual value. (e.g. string, integer).
    """

    def __init__(self, value: float) -> None:
        """
        Value of the literal.
        """

        super().__init__(value)

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)

