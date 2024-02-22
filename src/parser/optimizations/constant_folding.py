from ..AST import *


def constant_folding(ast: Ast):
    for node_w in ast.iter(AstIterPostorder):
        match node_w.n:
            case AstBinOpNode():
                if isinstance(node_w.n.lhs, AstLiteralNode) and isinstance(node_w.n.rhs, AstLiteralNode):
                    print("binop")
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
                            result = node_w.n.lhs.value << node_w.n.rhs.value
                        case "&":
                            result = node_w.n.lhs.value & node_w.n.rhs.value
                        case "|":
                            result = node_w.n.lhs.value | node_w.n.rhs.value
                        case "^":
                            result = node_w.n.lhs.value ^ node_w.n.rhs.value

                    node_w.n = AstLiteralNode(result)

            case AstUnOpNode():
                if isinstance(node_w.n.operand, AstLiteralNode):
                    print("unop")
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

                    node_w.n = AstLiteralNode(result)
