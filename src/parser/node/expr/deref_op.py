from ..basic import Digraph
from .un_op import UnaryOp
from uuid import UUID
from .expr import Expression


class DerefOp(UnaryOp):
    """
    Dereference Operation node. Node operating on one other node.
    """

    def __init__(self):
        super().__init__('*')

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)

    def __repr__(self) -> str:
        return self.get_typed_str("dereference")
