from src.parser.AST.node.stmt.statement import Statement
from src.parser.AST.node.terminator import *
from src.parser.AST.node.expr.expr import *
from src.parser.AST.node.stmt.compound_stmt import *
from src.parser.CFG import BasicBlock

class JumpStatement(Statement, Terminator):
    def __init__(self, label: str, value_w: Wrapper[Statement] = None):
        super().__init__()
        self.label: str = label
        self.value_w: Wrapper[Statement] = value_w

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        if self.value_w is not None:
            graph.edge(str(self.id), str(self.value_w.n.id))
    def __repr__(self):
        return f"jump ({self.label})"

