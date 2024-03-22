class SymbolType:
    def __init__(self, is_constant: bool = False):
        self.is_constant: bool = is_constant

class PrimitiveType(SymbolType):
    def __init__(self, type: str, is_constant: bool = False, ptr_count: int = 0, const_ptrs: list[int] = []):
        self.type: str = type
        self.ptr_count: int = ptr_count
        self.const_ptrs: list[int] = const_ptrs
        super().__init__(is_constant)
    def __repr__(self):
        ptr_str = '*'*self.ptr_count
        for const_ptr_index in self.const_ptrs:
            ptr_str = ptr_str[:const_ptr_index+1] + "const" + ptr_str[const_ptr_index+1:]
        result = f"{self.type}" if not self.is_constant else f"const {self.type}"
        return f"{result}{ptr_str}"
    def decrease_ptr_count(self):
        if self.ptr_count-1 in self.const_ptrs:
            self.const_ptrs.remove(self.ptr_count-1)
        self.ptr_count -= 1
    def increase_ptr_count(self):
        self.ptr_count += 1


class ArrayType(SymbolType):
    def __init__(self, element_type: str, is_constant: bool = False):
        self.element_type: str = element_type
        super().__init__(is_constant)

class FunctionType(SymbolType):
    def __init__(self, is_constant: bool = False):
        super().__init__(is_constant)


"""
class PointerType(SymbolType):
    def __init__(self, is_constant: bool = False):
        super().__init__(is_constant)
class ReferenceType(SymbolType):
    def __init__(self, is_constant: bool = False):
        super().__init__(is_constant)
"""