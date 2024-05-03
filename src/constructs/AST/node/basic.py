from src.constructs.node import *
import html

class Basic(AbstractNode):
    """
    Basic node. Contains attributes shared by all nodes.
    """

    def __init__(self) -> None:
        super().__init__()
        self.line_nr: int | None = None
        self.col_nr: int | None = None
        self.filename: str | None = None
        self.comments = []
        self.source_code_line: str | None = None
        self.local_symtab_w: Wrapper[SymbolTable] = wrap()



    def set_line_col_nr(self, line_nr: int, col_nr: int):
        self.line_nr = line_nr
        self.col_nr = col_nr

    def append_to_graph(self, graph: Digraph, parent_id: UUID | None, label: str | None = None) -> None:
        label_str = html.escape(str(self))
        comment_str = str('<br></br>'.join([html.escape(comment) for comment in self.comments]))
        graph.node(str(self.id), f"<{label_str}<br></br><FONT POINT-SIZE=\"5\">comments: {comment_str}</FONT>>")
        if parent_id is not None:
            graph.edge(str(parent_id), str(self.id), label)


from src.constructs.symbols.symbol_table import SymbolTable



