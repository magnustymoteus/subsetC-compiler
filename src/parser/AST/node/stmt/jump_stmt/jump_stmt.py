from src.parser.AST.node.stmt.statement import Statement
from src.parser.AST.node.terminator import *
from src.parser.AST.node.expr.expr import *
from src.parser.AST.node.stmt.compound_stmt import *
from src.parser.CFG import BasicBlock

class JumpStatement(Statement, Terminator):
    def __init__(self, label: str, value_w: Wrapper[CompoundStatement | BasicBlock] | None =None):
        super().__init__()
        self.label: str = label
        self.value_w: Wrapper[CompoundStatement | BasicBlock] = value_w
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
        if self.value_w is not None:
            self.value_w.n.append_to_graph(graph, self.id)
    def __repr__(self):
        return f"{self.label}"