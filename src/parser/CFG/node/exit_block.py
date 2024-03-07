from cfg_node import *
class ExitBlock(CFGNode):
    def __init__(self):
        super().__init__(no_successors=True)