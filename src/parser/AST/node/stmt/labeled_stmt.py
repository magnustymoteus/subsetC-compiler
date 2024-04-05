from src.parser.AST.node.stmt.statement import Statement
from src.parser.AST.node.terminator import *
from src.parser.AST.node.expr import Expression
class LabeledStatement(Statement, Terminator):
    def __init__(self, label: str, body: list[Wrapper[Statement]], expr_w: Wrapper[Expression] | None = None):
        super().__init__()
        self.label: str = label
        self.body: list[Wrapper[Statement]] = body
        self.expr_w: Wrapper[Expression] | None =  expr_w
    def __repr__(self):
        return f"{self.label} (label statement)"
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
        if self.expr_w is not None:
            self.expr_w.n.append_to_graph(graph, self.id)
        for statement in self.body:
            statement.n.append_to_graph(graph, self.id)