from ..basic import Digraph
from .lit import Literal
from uuid import UUID
from src.constructs.symbols.symbol_type import PrimitiveType

class FloatLiteral(Literal):
    """
    Literal node. Node containing an actual value. (e.g. string, integer).
    """

    def __init__(self, value: float) -> None:
        """
        Value of the literal.
        """

        super().__init__(value)
        self.type = PrimitiveType('float', True)

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)

