from src.compilation.visitor import ASTVisitor
from src.constructs import *
class ConstantFoldingVisitor(ASTVisitor):
    def __init__(self, ast: Ast):
        super().__init__(ast)
    def bin_op(self, node_w: Wrapper[BinaryOp]):
        self.visit(node_w.n.lhs_w)
        self.visit(node_w.n.rhs_w)
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
                    result = bool(node_w.n.lhs.value) and bool(node_w.n.rhs.value)
                case "||":
                    result = bool(node_w.n.lhs.value) or bool(node_w.n.rhs.value)
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
            coerced_type = PrimitiveType.typeCoercion([node_w.n.lhs_w.n.type, node_w.n.rhs_w.n.type], True)
            if isinstance(result, bool):
                node_w.n = IntLiteral(1 if result else 0)
            else:
                match coerced_type.type:
                    case "int":
                        node_w.n = IntLiteral(int(result))
                    case "float":
                        node_w.n = FloatLiteral(float(result))
                    case "char":
                        node_w.n = IntLiteral(int(result))
    def un_op(self, node_w: Wrapper[UnaryOp]):
        self.visit(node_w.n.operand_w)
        if isinstance(node_w.n.operand, Literal) and not node_w.n.is_postfix:
            result = node_w.n
            new_type = node_w.n.operand_w.n.type
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
                    result = int(not node_w.n.operand.value)
                case "~":
                    result = ~node_w.n.operand.value
            literal_type = type(node_w.n.operand)
            node_w.n = literal_type(result)
            node_w.n.type = new_type
    def cast_op(self, node_w: Wrapper[CastOp]):
        self.visit(node_w.n.expression_w)
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
