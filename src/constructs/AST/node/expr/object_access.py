from __future__ import annotations
from .expr import *
from .identifier import *
class ObjectAccess(Expression):
    def __init__(self, identifier_w: Wrapper[Identifier], member_w: Wrapper[Identifier | ObjectAccess]):
        self.identifier_w: Wrapper[Identifier] = identifier_w
        self.member_w: Wrapper[Identifier] = member_w
        super().__init__()
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        self.identifier_w.n.append_to_graph(graph, self.id, "object")
        self.member_w.n.append_to_graph(graph, self.id, "member")

    def __repr__(self):
        return self.get_typed_str("object access")