from llvmlite import ir
from typing import Callable

def is_pointer(value: ir.Instruction | ir.Constant) -> bool:
    return isinstance(value.type, ir.PointerType)

def get_pointer(left: ir.Instruction, right: ir.Instruction) -> ir.Instruction:
    return left if is_pointer(left) else right


def get_non_pointer(left: ir.Instruction, right: ir.Instruction) -> ir.Instruction:
    return left if not is_pointer(left) else right



def cast_toptr_if_constant(value: ir.Instruction | ir.Constant, pointer_type: ir.PointerType, builder: ir.IRBuilder,
                     create_reg: Callable) -> ir.Instruction:
    return builder.inttoptr(value, pointer_type, create_reg()) if isinstance(value.type, ir.Constant) else value

def get_pointer_comparison(left_value: ir.Instruction | ir.Constant, right_value: ir.Instruction | ir.Constant, operator: str, builder: ir.IRBuilder, create_reg: Callable) -> ir.Instruction:
    pointer_type = get_pointer(left_value, right_value).type
    left_value = cast_toptr_if_constant(left_value, pointer_type, builder, create_reg())
    right_value = cast_toptr_if_constant(right_value, pointer_type, builder, create_reg())
    comp_op = builder.icmp_signed(operator, left_value, right_value, create_reg())
    return builder.zext(comp_op, ir.IntType(32), create_reg())



def get_pointer_binary_op(left_value: ir.Instruction | ir.Constant, right_value: ir.Instruction | ir.Constant,
                          operator: str,
                          builder: ir.IRBuilder, create_reg: Callable) -> Callable:
    match operator:
        case '+':
            return lambda: builder.gep(get_pointer(left_value, right_value),
                                       [builder.sext(get_non_pointer(left_value, right_value), ir.IntType(64), create_reg())],
                                       True, create_reg())
        case '-':
            if is_pointer(left_value) and is_pointer(right_value):
                pass
            return lambda: builder.gep(get_pointer(left_value, right_value),
                                       [builder.neg(get_non_pointer(left_value, right_value), create_reg())], True,
                                       create_reg())
        case _:
            return lambda: get_pointer_comparison(left_value, right_value, operator, builder, create_reg)
