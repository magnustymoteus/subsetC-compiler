from src.parser.visitor.AST_visitor.ast_visitor import *

'''Traverses the AST tree in pre-order to perform constant propagation'''
class OptimizationVisitor(ASTVisitor):
    def __init__(self, ast: Ast):
        super().__init__(ast)
    def un_op(self, node_w: Wrapper[UnaryOp]):
        if node_w.n.type.ptr_count == 0 and isinstance(node_w.n.operand_w.n, Identifier):
            symbol: SymbolType = node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.operand_w.n.name)
            #if symbol.is_constant:

