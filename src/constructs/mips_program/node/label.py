from src.constructs.mips_program.node.node import Node


class Label(Node):
    """Node representing a MIPS label"""

    label: str
    "Jump label"

    def __init__(self, label: str) -> None:
        self.label = label
        super().__init__()

    def __str__(self) -> str:
        return f"{self.label}:"
