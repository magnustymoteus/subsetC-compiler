import math

from llvmlite import ir
from src.constructs.mips_program.program import MipsProgram
from src.constructs.mips_program.variable import Variables


def assert_type(value, typename):
    assert type(value).__name__ == typename, f"type '{type(value).__name__}' not implemented"


def get_type_size(type: ir.Type) -> int:
    """Get the size of the type in bytes."""
    match type:
        case ir.IntType():
            res = math.ceil(type.width / 8)
        case ir.PointerType():
            res = get_type_size(type.pointee)
        case ir.FloatType():
            res = 4
        case ir.ArrayType():
            res = type.count * get_type_size(type.element)
        case _:
            assert False
    assert res > 0
    return res


def get_args_size(args) -> int:
    """Get the size of the provided arguments in bytes."""
    return sum(get_type_size(arg.type) for arg in args)


class MVBase:
    tree: MipsProgram
    "Tree of the mips program blocks with instructions."

    @property
    def last_block(self):
        """Current block being visited."""
        return self.tree.blocks[-1]

    variables: Variables
    "List of passed variables in current function scope"

    stack_offset: int
    "Largest stack offset used"

    new_function_started: bool
    "True if a new function has just started. Used to indicate to the block visit a new stack frame should be created."
