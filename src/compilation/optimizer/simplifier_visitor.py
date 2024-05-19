from src.compilation.visitor.AST_visitor import *
from src.constructs import *
class SimplifierVisitor(ASTVisitor):
    def __init__(self, ast: Ast):
        super().__init__(ast)

    def compound_stmt(self, node_w: Wrapper[CompoundStatement]):
        for i, stmt_w in enumerate(node_w.n.statements):
            if isinstance(stmt_w.n, JumpStatement):
                node_w.n.statements = node_w.n.statements[:i + 1]
                break
        super().compound_stmt(node_w)

    def assign(self, node_w: Wrapper[Assignment]):
        if len(node_w.n.operator) > 1:
            operator: str = node_w.n.operator[0]
            node_w.n.operator = "="
            assignee_copy_w: Wrapper[Identifier] = wrap(node_w.n.assignee_w.n)
            value_copy_w: Wrapper[Expression] = wrap(node_w.n.value_w.n)
            CopyVisitor().visit(assignee_copy_w)
            CopyVisitor().visit(value_copy_w)

            bin_op: BinaryOp = BinaryOp(operator)
            bin_op.lhs_w = assignee_copy_w
            bin_op.rhs_w = value_copy_w
            bin_op.type = node_w.n.type
            bin_op.local_symtab_w.n = node_w.n.local_symtab_w.n

            node_w.n.value_w.n = bin_op
        super().assign(node_w)

    def bin_op(self, node_w: Wrapper[BinaryOp]):
        super().bin_op(node_w)
        match node_w.n.operator:
                case ">>":
                    if isinstance(node_w.n.rhs, UnaryOp) and node_w.n.rhs.operator == "-" and isinstance(node_w.n.rhs.operand, (CharLiteral, IntLiteral)):
                        node_w.n.rhs = node_w.n.rhs.operand
                        node_w.n.operator = "<<"
                case "<<":
                    if isinstance(node_w.n.lhs, UnaryOp) and node_w.n.lhs.operator == "-" and isinstance(
                            node_w.n.lhs.operand, (CharLiteral, IntLiteral)):
                        node_w.n.operator = ">>"
                        node_w.n.lhs = node_w.n.lhs.operand
                case _:
                    if node_w.n.operator in ["&&", "||"]:
                        node_w.n.lhs_w = wrap(BinaryOp("!=", node_w.n.lhs_w, wrap(IntLiteral(0))))
                        node_w.n.rhs_w = wrap(BinaryOp("!=", node_w.n.rhs_w, wrap(IntLiteral(0))))
