from src.parser.visitor.CFG_visitor.cfg_visitor import *
from copy import deepcopy
# TODO:

'''Converts AST so that expressions have at most two operands by creating intermediate variables'''
class TACVisitor(CFGVisitor):
    def __init__(self, cfg: ControlFlowGraph):
        self.interm_var_count: int = 0
        self.current_tac_list: list[list[Wrapper[Expression]]] = []
        self.declarations: list[Wrapper[VariableDeclaration]] = []
        self.current_index: int = 0
        super().__init__(cfg)

    def basic_block(self, node_w: Wrapper[BasicBlock]):
        for index, ast_item in enumerate(node_w.n.ast_items):
            self.current_tac_list.append([])
            self.visit(ast_item)
            self.current_index = index
        for index, elem in enumerate(self.current_tac_list):
            for sub_elem in elem:
                node_w.n.ast_items.insert(index, sub_elem)

        node_w.n.ast_items = self.declarations + node_w.n.ast_items

        self.current_tac_list.clear()
        self.declarations.clear()

    def addTACNode(self, node_w: Wrapper[Expression], custom_index: int | None = None) -> Wrapper[Identifier]:
        symbol_name: str = f"tac{self.interm_var_count}"
        new_type: PrimitiveType = deepcopy(node_w.n.type)

        identifier: Identifier = Identifier(symbol_name)
        identifier.type = new_type

        def_node: VariableDeclaration = VariableDeclaration(identifier.name, identifier.type)
        def_node.definition_w = node_w

        insertion_index: int = self.current_index if custom_index is None else custom_index

        self.current_tac_list[insertion_index+1].insert(0,wrap(def_node))

        self.interm_var_count += 1
        return wrap(identifier)

    def bin_op(self, node_w: Wrapper[BinaryOp]):
        super().bin_op(node_w)
        if not (isinstance(node_w.n.lhs_w.n, Identifier) or isinstance(node_w.n.lhs_w.n, Literal)):
            node_w.n.lhs_w = self.addTACNode(node_w.n.lhs_w)
        if not (isinstance(node_w.n.rhs_w.n, Identifier) or isinstance(node_w.n.rhs_w.n, Literal)):
            node_w.n.rhs_w = self.addTACNode(node_w.n.rhs_w)
    def deref_op(self, node_w: Wrapper[DerefOp]):
        super().un_op(node_w)
        if not (isinstance(node_w.n.operand_w.n, Identifier) or isinstance(node_w.n.operand_w.n, Literal)):
            node_w.n.operand_w = self.addTACNode(node_w.n.operand_w)
    def un_op(self, node_w: Wrapper[UnaryOp]):
        super().un_op(node_w)
        if not (isinstance(node_w.n.operand_w.n, Identifier) or isinstance(node_w.n.operand_w.n, Literal)):
                node_w.n.operand_w = self.addTACNode(node_w.n.operand_w)
    def cast_op(self, node_w: Wrapper[CastOp]):
        super().cast_op(node_w)
        if not (isinstance(node_w.n.expression_w.n, Identifier) or isinstance(node_w.n.expression_w.n, Literal)):
            node_w.n.expression_w = self.addTACNode(node_w.n.expression_w)

    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        super().variable_decl(node_w)
        if node_w.n.definition_w.n is not None:
            assign_node = Assignment("=")
            assign_node.assignee_w.n = Identifier(deepcopy(node_w.n.identifier))
            assign_node.value_w.n = deepcopy(node_w.n.definition_w.n)
            assign_node.type = deepcopy(node_w.n.definition_w.n.type)
            assign_node.assignee_w.n.type = node_w.n.type
            node_w.n.definition_w.n = None

            self.declarations.append(wrap(deepcopy(node_w.n)))
            node_w.n = assign_node






