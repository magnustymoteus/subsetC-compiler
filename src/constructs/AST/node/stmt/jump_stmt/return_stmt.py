from .jump_stmt import *
from src.constructs.AST.node.expr.expr import *
class ReturnStatement(JumpStatement):
    def __init__(self, expr_w: Wrapper[Expression] | None = None):
        super().__init__("return")
        self.expr_w: Wrapper[Expression] | None = expr_w
    def __repr__(self):
        return f"return"
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        if self.expr_w is not None:
            self.expr_w.n.append_to_graph(graph, self.id)