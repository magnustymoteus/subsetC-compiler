from src.parser.visitor.CFG_visitor.cfg_visitor import *
from copy import deepcopy

'''Convert AST with TAC to AST with only static single assignments'''
class SSAVisitor(CFGVisitor):
    def __init__(self, cfg: Cfg):
        self.assignment_count: dict[str, int] = {}
        super().__init__(cfg)

    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        self.assignment_count[node_w.n.identifier] += 1
        super().variable_decl(node_w)

    def assign(self, node_w: Wrapper[Assignment]):
        self.assignment_count[node_w.n.assignee_w.n] += 1
        super().assign(node_w)

