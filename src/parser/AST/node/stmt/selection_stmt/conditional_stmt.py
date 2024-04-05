from .selection_stmt import *

class ConditionalStatement(SelectionStatement):
    def __init__(self, condition_w: Wrapper[Expression],
                 true_branch_w: Wrapper[CompoundStatement | BasicBlock],
                 false_branch_w: Wrapper[CompoundStatement | BasicBlock] | None = None):
        super().__init__()
        self.condition_w: Wrapper[Expression] = condition_w
        self.true_branch_w: Wrapper[CompoundStatement | BasicBlock] = true_branch_w
        self.false_branch_w: Wrapper[CompoundStatement | BasicBlock] | None = false_branch_w
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
        self.condition_w.n.append_to_graph(graph, self.id)
        self.true_branch_w.n.append_to_graph(graph, self.id)
        if self.false_branch_w is not None:
            self.false_branch_w.n.append_to_graph(graph, self.id)

    def __repr__(self):
        return f"conditional statement"