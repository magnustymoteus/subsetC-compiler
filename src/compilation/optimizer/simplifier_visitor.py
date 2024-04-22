from src.compilation.visitor.AST_visitor import *
from src.constructs import *
class SimplifierVisitor(ASTVisitor):
    def __init__(self, ast: Ast):
        super().__init__(ast)

    def assign(self, node_w: Wrapper[Assignment]):
        if len(node_w.n.operator) > 1:
            operator: str = node_w.n.operator[0]
            node_w.n.operator = "="
            assignee_copy_w: Wrapper[Identifier] = wrap((node_w.n.assignee_w.n))
            value_copy_w: Wrapper[Expression] = wrap((node_w.n.value_w.n))
            CopyVisitor().visit(assignee_copy_w)
            CopyVisitor().visit(value_copy_w)

            bin_op: BinaryOp = BinaryOp(operator)
            bin_op.lhs_w = assignee_copy_w
            bin_op.rhs_w = value_copy_w
            bin_op.type = node_w.n.type
            bin_op.local_symtab_w.n = node_w.n.local_symtab_w.n

            node_w.n.value_w.n = bin_op
        super().assign(node_w)
