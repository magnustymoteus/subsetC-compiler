from src.parser.AST.ast import *
from src.parser.AST.node import *

def constant_folding(ast: Ast):
    for node_w in ast.iter(AstIter):
        match node_w.n:
            case BinaryOp():
                if isinstance(node_w.n.lhs, Literal) and isinstance(node_w.n.rhs, Literal):
                    result = node_w.n
                    match node_w.n.operator:
                        case "+":
                            result = node_w.n.lhs.value + node_w.n.rhs.value
                        case "-":
                            result = node_w.n.lhs.value - node_w.n.rhs.value
                        case "*":
                            result = node_w.n.lhs.value * node_w.n.rhs.value
                        case "/":
                            result = node_w.n.lhs.value / node_w.n.rhs.value
                        case ">":
                            result = node_w.n.lhs.value > node_w.n.rhs.value
                        case "<":
                            result = node_w.n.lhs.value < node_w.n.rhs.value
                        case "==":
                            result = node_w.n.lhs.value == node_w.n.rhs.value
                        case "&&":
                            result = node_w.n.lhs.value and node_w.n.rhs.value
                        case "||":
                            result = node_w.n.lhs.value or node_w.n.rhs.value
                        case ">=":
                            result = node_w.n.lhs.value >= node_w.n.rhs.value
                        case "<=":
                            result = node_w.n.lhs.value <= node_w.n.rhs.value
                        case "!=":
                            result = node_w.n.lhs.value != node_w.n.rhs.value
                        case "%":
                            result = node_w.n.lhs.value % node_w.n.rhs.value
                        case "<<":
                            if node_w.n.rhs.value >= 0:
                                result = node_w.n.lhs.value << node_w.n.rhs.value
                            else:
                                result = node_w.n.lhs.value >> abs(
                                    node_w.n.rhs.value)
                        case ">>":
                            if node_w.n.rhs.value >= 0:
                                result = node_w.n.lhs.value >> node_w.n.rhs.value
                            else:
                                result = node_w.n.lhs.value << abs(
                                    node_w.n.rhs.value)
                        case "&":
                            result = node_w.n.lhs.value & node_w.n.rhs.value
                        case "|":
                            result = node_w.n.lhs.value | node_w.n.rhs.value
                        case "^":
                            result = node_w.n.lhs.value ^ node_w.n.rhs.value
                    if isinstance(result, bool):
                        node_w.n = IntLiteral(1 if result else 0)
                    elif isinstance(result, float):
                        node_w.n = FloatLiteral(result)
                    else:
                        node_w.n = IntLiteral(result)

            case UnaryOp():
                if isinstance(node_w.n.operand, Literal) and not node_w.n.is_postfix:
                    result = node_w.n
                    match node_w.n.operator:
                        case "+":
                            result = node_w.n.operand.value
                        case "-":
                            result = -node_w.n.operand.value
                        case "--":
                            result = node_w.n.operand.value - 1
                        case "++":
                            result = node_w.n.operand.value + 1
                        case "!":
                            result = not node_w.n.operand.value
                        case "~":
                            result = ~node_w.n.operand.value
                    literal_type = type(node_w.n.operand)
                    node_w.n = literal_type(result)
            case CastOp():
                if isinstance(node_w.n.expression_w.n, Literal):
                    result = node_w.n
                    match node_w.n.target_type.type:
                        case "int":
                            result = IntLiteral(int(node_w.n.expression_w.n.value))
                        case "float":
                            result = FloatLiteral(float(node_w.n.expression_w.n.value))
                        case "char":
                            result = CharLiteral(int(node_w.n.expression_w.n.value))
                        case _:
                            raise Exception("Critical error: unknown cast passed type checks")
                    result.type = node_w.n.target_type
                    node_w.n = result

