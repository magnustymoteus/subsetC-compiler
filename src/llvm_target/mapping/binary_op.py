from typing import Callable
from .int import *
from .float import *
from .pointer import *
from llvmlite import ir



def get_binary_op(left_value: ir.Instruction | ir.Constant, right_value: ir.Instruction | ir.Constant, operator: str,
                  builder: ir.IRBuilder, create_reg: Callable) -> Callable:
    if isinstance(left_value.type, ir.PointerType) or isinstance(right_value.type, ir.PointerType):
        return get_pointer_binary_op(left_value, right_value, operator, builder, create_reg)
    else:
        match left_value.type:
            case ir.IntType():
                return get_int_binary_op(left_value, right_value, operator, builder, create_reg)
            case ir.FloatType():
                return get_float_binary_op(left_value, right_value, operator, builder, create_reg)
            case _:
                raise ValueError("unrecognized")