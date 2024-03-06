from src.parser.AST.node import *
class ControlFlowGraph():
    def __init__(self) -> None:
        self.entry_block_w: Wrapper[AbstractNode] = wrap()


    def to_dot_graph(self) -> Digraph:
        """
        Export the AST to a dot graph.
        """
        graph = Digraph(strict="true")
        self.entry_block_w.n.append_to_graph(graph, None)

        return graph