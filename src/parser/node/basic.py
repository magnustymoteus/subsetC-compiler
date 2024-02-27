from abc import ABC, abstractmethod
from graphviz import Digraph
from uuid import UUID, uuid4
from typing import TypeVar, Generic


class Basic(ABC):
    """
    Basic node. Contains attributes shared by all nodes.
    """

    def __init__(self) -> None:
        self.id: UUID = uuid4()

    @abstractmethod
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        """
        Add the node to the dot graph. The name is determined by the node's repr.
        """
        graph.node(str(self.id), str(self))
        if parent_id is not None:
            graph.edge(str(parent_id), str(self.id))

    def __repr__(self) -> str:
        return f"node-id:{str(self.id)}"


NodeType = TypeVar("NodeType", bound=Basic)


class Wrapper(Generic[NodeType]):
    """
    Wrapper for AST node. This allows for editing the tree in-place by reassigning the contained node.
    """

    def __init__(self, node: NodeType = None) -> None:
        self.n = node


def wrap(node: NodeType = None):
    """
    Return a wrapper of the provided node.
    """
    return Wrapper(node)
