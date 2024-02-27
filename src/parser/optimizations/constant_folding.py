from ..ast import *


def constant_folding(ast: Ast):
    for node_w in ast.iter(AstIter):
        match node_w.n:
            case BinaryOp():
                if isinstance(node_w.n.lhs, IntLiteral) and isinstance(node_w.n.rhs, IntLiteral):
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

                    node_w.n = IntLiteral(result)

            case UnaryOp():
                if isinstance(node_w.n.operand, IntLiteral):
                    result = node_w.n
                    match node_w.n.operator:
                        case "+":
                            result = node_w.n.operand.value
                        case "-":
                            result = -node_w.n.operand.value
                        case "!":
                            result = not node_w.n.operand.value
                        case "~":
                            result = ~node_w.n.operand.value

                    node_w.n = IntLiteral(result)
