from src.constructs import *
from src.compilation.visitor.AST_visitor import ASTVisitor

'''Semantic analysis of declarations (resolving forward declarations) '''
class ResolverVisitor(ASTVisitor):
    def __init__(self, ast: Ast, stdio_included: bool = False):
        self.is_main_defined: bool = False
        self.stdio_included: bool = stdio_included
        self.func_decls: dict[str, Wrapper[FunctionDeclaration]] = {}
        self.func_decl_instances: dict[str, list[Wrapper[FunctionDeclaration]]] = {}
        super().__init__(ast)
        if not self.is_main_defined:
            self.raiseSemanticErr("undefined reference to main")
        for name, node_w in self.func_decls.items():
            if node_w.n.body_w.n is None:
                self.raiseSemanticErr(f"function {name} declared but never defined")
            else:
                self.func_decl_instances[name][0].n = node_w.n
    def program(self, node_w: Wrapper[Program]):
        super().program(node_w)
        for name, func_decls in self.func_decl_instances.items():
            for func_decl_w in func_decls[1:]:
                node_w.n.children.remove(func_decl_w)

    def signature_match(self, type1: FunctionType, type2: FunctionType) -> bool:
        return type1.parameter_types == type2.parameter_types and type1.return_type == type2.return_type

    def io(self, node_w: Wrapper[IOStatement]):
        if not self.stdio_included:
            self.raiseSemanticErr(f"undefined reference to {node_w.n.name}: stdio.h not included")

    def func_decl(self, node_w: Wrapper[FunctionDeclaration]):
        super().func_decl(node_w)
        if node_w.n.name == 'main':
            self.is_main_defined = True
        found = self.func_decls.get(node_w.n.name, False)
        if not found:
            self.func_decls[node_w.n.name] = node_w
            self.func_decl_instances[node_w.n.name] = [node_w]
        else:
            self.func_decl_instances[node_w.n.name].append(node_w)
            # TODO: allow function overloading in the future
            if not self.signature_match(node_w.n.type, found.n.type):
                self.raiseSemanticErr(f"conflicting types for function {node_w.n.name}: {node_w.n.type} and {found.n.type}")
            if node_w.n.body_w.n is not None and found.n.body_w.n is not None:
                self.raiseSemanticErr(f"redefinition of function {node_w.n.name}")
            elif node_w.n.body_w.n and found.n.body_w.n is None:
                self.func_decls[node_w.n.name] = node_w


