from llvmlite import ir
from typing import Callable

def is_pointer(value: ir.Instruction | ir.Constant) -> bool:
    return value.type.is_pointer

def get_pointer(left: ir.Instruction, right: ir.Instruction) -> ir.Instruction:
    return left if is_pointer(left) else right


def get_non_pointer(left: ir.Instruction, right: ir.Instruction) -> ir.Instruction:
    return left if not is_pointer(left) else right

def cast_toptr_if_constant(value: ir.Instruction | ir.Constant, pointer_type: ir.PointerType, builder: ir.IRBuilder, reg_name) -> ir.Instruction:
    return builder.inttoptr(value, pointer_type, reg_name) if not value.type.is_pointer else value

def get_pointer_relational_comparison(left_value: ir.Instruction | ir.Constant, right_value: ir.Instruction | ir.Constant, operator: str, builder: ir.IRBuilder, create_reg: Callable) -> ir.Instruction:
    pointer_type = get_pointer(left_value, right_value).type

    left_value = cast_toptr_if_constant(left_value, pointer_type, builder, create_reg())
    right_value = cast_toptr_if_constant(right_value, pointer_type, builder, create_reg())

    comp_op = builder.icmp_unsigned(operator, left_value, right_value, create_reg())

    return builder.zext(comp_op, ir.IntType(32), create_reg())
def get_pointer_logical_value(value, builder: ir.IRBuilder, create_reg) -> ir.Instruction:
    if value.type.is_pointer:
        return builder.zext(builder.icmp_unsigned('!=', value, ir.Constant(value.type, None), create_reg()), ir.IntType(32), create_reg())
    return value


def get_pointer_logical_comparison(left_value, right_value, op: Callable, builder: ir.IRBuilder, create_reg: Callable):
    lhs = get_pointer_logical_value(left_value, builder, create_reg)
    rhs = get_pointer_logical_value(right_value, builder, create_reg)
    log_op = op(lhs, rhs, create_reg())
    return builder.zext(log_op, ir.IntType(32), create_reg())

def get_pointer_binary_op(left_value: ir.Instruction | ir.Constant, right_value: ir.Instruction | ir.Constant,
                          operator: str,
                          builder: ir.IRBuilder, create_reg: Callable) -> Callable:
    match operator:
        case '+':
            return lambda: builder.gep(get_pointer(left_value, right_value),
                                       [builder.zext(get_non_pointer(left_value, right_value), ir.IntType(64), create_reg())],
                                       True, create_reg())
        case '-':
            if is_pointer(left_value) and is_pointer(right_value):
                return lambda: builder.sdiv(
                    builder.sub(builder.ptrtoint(left_value,ir.IntType(64), create_reg()),
                                        builder.ptrtoint(right_value, ir.IntType(64), create_reg()),
                                                            create_reg()),
                ir.Constant(ir.IntType(64), 4), create_reg())
            return lambda: builder.gep(get_pointer(left_value, right_value),
                                       [builder.zext(
                                           builder.neg(get_non_pointer(left_value, right_value), create_reg()), ir.IntType(64)
                                           ,create_reg())], True,
                                       create_reg())
        case '||':
            return lambda: get_pointer_logical_comparison(left_value, right_value, builder.or_, builder, create_reg)
        case '&&':
            return lambda: get_pointer_logical_comparison(left_value, right_value, builder.and_, builder, create_reg)
        case _:
            return lambda: get_pointer_relational_comparison(left_value, right_value, operator, builder, create_reg)
