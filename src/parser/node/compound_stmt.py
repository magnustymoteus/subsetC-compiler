from .basic import Wrapper, NodeType, Digraph, wrap, Basic
from uuid import UUID


class CompoundStatement(Basic):
    """
    Program node that has all statements of the program as its children.
    """

    def __init__(self):
        self.statements: list[Wrapper[NodeType]] = []
        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
        for w in self.statements:
            w.n.append_to_graph(graph, self.id)


    def __repr__(self):
        return f"compound_stmt"
