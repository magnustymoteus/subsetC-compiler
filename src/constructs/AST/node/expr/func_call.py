from .expr import *
class FunctionCall(Expression):
    def __init__(self, func_name: str, arguments: list[Wrapper[Expression]]):
        super().__init__()
        self.func_name: str = func_name
        self.arguments: list[Wrapper[Expression]] = arguments
    def __repr__(self):
        return super().get_typed_str(f"call {self.func_name}")
    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        super().append_to_graph(graph, parent_id, label)
        for i, arg_w in enumerate(self.arguments):
            arg_w.n.append_to_graph(graph, self.id, f"argument {i}")