from src.parser.AST.node.stmt.statement import Statement
from src.parser.AST.node.terminator import *
from src.parser.AST.node.expr.expr import *
from src.parser.CFG import BasicBlock
from src.parser.AST.node.stmt.compound_stmt import *

class IterationStatement(Statement, Terminator):
    def __init__(self, condition_w: Wrapper[CompoundStatement | BasicBlock],
                 body_w: Wrapper[CompoundStatement | BasicBlock]):
        super().__init__()
        self.condition_w: Wrapper[CompoundStatement | BasicBlock] = condition_w
        self.body_w: Wrapper[CompoundStatement | BasicBlock] = body_w
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
        self.condition_w.n.append_to_graph(graph, self.id)
        self.body_w.n.append_to_graph(graph, self.id)

    def __repr__(self):
        return f"iteration statement"