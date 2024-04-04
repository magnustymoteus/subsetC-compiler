from uuid import UUID
from ..basic import Digraph
from .expr import Expression


class Identifier(Expression):
    def __init__(self, name: str) -> None:
        self.name: str = name
        """
        User assigned name of the indentifier.
        """

        # TODO
        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)

    def __repr__(self) -> str:
        return self.get_typed_str(f"id: {self.name}")
