from src.parser.AST.node.stmt.statement import Statement
from src.parser.AST.node.terminator import *
from src.parser.AST.node.expr.expr import *
from src.parser.AST.node.stmt.compound_stmt import *
from src.parser.CFG import BasicBlock


class SwitchStatement(Statement, Terminator):
    def __init__(self, value_w: Wrapper[Expression], conditions: list[Wrapper[Expression]], branches: list[Wrapper[CompoundStatement]],
                 default_index: int | None = None):
        super().__init__()
        self.value_w: Wrapper[Expression] = value_w
        self.conditions: list[Wrapper[Expression]] = conditions
        self.branches: list[Wrapper[CompoundStatement]] = branches
        self.default_index: int | None = default_index
        self.end_branch_w: Wrapper[Statement] | None = None

    def __repr__(self):
        return f"switch"
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        for i, condition_w in enumerate(self.conditions):
            condition_w.n.append_to_graph(graph, self.id, f"case {i+1}")
        for i, branch_w in enumerate(self.branches):
            label: str = f"branch {i+1}" if self.default_index is None or i != self.default_index else "default"
            branch_w.n.append_to_graph(graph, self.id, label)
        if self.end_branch_w is not None:
            graph.edge(str(self.id), str(self.end_branch_w.n.id), label="end")
