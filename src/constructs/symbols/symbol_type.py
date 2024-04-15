class SymbolType:
    def __init__(self, is_constant: bool = False, ptr_count: int = 0, const_ptrs: list[int] = []):
        self.is_constant: bool = is_constant
        self.ptr_count: int = ptr_count
        self.const_ptrs: list[int] = const_ptrs
    def decrease_ptr_count(self):
        if self.ptr_count-1 in self.const_ptrs:
            self.const_ptrs.remove(self.ptr_count-1)
        self.ptr_count -= 1
    def increase_ptr_count(self):
        self.ptr_count += 1


class VoidType(SymbolType):
    pass

class PrimitiveType(SymbolType):
    def __init__(self, type: str, is_constant: bool = False, ptr_count: int = 0, const_ptrs: list[int] = []):
        self.type: str = type
        super().__init__(is_constant, ptr_count, const_ptrs)
    def __repr__(self):
        ptr_str = '*'*self.ptr_count
        added = 0
        for const_ptr_index in self.const_ptrs:
            ptr_str = ptr_str[:const_ptr_index+1+added] + "const" + ptr_str[const_ptr_index+1+added:]
            added += 5
        result = f"{self.type}" if not self.is_constant else f"const {self.type}"
        return f"{result}{ptr_str}"

class FunctionType(SymbolType):
    def __init__(self, return_type: SymbolType, parameter_types: list[SymbolType]):
        self.return_type: SymbolType = return_type
        self.parameter_types: list[SymbolType] = parameter_types
        super().__init__()
    def __repr__(self):
        return f"{self.return_type} ({self.parameter_types})"


'''class ArrayType(SymbolType):
    def __init__(self, element_type: str, is_constant: bool = False):
        self.element_type: str = element_type
        super().__init__(is_constant)'''