from llvmlite import ir
from typing import Callable

def do_cast(builder: ir.IRBuilder,
              from_type: ir.Type, to_type: ir.Type, value: ir.Instruction | ir.Constant, create_reg: Callable) \
        -> ir.Instruction:
    if from_type == to_type:
        return value
    if not isinstance(from_type, ir.PointerType) and isinstance(to_type, ir.PointerType):
        return builder.inttoptr(value, to_type, create_reg())
    if isinstance(from_type, ir.PointerType) and isinstance(to_type, ir.PointerType):
        return builder.bitcast(value, to_type, create_reg())
    # {("from_type", "to_type"): llvmlite_castfunc}
    casts: dict[tuple[ir.Type, ir.Type], ir.IRBuilder.function] = {
        (ir.FloatType(), ir.IntType(32)): builder.fptosi,
        (ir.FloatType(), ir.IntType(8)): builder.fptosi,
        (ir.IntType(32), ir.FloatType()): builder.sitofp,
        (ir.IntType(32), ir.IntType(8)): builder.sext,
        (ir.IntType(8), ir.FloatType()): builder.sitofp,
        (ir.IntType(8), ir.IntType(32)): builder.sext,
    }
    return casts[from_type, to_type](value, to_type, create_reg())
