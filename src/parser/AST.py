from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generator, Generic, TypeVar

from graphviz import Digraph
from uuid import UUID, uuid4


def main():
    ast = Ast()
    n1: NodeWrapper[AstBinOpNode] = wrap(AstBinOpNode("+"))
    n2: NodeWrapper[AstBinOpNode] = wrap(AstBinOpNode("+"))
    n3: NodeWrapper[AstLiteralNode] = wrap(AstLiteralNode("1"))
    n4: NodeWrapper[AstLiteralNode] = wrap(AstLiteralNode("2"))
    n5: NodeWrapper[AstUnOpNode] = wrap(AstUnOpNode("-"))
    n6: NodeWrapper[AstLiteralNode] = wrap(AstLiteralNode("3"))

    ast.set_root(n1)
    n1.n.lhs_w = n2
    n1.n.rhs_w = n3
    n2.n.lhs_w = n4
    n2.n.rhs_w = n5
    n5.n.operand = n6

    graph = ast.to_dot_graph()
    graph.save(filename="graph.gv")

    for node in ast.iter(AstIterPostorder):
        print(node.n)


class AstIter(ABC):
    def __init__(self, ast: Ast) -> None:
        self.ast = ast

    def __iter__(self) -> Generator[NodeWrapper[NodeType], None, None]:
        yield from self.match_node(self.ast.root)

    def match_node(self, node_w: NodeWrapper[NodeType]):  # TODO rename
        match node_w.n:
            case AstBinOpNode():
                yield from self.bin_op(node_w)
            case AstUnOpNode():
                yield from self.un_op(node_w)
            case AstLiteralNode():
                yield from self.literal(node_w)
            case AstAssignNode():
                yield from self.assign(node_w)
            case _:
                raise Exception  # TODO proper exception type

    @abstractmethod
    def bin_op(self, node_w: NodeWrapper[AstBinOpNode]):
        raise Exception  # TODO proper exception type

    @abstractmethod
    def un_op(self, node_w: NodeWrapper[AstUnOpNode]):
        raise Exception  # TODO proper exception type

    @abstractmethod
    def literal(self, node_w: NodeWrapper[AstLiteralNode]):
        raise Exception  # TODO proper exception type

    @abstractmethod
    def assign(self, node_w: NodeWrapper[AstAssignNode]):
        raise Exception  # TODO proper exception type


class AstIterPostorder(AstIter):
    def __init__(self, ast: Ast) -> None:
        super().__init__(ast)

    def bin_op(self, node_w: NodeWrapper[AstBinOpNode]):
        yield from self.match_node(node_w.n.lhs_w)
        yield from self.match_node(node_w.n.rhs_w)
        yield node_w

    def un_op(self, node_w: NodeWrapper[AstUnOpNode]):
        yield from self.match_node(node_w.n.operand_w)
        yield node_w

    def literal(self, node_w: NodeWrapper[AstLiteralNode]):
        yield node_w

    def assign(self, node_w: NodeWrapper[AstAssignNode]):
        yield from self.match_node(node_w.n.assignee_w)
        yield from self.match_node(node_w.n.value_w)
        yield node_w


class Ast:
    def __init__(self) -> None:
        self.root: NodeWrapper[AstBasicNode] = None

    def iter(self, iter_method: AstIter) -> Generator[NodeWrapper[NodeType], None, None]:
        return iter_method(self)

    def set_root(self, nodw_w: NodeWrapper[AstBasicNode]):
        self.root = nodw_w

    def to_dot_graph(self) -> Digraph:
        graph = Digraph()
        self.root.n.append_to_graph(graph, None)

        return graph


class AstBasicNode(ABC):
    """
    Basic node. Contains attributes shared by all nodes.
    """

    def __init__(self) -> None:
        self.id: UUID = uuid4()

    @abstractmethod
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        graph.node(str(self.id), str(self))
        if parent_id is not None:
            graph.edge(str(parent_id), str(self.id))

    def __repr__(self) -> str:
        return f"node-id:{str(self.id)}"


NodeType = TypeVar("NodeType", bound=AstBasicNode)


class NodeWrapper(Generic[NodeType]):
    def __init__(self, node: NodeType = None) -> None:
        self.n = node


def wrap(node: NodeType = None):
    return NodeWrapper(node)


class AstBinOpNode(AstBasicNode):
    """
    Binary Operation node. Node operating on two other nodes.
    """

    def __init__(self, operator: str) -> None:
        self.lhs_w: NodeWrapper = wrap()  # TODO ensure gets set
        self.rhs_w: NodeWrapper = wrap()  # TODO ensure gets set
        self.operator: str = operator  # TODO use enum instead of string for operator type
        super().__init__()

    @property
    def lhs(self) -> AstBasicNode:
        return self.lhs_w.n

    @lhs.setter
    def lhs(self, node: AstBasicNode):
        self.lhs_w.n = node

    @property
    def rhs(self) -> AstBasicNode:
        return self.rhs_w.n

    @rhs.setter
    def rhs(self, node: AstBasicNode):
        self.rhs_w.n = node

    def append_to_graph(self, graph: Digraph, parent_id: str | None) -> None:
        super().append_to_graph(graph, parent_id)
        self.lhs.append_to_graph(graph, self.id)
        self.rhs.append_to_graph(graph, self.id)

    def __repr__(self) -> str:
        return f"{self.operator}"


class AstUnOpNode(AstBasicNode):
    """
    Unary Operation node. Node operating on one other node.
    """

    def __init__(self, operator: str) -> None:
        self.operand_w: NodeWrapper = wrap()  # TODO ensure gets set
        self.operator: str = operator  # TODO use enum instead of string for operator type
        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: str | None) -> None:
        super().append_to_graph(graph, parent_id)
        self.operand.append_to_graph(graph, self.id)

    @property
    def operand(self) -> AstBasicNode:
        return self.operand_w.n

    @operand.setter
    def operand(self, node: AstBasicNode):
        self.operand_w.n = node

    def __repr__(self) -> str:
        return f"{self.operator}"


class AstLiteralNode(AstBasicNode):
    """
    Literal node. Node containing an actual value. (e.g. string, integer).
    """

    def __init__(self, value: int) -> None:
        self.value: int = value  # TODO ensure gets set
        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: str | None) -> None:
        super().append_to_graph(graph, parent_id)

    def __repr__(self) -> str:
        return f"{self.value}"


class AstAssignNode(AstBasicNode):
    """
    Assignment node. Indicates an assignment to a value.
    """

    def __init__(self) -> None:
        self.assignee_w: NodeWrapper = wrap()  # TODO ensure gets set
        self.value_w: NodeWrapper = wrap()  # TODO ensure gets set
        super().__init__()

    @property
    def assignee(self):
        return self.assignee_w.n

    @assignee.setter
    def assignee(self, node: AstBasicNode):
        self.assignee_w.n = node

    @property
    def value(self):
        return self.value_w.n

    @value.setter
    def value(self, node: AstBasicNode):
        self.value_w.n = node

    def append_to_graph(self, graph: Digraph, parent_id: str | None) -> None:
        super().append_to_graph(graph, parent_id)
        self.assignee.append_to_graph(graph, self.id)
        self.value.append_to_graph(graph, self.id)

    def __repr__(self) -> str:
        return f"="


if __name__ == "__main__":
    main()
