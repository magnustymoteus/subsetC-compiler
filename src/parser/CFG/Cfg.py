from src.parser.AST.node import *
from .node.basic_block_list import *
class ControlFlowGraph():
    def __init__(self) -> None:
        self.bblock_list: Wrapper[BasicBlockList] = wrap(BasicBlockList())



    def to_dot_graph(self) -> Digraph:
        """
        Export the AST to a dot graph.
        """
        graph = Digraph(strict="true")
        self.bblock_list.n.append_to_graph(graph, None)

        return graph