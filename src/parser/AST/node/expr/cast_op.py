from ..basic import Basic, Wrapper, wrap, Digraph
from uuid import UUID
from .expr import Expression
from src.symbol_table.symbol_type import PrimitiveType

class CastOp(Expression):
    """
    Unary Operation node. Node operating on one other node.
    """

    def __init__(self, target_type: PrimitiveType) -> None:
        self.target_type = target_type
        self.expression_w : Wrapper = wrap()
        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
        self.expression_w.n.append_to_graph(graph, self.id)

    def __repr__(self) -> str:
        return self.get_typed_str(f"cast to {self.type}")
