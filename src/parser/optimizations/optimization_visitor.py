from src.parser.visitor.AST_visitor.ast_visitor import *
from src.parser.visitor.AST_visitor.copy_visitor import *
from copy import deepcopy

'''Traverses the AST tree in pre-order to perform constant propagation along other small optimizations'''
class OptimizationVisitor(ASTVisitor):
    def __init__(self, ast: Ast):
        super().__init__(ast)
    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        if node_w.n.definition_w.n is not None:
            self.visit(node_w.n.definition_w)

    def un_op(self, node_w: Wrapper[UnaryOp]):
        super().un_op(node_w)
        if node_w.n.operator in ["++", "--"]:
            if isinstance(node_w.n.operand_w.n, Identifier):
                symbol: SymbolTableEntry = node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.operand_w.n.name)
                symbol.has_changed = True
    def assign(self, node_w: Wrapper[Assignment]):
        self.visit(node_w.n.value_w)
        if isinstance(node_w.n.assignee_w.n, Identifier):
            symbol: SymbolTableEntry = node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.assignee_w.n.name)
            symbol.has_changed = True

    def deref_op(self, node_w: Wrapper[DerefOp]):
        if isinstance(node_w.n.operand_w.n, AddressOfOp):
            node_w.n = node_w.n.operand_w.n.operand_w.n
            self.visit(node_w)
        elif node_w.n.type.ptr_count == 0:
            node_w.n = node_w.n.operand_w.n
            self.visit(node_w)

    def addressof_op(self, node_w: Wrapper[AddressOfOp]):
        if not isinstance(node_w.n.operand_w.n, Identifier):
            self.visit(node_w.n.operand_w)
    def identifier(self, node_w: Wrapper[Identifier]):
        symbol: SymbolTableEntry = node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.name)
        if symbol.type.ptr_count == 0 and not symbol.has_changed:
            value = symbol.value_w
            CopyVisitor().visit(value)
            node_w.n = value.n
