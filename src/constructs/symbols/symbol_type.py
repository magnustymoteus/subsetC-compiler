from __future__ import annotations
class SymbolType:
    type_ranks: list[str] = ["char", "int", "float", "struct", "union"]
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
    def get_pointer_string(self) -> str:
        ptr_str = '*' * self.ptr_count
        added = 0
        for const_ptr_index in self.const_ptrs:
            ptr_str = ptr_str[:const_ptr_index + 1 + added] + "const" + ptr_str[const_ptr_index + 1 + added:]
            added += 5
        return ptr_str


class VoidType(SymbolType):
    pass

class PrimitiveType(SymbolType):
    @staticmethod
    def typeCoercion(primitive_types: list[PrimitiveType], is_constant: bool) -> PrimitiveType:
        """
        Perform type coercion on a list of primitive types.

        Args:
            primitive_types (list[str]): The list of primitive types to perform type coercion on.
            is_constant (bool): True if the resulting type should be constant, False otherwise.

        Returns:
            PrimitiveType: The resulting type after type coercion.
        """
        current_rank = 0
        for current_type in primitive_types:
            # check if there is a pointer, if so coerce to that pointer (doesn't do extra checks)
            if current_type.ptr_count > 0:
                return current_type
            index = PrimitiveType.type_ranks.index(current_type.type)
            if index > current_rank:
                current_rank = index
        return PrimitiveType(PrimitiveType.type_ranks[current_rank], is_constant)
    def __init__(self, type: str, is_constant: bool = False, ptr_count: int = 0, const_ptrs: list[int] = []):
        self.type: str = type
        super().__init__(is_constant, ptr_count, const_ptrs)
    def __repr__(self):
        result = f"{self.type}" if not self.is_constant else f"const {self.type}"
        return f"{result}{self.get_pointer_string()}"
    def __eq__(self, other):
        return self.type == other.type and self.ptr_count == other.ptr_count

class FunctionType(SymbolType):
    def __init__(self, return_type: SymbolType, parameter_types: list[SymbolType]):
        self.return_type: SymbolType = return_type
        self.parameter_types: list[SymbolType] = parameter_types
        super().__init__()
    def __repr__(self):
        return f"{self.return_type} ({self.parameter_types})"
# struct or union type
class CompositeType(SymbolType):
    def __init__(self, name: str, type: str):
        assert type in ["union", "struct"]
        self.type: str = type
        self.name: str = name
        super().__init__()
    def __repr__(self):
        return f"{self.type} {self.name}{super().get_pointer_string()}"
    def __eq__(self, other: CompositeType):
        return self.type == other.type and self.name == other.name


class ArrayType(PrimitiveType):
    def __init__(self, element_type: SymbolType, dimension: list[int]):
        self.element_type: SymbolType = element_type
        self.dimension = dimension
        super().__init__(element_type.type, element_type.is_constant, len(dimension))
    def get_dimension_string(self) -> str:
        return "".join([f"[{num}]" for num in self.dimension])
    def __repr__(self):
        return f"{super().__repr__()} (array)"

