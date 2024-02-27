from .basic import Basic, Wrapper, NodeType, Digraph
from uuid import UUID


class Program(Basic):
    """
    Program node that has all statements of the program as its children.
    """

    def __init__(self, statements: list[Wrapper[NodeType]]):
        self.statements: list[Wrapper[NodeType]] = statements
        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
        for w in self.statements:
            w.n.append_to_graph(graph, self.id)

    def __repr__(self):
        return f"program"
