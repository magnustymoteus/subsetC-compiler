from src.parser.AST.node.stmt.statement import Statement
from src.parser.AST.node.terminator import *
from src.parser.AST.node.expr.expr import *
from src.parser.CFG import BasicBlock
from src.parser.AST.node.variable_decl import *
from src.parser.AST.node.stmt.compound_stmt import *

class IterationStatement(Statement, Terminator):
    def __init__(self, condition_w: Wrapper[Expression], body_w: Wrapper[CompoundStatement], adv_w: Wrapper[Expression | BasicBlock] | None = None):
        super().__init__()
        self.condition_w: Wrapper[Expression] = condition_w
        self.body_w: Wrapper[CompoundStatement | BasicBlock] = body_w
        self.adv_w: Wrapper[Expression | BasicBlock] | None = adv_w
        self.end_branch_w: Wrapper[Statement] | None = None

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
        self.condition_w.n.append_to_graph(graph, self.id, "condition")
        self.body_w.n.append_to_graph(graph, self.id, "body")
        if self.adv_w is not None:
            self.adv_w.n.append_to_graph(graph, self.id, "advancement")
        if self.end_branch_w is not None:
            graph.edge(str(self.id), str(self.end_branch_w.n.id), label="end")

    def __repr__(self):
        return f"iteration statement"