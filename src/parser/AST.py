from __future__ import annotations
from abc import ABC, abstractmethod

from typing import List
import typing
from graphviz import Digraph
import random


def main():
    ast = Ast()
    n1 = AstBinOpNode("+")
    n2 = AstBinOpNode("+")
    n3 = AstLiteralNode("1")
    n4 = AstLiteralNode("2")
    n5 = AstLiteralNode("3")

    ast.set_root(n1)
    n1.lhs = n2
    n1.rhs = n3
    n2.lhs = n4
    n2.rhs = n5

    graph = ast.to_dot_graph()
    graph.save(filename="graph.gv")

    # for node in ast.iter(AstIterPostorder):
    #     print(node.name)


# class AstIter(ABC):
#     def __init__(self, ast: Ast) -> None:
#         self.ast = ast

#     def __iter__(self) -> None:
#         self.visit(self.ast.root)

#     def visit(self, node: AstBasicNode):  # TODO rename
#         match node:
#             case AstBinOpNode():
#                 yield from self.bin_op(node)
#             case AstUnOpNode():
#                 yield from self.un_op(node)
#             case AstLiteralNode():
#                 yield from self.literal(node)
#             case _:
#                 raise Exception  # TODO proper exception type

#     # @abstractmethod
#     def bin_op(self, node: AstBinOpNode):
#         raise Exception  # TODO proper exception type

#     # @abstractmethod
#     def un_op(self, node: AstUnOpNode):
#         raise Exception  # TODO proper exception type

#     # @abstractmethod
#     def literal(self, node: AstLiteralNode):
#         raise Exception  # TODO proper exception type


# class AstIterPostorder():
#     def __init__(self, ast: Ast) -> None:
#         self.ast = ast

#     def __iter__(self):
#         return self.visit(self.ast.root)

#     def visit(self, node: AstBasicNode):  # TODO rename
#         match node:
#             case AstBinOpNode():
#                 yield from self.bin_op(node)
#             case AstUnOpNode():
#                 yield from self.un_op(node)
#             case AstLiteralNode():
#                 yield from self.literal(node)
#             case _:
#                 raise Exception  # TODO proper exception type

#     def bin_op(self, node: AstBinOpNode):
#         yield from self.visit(node.lhs)
#         yield from self.visit(node.rhs)
#         yield node

#     def un_op(self, node: AstUnOpNode):
#         self.visit(self, node.operand)
#         yield node

#     def literal(self, node: AstLiteralNode):
#         yield self


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

    def __init__(self, name: str) -> None:
        self.name = name
        self.children: List[AstBasicNode] = list()
        pass

    def append_child(self, child: AstBasicNode) -> None:
        self.children.append(child)
        # TODO necessary? alternative: per node type

    def append_to_graph(self, graph: Digraph, parent_id: str | None) -> None:
        # must be unique for every node
        node_id = str(random.randint(0, 100_000_000))
        graph.node(node_id, self.name, val="abc", val2="def")
        if parent_id is not None:
            graph.edge(parent_id, node_id)

        for child in self.children:
            child.append_to_graph(graph, node_id)


class AstBinOpNode(AstBasicNode):
    """
    Binary Operation node. Node operating on two other nodes.
    """

    def __init__(self, name: str) -> None:
        self.lhs: AstBasicNode = None  # TODO
        self.rhs: AstBasicNode = None  # TODO
        super().__init__(name)


class AstUnOpNode(AstBasicNode):
    """
    Unary Operation node. Node operating on one other node.
    """

    def __init__(self, name: str) -> None:
        self.operand: AstBasicNode = None  # TODO
        super().__init__(name)


class AstLiteralNode(AstBasicNode):
    """
    Literal node. Node containing an actual value. (e.g. string, integer).
    """

    def __init__(self, name: str) -> None:
        self.value = None  # TODO
        super().__init__(name)


if __name__ == "__main__":
    main()
