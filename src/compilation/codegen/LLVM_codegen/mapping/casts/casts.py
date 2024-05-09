from llvmlite import ir
from typing import Callable, Optional
from src.constructs.symbols import PrimitiveType

def do_cast(value, from_type: PrimitiveType, to_type: PrimitiveType) \
        -> Optional[Callable]:
    if from_type.ptr_count > 0 and to_type.ptr_count > 0:
        return value.bitcast
    if from_type.ptr_count > 0 and to_type.ptr_count == 0:
        return value.ptrtoint
    if from_type.ptr_count == 0 and to_type.ptr_count > 0:
        return value.inttoptr
    if from_type.type == to_type.type:
        return None
    # {("from_type", "to_type"): llvmlite_castfunc}
    casts: dict[tuple[str, str], ir.IRBuilder.function] = {
        ("float", "int"): value.fptosi,
        ("float", "char"): value.fptosi,
        ("int", "float"): value.sitofp,
        ("int", "char"): value.trunc,
        ("char", "float"): value.sitofp,
        ("char", "int"): value.sext,
    }
    return casts[from_type.type, to_type.type]
