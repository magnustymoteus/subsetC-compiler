from src.parser.AST.node.stmt.statement import Statement
from src.parser.AST.node.terminator import *
from src.parser.AST.node.expr.expr import *
from src.parser.AST.node.stmt.compound_stmt import *
from src.parser.CFG import BasicBlock


class SelectionStatement(Statement, Terminator):
    def __init__(self, conditions: list[Wrapper[Expression]], branches: list[Wrapper[CompoundStatement]],
                 default_branch_w : Wrapper[CompoundStatement | BasicBlock] | None = None):
        super().__init__()
        self.conditions: list[Wrapper[Expression]] = conditions
        self.branches: list[Wrapper[CompoundStatement]] = branches
        self.default_branch_w: Wrapper[CompoundStatement] | None = default_branch_w
        self.end_branch_w: Wrapper[Statement] | None = None
        assert len(self.conditions) == len(self.branches) and len(self.conditions) > 0
    def __repr__(self):
        return f"selection"
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        for i, condition_w in enumerate(self.conditions):
            condition_w.n.append_to_graph(graph, self.id, f"condition {i+1}")
        for i, branch_w in enumerate(self.branches):
            branch_w.n.append_to_graph(graph, self.id, f"branch {i+1}")
        if self.default_branch_w is not None:
            self.default_branch_w.n.append_to_graph(graph, self.id, f"default branch")
        if self.end_branch_w is not None:
            graph.edge(str(self.id), str(self.end_branch_w.n.id), label="end")
