from src.parser.AST.node.basic import Wrapper, AbstractNode, Digraph
from uuid import UUID
from src.parser.AST.node.stmt.statement import Statement


class CompoundStatement(Statement):
    """
    Program node that has all statements of the program as its children.
    """

    def __init__(self, statements: list[Wrapper[AbstractNode]] = None):
        self.statements: list[Wrapper[AbstractNode]] = [] if statements is None else statements
        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        for w in self.statements:
            w.n.append_to_graph(graph, self.id)


    def __repr__(self):
        return f"compound_stmt"
