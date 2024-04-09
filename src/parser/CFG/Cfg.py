from src.parser.AST.node import *
from graphviz import Digraph
from .node.basic_block import *
class ControlFlowGraph():
    def __init__(self) -> None:
        self.basic_blocks: list[Wrapper[BasicBlock]] = []

    def add_basic_block(self) -> Wrapper[BasicBlock]:
        basic_block_w: Wrapper[BasicBlock] = wrap(BasicBlock())
        self.basic_blocks.append(basic_block_w)
        return basic_block_w
    def to_dot_graph(self) -> Digraph:
        """
        Export the AST to a dot graph.
        """
        graph = Digraph(strict=True)
        for basic_block_w in self.basic_blocks:
            basic_block_w.n.append_to_graph(graph, None)
        return graph