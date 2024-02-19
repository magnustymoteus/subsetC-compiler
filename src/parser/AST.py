from __future__ import annotations
from abc import ABC, abstractmethod

from graphviz import Digraph
from uuid import UUID, uuid4


def main():
    ast = Ast()
    n1 = AstBinOpNode("+")
    n2 = AstBinOpNode("+")
    n3 = AstLiteralNode("1")
    n4 = AstLiteralNode("2")
    n5 = AstUnOpNode("-")
    n6 = AstLiteralNode("3")

    ast.set_root(n1)
    n1.lhs = n2
    n1.rhs = n3
    n2.lhs = n4
    n2.rhs = n5
    n5.operand = n6

    graph = ast.to_dot_graph()
    graph.save(filename="graph.gv")

    for node in ast.iter(AstIterPostorder):
        print(node.name)


class AstIter(ABC):
    def __init__(self, ast: Ast) -> None:
        self.ast = ast

    def __iter__(self):
        yield from self.match_node(self.ast.root)

    def match_node(self, node: AstBasicNode):  # TODO rename
        match node:
            case AstBinOpNode():
                yield from self.bin_op(node)
            case AstUnOpNode():
                yield from self.un_op(node)
            case AstLiteralNode():
                yield from self.literal(node)
            case _:
                raise Exception  # TODO proper exception type

    @abstractmethod
    def bin_op(self, node: AstBinOpNode):
        raise Exception  # TODO proper exception type

    @abstractmethod
    def un_op(self, node: AstUnOpNode):
        raise Exception  # TODO proper exception type

    @abstractmethod
    def literal(self, node: AstLiteralNode):
        raise Exception  # TODO proper exception type


class AstIterPostorder(AstIter):
    def __init__(self, ast: Ast) -> None:
        super().__init__(ast)

    def bin_op(self, node: AstBinOpNode):
        yield from self.match_node(node.lhs)
        yield from self.match_node(node.rhs)
        yield node

    def un_op(self, node: AstUnOpNode):
        yield from self.match_node(node.operand)
        yield node

    def literal(self, node: AstLiteralNode):
        yield node


class Ast:
    def __init__(self) -> None:
        self.root: AstBasicNode = None

    def __iter__(self):
        AstIterPostorder(self)

    def iter(self, iter_method: AstIter):
        return iter_method(self)

    def set_root(self, node: AstBasicNode):
        self.root = node

    def to_dot_graph(self) -> Digraph:
        graph = Digraph()
        self.root.append_to_graph(graph, None)

        return graph


class AstBasicNode(ABC):
    """
    Basic node. Contains attributes shared by all nodes.
    """

    def __init__(self) -> None:
        self.id: UUID = uuid4()

    @abstractmethod
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        graph.node(str(self.id), str(self), val="abc", val2="def")
        if parent_id is not None:
            graph.edge(str(parent_id), str(self.id))

    def __repr__(self) -> str:
        return f"node-id:{str(self.id)}"


# class NodeWrapper:
#     def __init__(self, node:AstBasicNode) -> None:
#         self.node = node


class AstBinOpNode(AstBasicNode):
    """
    Binary Operation node. Node operating on two other nodes.
    """

    def __init__(self, operator: str) -> None:
        self.lhs: AstBasicNode = None  # TODO ensure gets set
        self.rhs: AstBasicNode = None  # TODO ensure gets set
        self.operator: str = operator  # TODO use enum instead of string for operator type
        super().__init__()

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
        self.operand: AstBasicNode = None  # TODO ensure gets set
        self.operator: str = operator  # TODO use enum instead of string for operator type
        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: str | None) -> None:
        super().append_to_graph(graph, parent_id)
        self.operand.append_to_graph(graph, self.id)

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
        self.assignee = None  # TODO ensure gets set
        self.value = None  # TODO ensure gets set
        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: str | None) -> None:
        super().append_to_graph(graph, parent_id)

    def __repr__(self) -> str:
        return f"="


if __name__ == "__main__":
    main()
