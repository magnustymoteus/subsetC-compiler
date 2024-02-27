from .basic import Basic, Wrapper, NodeType, Digraph
from uuid import UUID


class Program(Basic):
    """
    Program node that has all statements of the program as its children.
    """

    def __init__(self, children: list[Wrapper[NodeType]]):
        self.children: list[Wrapper[NodeType]] = children
        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
        for w in self.children:
            w.n.append_to_graph(graph, self.id)

    def __repr__(self):
        return f"program"
