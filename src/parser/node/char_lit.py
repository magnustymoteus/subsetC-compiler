from .basic import Basic, Digraph
from uuid import UUID


class CharLiteral(Basic):
    """
    Literal node. Node containing an actual value. (e.g. string, integer).
    """

    def __init__(self, value: int | str) -> None:
        self.value: int = 0
        """
        Value of the literal.
        """

        if isinstance(value, int):
            self.value: int = value
        elif isinstance(value, str):
            assert len(str) == 1
            self.value: int = ord(value)
        assert value < 128  # basic ascii only

        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)

    def __repr__(self) -> str:
        return f"{self.value}: {chr(self.value)}"
