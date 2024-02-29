from .basic import Digraph
from .lit import Literal
from uuid import UUID


class CharLiteral(Literal):
    """
    Literal node. Node containing an actual value. (e.g. string, integer).
    """

    def __init__(self, value: int | str) -> None:
        """
        Value of the literal.
        """
        super().__init__(value)

        if isinstance(value, int):
            self.value: int = value
        elif isinstance(value, str):
            assert len(value) == 1
            self.value: int = ord(value)
        assert self.value < 128  # basic ascii only


    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)

    def __repr__(self) -> str:
        return f"'{chr(self.value)}'"
