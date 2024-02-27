from .basic import Basic, Wrapper, wrap, Digraph
from uuid import UUID


class UnaryOp(Basic):
    """
    Unary Operation node. Node operating on one other node.
    """

    def __init__(self, operator: str) -> None:
        self.operand_w: Wrapper = wrap()  # TODO ensure gets set
        """
        Wrapper for the value node operated on.
        """

        self.operator: str = operator  # TODO use enum instead of string for operator type
        """
        Operation type of the node.
        """

        super().__init__()

    @property
    def operand(self) -> Basic:
        """
        The value node the operation acts on.
        """
        return self.operand_w.n

    @operand.setter
    def operand(self, node: Basic):
        self.operand_w.n = node

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
        self.operand.append_to_graph(graph, self.id)

    def __repr__(self) -> str:
        return f"{self.operator}"
