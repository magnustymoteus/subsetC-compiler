from src.parser.visitor.CFG_visitor.cfg_visitor import *
from copy import deepcopy

# TODO:

'''Converts AST so that expressions have at most two operands by creating intermediate variables'''
class TACVisitor(CFGVisitor):
    def __init__(self, cfg: ControlFlowGraph):
        self.interm_var_count: int = 0
        self.current_tac_list: list[Wrapper[Expression]] = []

        super().__init__(cfg)

    def basic_block(self, node_w: Wrapper[BasicBlock]):
        super().basic_block(node_w)
        node_w.n.ast_items = self.current_tac_list + node_w.n.ast_items
        self.current_tac_list = []

    def addTACNode(self, node_w: Wrapper[Expression]) -> Wrapper[Identifier]:
        symbol_name: str = f"tac{self.interm_var_count}"
        new_type: PrimitiveType = deepcopy(node_w.n.type)

        identifier: Identifier = Identifier(symbol_name)
        identifier.type = new_type

        def_node: VariableDeclaration = VariableDeclaration(identifier.name, identifier.type)
        def_node.definition_w = node_w
        self.current_tac_list.append(wrap(def_node))

        self.interm_var_count += 1
        return wrap(identifier)

    def bin_op(self, node_w: Wrapper[BinaryOp]):
        super().bin_op(node_w)
        if not (isinstance(node_w.n.lhs_w.n, Identifier) or isinstance(node_w.n.lhs_w.n, Literal)):
            node_w.n.lhs_w = self.addTACNode(node_w.n.lhs_w)
        if not (isinstance(node_w.n.rhs_w.n, Identifier) or isinstance(node_w.n.rhs_w.n, Literal)):
            node_w.n.rhs_w = self.addTACNode(node_w.n.rhs_w)
    def un_op(self, node_w: Wrapper[UnaryOp]):
        super().un_op(node_w)
        if not (isinstance(node_w.n.operand_w.n, Identifier) or isinstance(node_w.n.operand_w.n, Literal)):
            node_w.n.operand_w = self.addTACNode(node_w.n.operand_w)






