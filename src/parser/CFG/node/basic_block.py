from src.parser.node import *
from src.parser.AST import *
from cfg_node import *
class BasicBlock(CFGNode):
    def __init__(self, ast_nodes: list[Wrapper[Basic]]):
        self.ast_block_items: list[Wrapper[Basic]] = ast_nodes

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)