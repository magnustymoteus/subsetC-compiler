from uuid import UUID, uuid4
from typing import TypeVar, Generic
from abc import ABC, abstractmethod
from graphviz import Digraph


class AbstractNode(ABC):
    def __init__(self) -> None:
        self.id: UUID = uuid4()


    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        graph.node(str(self.id), str(self))
        if parent_id is not None:
            graph.edge(str(parent_id), str(self.id))

    def __repr__(self) -> str:
        return f"node-id:{str(self.id)}"

NodeType = TypeVar("NodeType", bound=AbstractNode)

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

