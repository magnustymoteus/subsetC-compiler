from src.symbol_table import *
from src.parser.AST.node.stmt.compound_stmt import *
from .basic import *
from .variable_decl import *

class FunctionDefinition(Basic):

    def __init__(self, name: str, body_w: Wrapper[CompoundStatement], parameters: list[Wrapper[VariableDeclaration]] = []) -> None:
        self.name: str = name
        self.body_w : Wrapper[CompoundStatement] = body_w
        self.parameters: list[Wrapper[VariableDeclaration]] = parameters
        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        for i, param_w in enumerate(self.parameters):
            param_w.n.append_to_graph(graph, self.id, f"parameter {i}")
        self.body_w.n.append_to_graph(graph, self.id, "body")
    def __repr__(self) -> str:
        return f"function definition {self.name} ({self.type})"
