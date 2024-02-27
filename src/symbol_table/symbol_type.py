class SymbolType:
    def __init__(self, is_constant: bool = False):
        self.is_constant: bool = is_constant

class PrimitiveType(SymbolType):
    def __init__(self, type: str, is_constant: bool = False):
        self.type: str = type
        super().__init__(is_constant)

class PointerType(SymbolType):
    def __init__(self, is_constant: bool = False):
        super().__init__(is_constant)
class ReferenceType(SymbolType):
    def __init__(self, is_constant: bool = False):
        super().__init__(is_constant)

class ArrayType(SymbolType):
    def __init__(self, element_type: str, is_constant: bool = False):
        self.element_type: str = element_type
        super().__init__(is_constant)

class FunctionType(SymbolType):
    def __init__(self, is_constant: bool = False):
        super().__init__(is_constant)