from llvmlite import ir
from typing import Callable, Optional
from src.constructs.symbols import PrimitiveType

def do_cast(builder: ir.IRBuilder,
              from_type: PrimitiveType, to_type: PrimitiveType) \
        -> Optional[Callable]:
    if from_type.ptr_count > 0 and to_type.ptr_count > 0:
        return builder.bitcast
    if from_type.ptr_count > 0 and to_type.ptr_count == 0:
        return builder.ptrtoint
    if from_type.ptr_count == 0 and to_type.ptr_count > 0:
        return builder.inttoptr
    if from_type.type == to_type.type:
        return None
    # {("from_type", "to_type"): llvmlite_castfunc}
    casts: dict[tuple[str, str], ir.IRBuilder.function] = {
        ("float", "int"): builder.fptosi,
        ("float", "char"): builder.fptosi,
        ("int", "float"): builder.sitofp,
        ("int", "char"): builder.sext,
        ("char", "float"): builder.sitofp,
        ("char", "int"): builder.sext,
    }
    return casts[from_type.type, to_type.type]
