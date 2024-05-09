from llvmlite import ir
from typing import Callable

def get_float_boolean_binary_op(left_value: ir.Instruction | ir.Constant, right_value: ir.Instruction | ir.Constant,
                          operator: str,
                          builder: ir.IRBuilder, create_reg: Callable, boolean_op: Callable) -> ir.Instruction:
    return builder.zext(boolean_op(), ir.IntType(32), create_reg())

def get_float_logical_comp_op(op: Callable, builder: ir.IRBuilder, create_reg: Callable):
    return builder.zext(op(), ir.IntType(32), create_reg())

def get_float_binary_op(left_value: ir.Instruction | ir.Constant, right_value: ir.Instruction | ir.Constant, operator: str,
                        builder: ir.IRBuilder, create_reg: Callable) -> Callable:
    match operator:
        case "+":
            return lambda: builder.fadd(left_value, right_value, create_reg())
        case "-":
            return lambda: builder.fsub(left_value, right_value, create_reg())
        case "*":
            return lambda: builder.fmul(left_value, right_value, create_reg())
        case "/":
            return lambda: builder.fdiv(left_value, right_value, create_reg())
        case "%":
            return lambda: builder.frem(left_value, right_value, create_reg())
        case "<<":
            return lambda: builder.ashr(left_value, right_value, create_reg())
        case ">>":
            return lambda: builder.shl(left_value, right_value, create_reg())
        case "|":
            return lambda: builder.or_(left_value, right_value, create_reg())
        case "||":
            rel_op = lambda: builder.or_(
                builder.fcmp_unordered('!=', left_value, ir.Constant(ir.FloatType(), 0.0)),
                builder.fcmp_unordered('!=', right_value, ir.Constant(ir.FloatType(), 0.0)), create_reg())
            return lambda: get_float_logical_comp_op(rel_op, builder, create_reg)
        case "^":
            return lambda: builder.xor(left_value, right_value, create_reg())
        case "&":
            return lambda: builder.and_(left_value, right_value, create_reg())
        case "&&":
            rel_op = lambda: builder.and_(
                builder.fcmp_unordered('!=', left_value, ir.Constant(ir.FloatType(), 0.0)),
                builder.fcmp_unordered('!=', right_value, ir.Constant(ir.FloatType(), 0.0)), create_reg())
            return lambda: get_float_logical_comp_op(rel_op, builder, create_reg)
        case _:
            comp_op: Callable = lambda: builder.fcmp_unordered(operator, left_value, right_value, create_reg())
            return lambda: get_float_boolean_binary_op(left_value, right_value, operator, builder, create_reg, comp_op)
