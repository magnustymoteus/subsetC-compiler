from src.symbol_table import SymbolType
from src.parser.AST.node.compound_stmt import *

class FunctionDefinition(Basic):

    def __init__(self, return_type: SymbolType, name: str, parameter_list) -> None:
        self.return_type: SymbolType = return_type
        self.parameter_list = parameter_list
        self.body_w : Wrapper[CompoundStatement] = wrap()
        self.name = name

        super().__init__()

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None) -> None:
        super().append_to_graph(graph, parent_id)

    def __repr__(self) -> str:
        return f"{self.return_type} {self.name}({self.parameter_list})"