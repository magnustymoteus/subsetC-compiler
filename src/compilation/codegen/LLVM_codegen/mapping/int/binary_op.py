from llvmlite import ir
from typing import Callable

def get_int_boolean_binary_op(left_value: ir.Instruction | ir.Constant, right_value: ir.Instruction | ir.Constant,
                          operator: str,
                          builder: ir.IRBuilder, create_reg: Callable, boolean_op: Callable) -> ir.Instruction:
    return builder.zext(boolean_op(), ir.IntType(32), create_reg())
def get_int_logical_comp_op(op: Callable, builder: ir.IRBuilder, create_reg: Callable):
    return builder.zext(builder.icmp_signed('!=', op(), ir.Constant(ir.IntType(32), 0)), ir.IntType(32), create_reg())
def get_int_binary_op(left_value: ir.Instruction | ir.Constant, right_value: ir.Instruction | ir.Constant, operator: str,
                             builder: ir.IRBuilder, create_reg: Callable) -> Callable:
    match operator:
        case "+":
            return lambda: builder.add(left_value, right_value, create_reg())
        case "-":
            return lambda: builder.sub(left_value, right_value, create_reg())
        case "*":
            return lambda: builder.mul(left_value, right_value, create_reg())
        case "/":
            return lambda: builder.sdiv(left_value, right_value, create_reg())
        case "%":
            return lambda: builder.srem(left_value, right_value, create_reg())
        case "<<":
            return lambda: builder.shl(left_value, right_value, create_reg())
        case ">>":
            return lambda: builder.ashr(left_value, right_value, create_reg())
        case "|":
            return lambda: builder.or_(left_value, right_value, create_reg())
        case "||":
            rel_op= lambda: builder.or_(left_value, right_value, create_reg())
            return lambda: get_int_logical_comp_op(rel_op, builder, create_reg)
        case "^":
            return lambda: builder.xor(left_value, right_value, create_reg())
        case "&":
            return lambda: builder.and_(left_value, right_value, create_reg())
        case "&&":
            rel_op = lambda: builder.and_(left_value, right_value, create_reg())
            return lambda: get_int_logical_comp_op(rel_op, builder, create_reg)
        case _:
            comp_op: Callable = lambda: builder.icmp_signed(operator, left_value, right_value, create_reg())
            return lambda: get_int_boolean_binary_op(left_value, right_value, operator, builder, create_reg, comp_op)
