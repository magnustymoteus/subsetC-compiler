from __future__ import annotations
from src.parser.node import *
class CFGNode(AbstractNode):
    def __init__(self, no_successors: bool = False, no_predecessors: bool = False):
        super().__init__()
        self.successors: list[Wrapper[CFGNode]] = [] if not no_successors else None
        self.predecessors: list[Wrapper[CFGNode]] = [] if not no_predecessors else None

