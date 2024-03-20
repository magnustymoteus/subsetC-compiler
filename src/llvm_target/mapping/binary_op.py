from typing import Callable
from src.symbol_table.symbol_table import *
from . import *
from llvmlite import ir

def cast_to_pointer(value: ir.Instruction | ir.Constant, builder: ir.IRBuilder) -> ir.Instruction:
    if isinstance(value, ir.Constant):
        pass

def get_binary_op(left_value: ir.Instruction | ir.Constant, right_value: ir.Instruction | ir.Constant, operator: str,
                  builder: ir.IRBuilder, create_reg: Callable) -> Callable:
    if not (isinstance(left_value.type, ir.PointerType) or isinstance(right_value.type, ir.PointerType)):
        match left_value.type:
            case ir.IntType():
                return get_int_binary_op(left_value, right_value, operator, builder, create_reg)
            case ir.FloatType():
                return get_float_binary_op(left_value, right_value, operator, builder, create_reg)
            case _:
                raise ValueError("unrecognized")
    else:
        if isinstance(left_value.type, ir.PointerType):
            pass