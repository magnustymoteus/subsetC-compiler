from ..basic import Basic, Wrapper, wrap, Digraph
from .expr import Expression


class Assignment(Expression):
    """
    Assignment node. Indicates an assignment to a value.
    """

    def __init__(self, operator: str) -> None:
        self.assignee_w: Wrapper = wrap()  # TODO ensure gets set
        """
        Wrapper for the variable node assigned to.
        """

        self.value_w: Wrapper = wrap()  # TODO ensure gets set
        """
        Wrapper for the assigned value node.
        """
        self.operator: str = operator

        super().__init__()

    @property
    def assignee(self):
        """
        The variable node assigned to.
        """
        return self.assignee_w.n

    @assignee.setter
    def assignee(self, node: Basic):
        self.assignee_w.n = node

    @property
    def value(self):
        """
        The value node assigned to the variable.
        """
        return self.value_w.n

    @value.setter
    def value(self, node: Basic):
        self.value_w.n = node

    def append_to_graph(self, graph: Digraph, parent_id: str | None) -> None:
        super().append_to_graph(graph, parent_id)
        self.assignee.append_to_graph(graph, self.id)
        self.value.append_to_graph(graph, self.id)

    def __repr__(self) -> str:
        return self.get_typed_str(self.operator)
