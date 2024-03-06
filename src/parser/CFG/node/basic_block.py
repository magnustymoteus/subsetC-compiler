from src.parser.node import *
from src.parser.AST import *
class BasicBlock(AbstractNode):
    def __init__(self, ast_nodes: list[Wrapper[Basic]]):
        self.ast_nodes: list[Wrapper[Basic]] = ast_nodes
        self.successors: list[Wrapper[BasicBlock]] = []

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)