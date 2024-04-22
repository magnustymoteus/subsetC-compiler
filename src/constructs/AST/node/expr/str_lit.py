from src.constructs.AST.node.basic import *
from src.constructs.AST.node.expr import ArrayLiteral, CharLiteral
from uuid import UUID
from src.constructs.symbols.symbol_type import *


class StringLiteral(ArrayLiteral):
    """
    Literal node. Node containing an actual value. (e.g. string, integer).
    """

    def __init__(self, value: str) -> None:
        char_lits: list[Wrapper[CharLiteral]] = [wrap(CharLiteral(char)) for char in value]
        self.string = value
        super().__init__(char_lits)

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)

    def __repr__(self) -> str:
        return super().get_typed_str(f'"{self.string}"')
