from .instruction import Instruction


class Comment(Instruction):
    """
    Node representing a MIPS comment
    """

    text: str
    "Comment text"

    def __init__(self, text: str) -> None:
        self.text = text
        super().__init__()

    def __str__(self) -> str:
        return f"# {self.text}"
