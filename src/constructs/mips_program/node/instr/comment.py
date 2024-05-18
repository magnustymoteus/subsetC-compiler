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

class CComment(Comment):
    """
    Node representing a comment originating from C or containing C code
    """

    def __init__(self, text: str) -> None:
        super().__init__(text)

    def __str__(self) -> str:
        return f"# C: {self.text}"

class IrComment(Comment):
    """
    Node representing an IR comment
    """

    def __init__(self, text: str) -> None:
        super().__init__(text)

    def __str__(self) -> str:
        return f"# IR: {self.text}"

class Blank(Instruction):
    """
    Node representing a blank line
    """

    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return ""