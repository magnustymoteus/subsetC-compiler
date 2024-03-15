from src.parser.node import *
from src.parser.AST import *
from .cfg_node import *
class BasicBlock(CFGNode):
    def __init__(self):
        super().__init__()
        self.ast_items: list[Wrapper[Basic]] = []
        #self.successors: list[Wrapper[CFGNode]] = [] if not no_successors else None
        #self.predecessors: list[Wrapper[CFGNode]] = [] if not no_predecessors else None

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
        for ast_item_w in self.ast_items:
            ast_item_w.n.append_to_graph(graph, self.id)
    def __repr__(self):
        return f"basic block"