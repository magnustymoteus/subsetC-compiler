from .basic_block import BasicBlock
from .cfg_node import *
class BasicBlockList(CFGNode):
    def __init__(self):
        super().__init__()
        self.basic_blocks: list[Wrapper[BasicBlock]] = []
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
        for block_w in self.basic_blocks:
            block_w.n.append_to_graph(graph, self.id)


    def __repr__(self):
        return "basic block list"