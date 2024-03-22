from .basic import Digraph, Wrapper, wrap
from .block_item import BlockItem
from uuid import UUID
from src.symbol_table import SymbolType
class VariableDeclaration(BlockItem):

    def __init__(self, identifier: str, type: SymbolType, storage_class_specifier = None):
        self.identifier: str = identifier
        self._type: SymbolType = type
        self.definition_w: Wrapper = wrap()
        self.storage_class_specifier: str | None = storage_class_specifier
        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)
        if self.definition_w.n is not None:
            self.definition_w.n.append_to_graph(graph, self.id)
        #if self.local_symtab_w.n is not None:
        #    self.local_symtab_w.n.append_to_graph(graph, self.id)

    @property
    def type(self) -> SymbolType:
        if self._type is not None:
            if self.local_symtab_w.n is not None and self.local_symtab_w.n.symbol_exists(self._type.type):
                return self.local_symtab_w.n.lookup_symbol(self._type.type).type
        return self._type
    @type.setter
    def type(self, value: SymbolType):
        self._type = value


    def __repr__(self) -> str:
        if self.storage_class_specifier == "typedef":
            res = f"type definition {self.identifier}"
        else:
            res = f"definition: {self.identifier}" if self.definition_w.n is not None else f"declaration: {self.identifier}"
        return f"{res} ({self.type.__repr__()})"

