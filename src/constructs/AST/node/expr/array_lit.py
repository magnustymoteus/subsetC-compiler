from __future__ import annotations
from .lit import *
from ..basic import *
from src.constructs.symbols.symbol_type import *
from copy import deepcopy

class ArrayLiteral(Literal):

    def __init__(self, values: list[Wrapper]):
        super().__init__(values)

    @staticmethod
    def to_array(lit: ArrayLiteral):
        result = [value_w for value_w in lit.value]
        for i, elem_w in enumerate(result):
            if isinstance(elem_w.n, ArrayLiteral):
                result[i] = ArrayLiteral.to_array(elem_w.n)
        return result


    def adjust(self, dimension: list[int], elem_type: PrimitiveType):
        assert len(dimension) == len(self.type.dimension)
        self.type.element_type = elem_type
        self.value = self.value[:dimension[0]]
        default_lit = Literal(0)
        default_lit.type = elem_type
        if dimension[0] > len(self.value):
            self.value += [wrap(default_lit)]*(dimension[0]-len(self.value))
        for elem_w in self.value:
            if len(dimension) > 1 and not isinstance(elem_w.n.type, ArrayType):
                elem_w.n = ArrayLiteral([wrap(elem_w.n)])
            if isinstance(elem_w.n.type, ArrayType):
                elem_w.n.adjust(dimension[1:], elem_type)
        self.type.dimension = dimension
        assert dimension[0] == len(self.value)



    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)

    def __repr__(self):
        return self.get_typed_str(f"{[elem.n.__repr__() for elem in self.value]}")

