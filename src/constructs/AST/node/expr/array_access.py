from .expr import *
from .identifier import *
class ArrayAccess(Expression):
    def __init__(self, accessed_w: Wrapper[Expression], index_w: Wrapper[Expression]):
        self.accessed_w: Wrapper[Expression] = accessed_w
        self.index_w: Wrapper[Basic] = index_w
        super().__init__()
    def __repr__(self):
        return self.get_typed_str(f"array access")
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        self.accessed_w.n.append_to_graph(graph, self.id, "array")
        self.index_w.n.append_to_graph(graph, self.id, "index")