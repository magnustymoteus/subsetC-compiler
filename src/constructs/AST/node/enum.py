from .basic import *
from src.constructs.symbols.symbol_type import PrimitiveType
class Enumeration(Basic):
    def __init__(self, name: str, chronological_labels: list[str]):
        '''
        :param chronological_labels: A list of the labels that represent integer constants starting from 0
        '''
        super().__init__()
        self.name: str = name
        self.chronological_labels: list[str] = chronological_labels
        self.type: PrimitiveType = PrimitiveType('int')
    def __repr__(self):
        return f"enum {self.name} {[label for label in self.chronological_labels]} ({self.type.__repr__()})"