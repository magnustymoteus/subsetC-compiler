from src.parser.AST.node.stmt.compound_stmt import *

class JumpStatement(Statement):
    def __init__(self, label: str, value_w: Wrapper[Statement] = None):
        super().__init__()
        self.label: str = label
        self.value_w: Wrapper[Statement] = value_w

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        if self.value_w is not None:
            graph.edge(str(self.id), str(self.value_w.n.id))
    def __repr__(self):
        return f"jump ({self.label})"

