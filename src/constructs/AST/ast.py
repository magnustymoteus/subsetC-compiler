from typing import Generator
from src.constructs.AST.node import *

class Ast:
    def __init__(self) -> None:
        self.root_w: Wrapper[Basic] = wrap()

    def set_root(self, root: Wrapper[Basic]) -> None:
        self.root_w = root

    def to_dot_graph(self) -> Digraph:
        """
        Export the AST to a dot graph.
        """
        graph = Digraph(strict=True)
        self.root_w.n.append_to_graph(graph, None)

        return graph
