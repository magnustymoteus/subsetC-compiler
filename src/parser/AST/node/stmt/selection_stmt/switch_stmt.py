from .selection_stmt import *
from ..labeled_stmt import *


class SwitchStatement(SelectionStatement):
    def __init__(self, expr_w: Wrapper[Expression], cases: list[Wrapper[LabeledStatement]], default_w: Wrapper[LabeledStatement] | None = None):
        super().__init__()
        self.expr_w: Wrapper[Expression] = expr_w
        self.cases: list[Wrapper[LabeledStatement]] = cases
        self.default_w: Wrapper[LabeledStatement] | None = default_w

    def __repr__(self):
        return f"switch"
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
        self.expr_w.n.append_to_graph(graph, self.id)
        for case_w in self.cases:
            case_w.n.append_to_graph(graph, self.id)
        if self.default_w is not None:
            self.default_w.n.append_to_graph(graph, self.id)