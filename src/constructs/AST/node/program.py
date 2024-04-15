from .basic import Basic, Wrapper, AbstractNode, Digraph, wrap
from uuid import UUID


class Program(Basic):
    """
    Program node that has all statements of the program as its children.
    """

    def __init__(self):
        self.children: list[Wrapper[AbstractNode]] = []
        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        for child in self.children:
            child.n.append_to_graph(graph, self.id)


    def __repr__(self):
        return f"program"
