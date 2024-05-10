from src.constructs.AST.node.stmt.statement import *
from src.constructs.AST.node.expr import *

class IOStatement(Statement):
    def __init__(self, name: str, contents_w: Wrapper[StringLiteral], arguments: list[Wrapper[Expression]]):
        super().__init__()
        self.name: str = name
        self.contents_w: Wrapper[StringLiteral] = contents_w
        self.arguments: list[Wrapper[Expression]] = arguments

    def __repr__(self):
        return f'{self.name} "{self.contents_w.n.string}"'

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        for argument_w in self.arguments:
            argument_w.n.append_to_graph(graph, self.id)