from src.parser.AST.node.stmt.statement import Statement
from src.parser.AST.node.terminator import *
from src.parser.AST.node.expr.expr import *
from src.parser.AST.node.stmt.compound_stmt import *
from src.parser.CFG import BasicBlock


class ConditionalStatement(Statement, Terminator):
    def __init__(self, condition_w: Wrapper[Expression | BasicBlock],
                 true_branch_w: Wrapper[CompoundStatement | BasicBlock], false_branch_w: Wrapper[CompoundStatement | BasicBlock] | None = None):
        super().__init__()
        self.condition_w: Wrapper[Expression | BasicBlock] = condition_w
        self.true_branch_w: Wrapper[CompoundStatement | BasicBlock] = true_branch_w
        self.false_branch_w: Wrapper[CompoundStatement | BasicBlock] | None = false_branch_w
        self.end_branch_w: Wrapper[Statement] | None = None
    def __repr__(self):
        return f"conditional"
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        self.condition_w.n.append_to_graph(graph, self.id, f"condition")
        self.true_branch_w.n.append_to_graph(graph, self.id, "true")
        if self.false_branch_w is not None:
            self.false_branch_w.n.append_to_graph(graph, self.id, "false")
        if self.end_branch_w is not None:
            graph.edge(str(self.id), str(self.end_branch_w.n.id), label="end")
