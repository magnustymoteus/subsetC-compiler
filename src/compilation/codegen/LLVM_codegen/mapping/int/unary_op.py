from llvmlite.ir import IRBuilder
from src.constructs.AST.node import *

def do_signed_int_unary_op(operator: str, builder: IRBuilder, node: UnaryOp):
    match operator:
        case "+":
            pass
        case "-":
            pass
        case "!":
            pass
        case "~":
            pass
        case "&":
            pass
        case "*"
            pass
        case "++":
            pass
        case "--":
            pass
