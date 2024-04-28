from src.constructs import *
from src.compilation.visitor.AST_visitor import ASTVisitor
class MainChecker(ASTVisitor):
    def __init__(self, ast: Ast):
        super().__init__(ast)

    def func_decl(self, node_w: Wrapper[FunctionDeclaration]):
        if node_w.n.identifier == "main":
            last_stmt = node_w.n.definition_w.n.statements[-1].n
            return_type = node_w.n.type.return_type
            if return_type.type == "int" and not return_type.ptr_count and isinstance(last_stmt, ReturnStatement):
                if not (isinstance(last_stmt.expr_w.n, IntLiteral) and last_stmt.expr_w.n.value == 0):
                    self.raiseSemanticErr(f"main exited with error code {last_stmt.expr_w.n}")

