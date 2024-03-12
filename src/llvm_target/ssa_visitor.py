from src.parser.visitor.CFG_visitor.cfg_visitor import *
from copy import deepcopy

'''Convert variable names to %number and put the '''
class SSAVisitor(CFGVisitor):
    def __init__(self, cfg: Cfg):
        self.assignment_count: dict[str, int] = {}
        super().__init__(cfg)

    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        super().variable_decl(node_w)


    def assign(self, node_w: Wrapper[Assignment]):
        #self.assignment_count[node_w.n.assignee_w.n] += 1
        super().assign(node_w)

