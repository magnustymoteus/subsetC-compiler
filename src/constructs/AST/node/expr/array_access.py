from .expr import *
from .identifier import *
class ArrayAccess(Expression):
    def __init__(self, identifier_w: Wrapper[Identifier], indices: list[Wrapper[Expression]]):
        self.identifier_w: Wrapper[Identifier] = identifier_w
        self.indices: list[Wrapper[Basic]] = indices
        super().__init__()
    def __repr__(self):
        return self.get_typed_str(f"array access")
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        self.identifier_w.n.append_to_graph(graph, self.id, "array")
        for i, index_w in enumerate(self.indices):
            index_w.n.append_to_graph(graph, self.id, f"index {i+1}")

