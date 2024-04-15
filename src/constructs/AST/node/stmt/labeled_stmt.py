from uuid import UUID

from graphviz import Digraph

from src.constructs.AST.node.stmt.statement import Statement
from src.constructs.AST.node.expr import Expression
from src.constructs.node import Wrapper


class LabeledStatement(Statement):
    def __init__(self, label: str, body: list[Wrapper[Statement]], expr_w: Wrapper[Expression] | None = None):
        super().__init__()
        self.label: str = label
        self.body: list[Wrapper[Statement]] = body
        self.expr_w: Wrapper[Expression] | None =  expr_w
    def __repr__(self):
        return f"{self.label} (label statement)"
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        if self.expr_w is not None:
            self.expr_w.n.append_to_graph(graph, self.id, "condition")
        for statement in self.body:
            statement.n.append_to_graph(graph, self.id)