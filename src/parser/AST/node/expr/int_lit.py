from ..basic import Digraph
from .lit import Literal
from uuid import UUID
from src.symbol_table.symbol_type import PrimitiveType


class IntLiteral(Literal):
    """
    Literal node. Node containing an actual value. (e.g. string, integer).
    """

    def __init__(self, value: int) -> None:
        super().__init__(value)
        self.type = PrimitiveType('int', True)

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)

