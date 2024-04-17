from src.constructs.AST.node.stmt.compound_stmt import *
from .basic import *
from .variable_decl import *
from src.constructs.symbols.symbol_type import FunctionType

class FunctionDeclaration(VariableDeclaration):

    def __init__(self, name: str, type: FunctionType, parameters: list[Wrapper[VariableDeclaration]] = [], body_w: Wrapper[CompoundStatement | None] = None) -> None:
        self.parameters: list[Wrapper[VariableDeclaration]] = parameters
        super().__init__(name, type)
        self.definition_w : Wrapper[CompoundStatement | None] = body_w if body_w is not None else wrap()


    @property
    def body_w(self) -> Wrapper[CompoundStatement]:
        return self.definition_w
    @body_w.setter
    def body_w(self, value_w: Wrapper[CompoundStatement]):
        self.definition_w = value_w
    @property
    def name(self) -> str:
        return self.identifier
    @name.setter
    def name(self, name: str):
        self.identifier = name

    @property
    def type(self) -> FunctionType:
        return self._type

    @type.setter
    def type(self, value: FunctionType):
        self._type = value
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        for i, param_w in enumerate(self.parameters):
            param_w.n.append_to_graph(graph, self.id, f"parameter {i}")
        if self.definition_w is not None:
            self.definition_w.n.append_to_graph(graph, self.id, "definition")
    def __repr__(self) -> str:
        return f"function declaration {self.identifier} ({self.type})"
