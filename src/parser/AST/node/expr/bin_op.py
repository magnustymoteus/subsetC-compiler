from ..basic import Basic, Wrapper, wrap, Digraph
from uuid import UUID
from .expr import Expression

class BinaryOp(Expression):
    # class Operator:
    #     def __init__(self, op: str) -> None:
    #         self.op: str = op

    #     def apply(self, lhs: IntLiteral, rhs: IntLiteral):
    #         match lhs, rhs, self.op:
    #             case IntLiteral(), IntLiteral(), "+":
    #                 pass
    #             case _:
    #                 raise Exception

    #     def can_apply(self, lhs: Basic, rhs: Basic):
    #         pass

    """
    Binary Operation node. Node operating on two other nodes.
    """

    def __init__(self, operator: str, lhs_w: Wrapper[Expression] | None = None, rhs_w: Wrapper[Expression] | None = None) -> None:
        self.lhs_w: Wrapper = wrap() if lhs_w is None else lhs_w
        """
        Wrapper for left hand side value node.
        """

        self.rhs_w: Wrapper = wrap() if rhs_w is None else rhs_w
        """
        Wrapper for right hand side value node.
        """

        self.operator: str = operator
        """
        Operation type of the node.
        """

        super().__init__()

    @property
    def lhs(self) -> Basic:
        """
        The left hand side value node of the operation.
        """
        return self.lhs_w.n

    @lhs.setter
    def lhs(self, node: Basic):
        self.lhs_w.n = node

    @property
    def rhs(self) -> Basic:
        """
        The right hand side value node of the operation.
        """
        return self.rhs_w.n

    @rhs.setter
    def rhs(self, node: Basic):
        self.rhs_w.n = node

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        self.lhs.append_to_graph(graph, self.id)
        self.rhs.append_to_graph(graph, self.id)

    def __repr__(self) -> str:
        return self.get_typed_str(self.operator)
