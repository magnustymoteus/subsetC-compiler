from .basic import Wrapper, AbstractNode, Digraph, wrap, Basic
from uuid import UUID
from .statement import Statement


class CompoundStatement(Statement):
    """
    Program node that has all statements of the program as its children.
    """

    def __init__(self):
        self.statements: list[Wrapper[AbstractNode]] = []
        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
        for w in self.statements:
            w.n.append_to_graph(graph, self.id)


    def __repr__(self):
        return f"compound_stmt"
