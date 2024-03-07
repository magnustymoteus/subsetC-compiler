from cfg_node import *
class EntryBlock(CFGNode):
    def __init__(self):
        super().__init__(no_predecessors=True)