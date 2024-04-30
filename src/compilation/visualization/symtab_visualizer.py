from src.compilation.visitor.AST_visitor.ast_visitor import *

class SymbolTablesVisualizer(ASTVisitor):
    def __init__(self, ast: Ast):
        self.parent_map: dict[UUID, UUID] = {}
        self.symtabs: dict[UUID, SymbolTable] = {}
        super().__init__(ast)
        self.graph = Digraph(strict=True)
        for symtab in self.symtabs.values():
            symtab.append_to_graph(self.graph, self.parent_map.get(symtab.id, None))
    def visit(self, node_w: Wrapper[Basic]):
        symtab = node_w.n.local_symtab_w.n
        if symtab is not None:
            self.symtabs[symtab.id] = symtab
            if symtab.has_parent():
                self.parent_map[symtab.id] = symtab.parent.n.id
        super().visit(node_w)