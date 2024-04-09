from ..basic import *
from src.symbol_table.symbol_type import PrimitiveType
class Expression(Basic):
    def __init__(self):
        self._type: PrimitiveType | None = None
        super().__init__()
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
    def get_typed_str(self, repr_str: str):
        if self.type is not None:
            return f"{repr_str} ({self.type})"
        return str(repr_str)
    @property
    def type(self) -> PrimitiveType:
        if self._type is not None:
            if self.local_symtab_w.n is not None and self.local_symtab_w.n.symbol_exists(self._type.type):
                return self.local_symtab_w.n.lookup_symbol(self._type.type).type
        return self._type
    @type.setter
    def type(self, value: PrimitiveType):
        self._type = value

