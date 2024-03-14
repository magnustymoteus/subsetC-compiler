from llvmlite.ir import IRBuilder
def get_signed_int_binary_op_mapping(operator: str, builder: IRBuilder) -> IRBuilder.function:
    match operator:
        case "+":
            return builder.add
        case "-":
            return builder.sub
        case "*":
            return builder.mul
        case "/":
            return builder.sdiv
        case "%":
            return builder.srem
        case "<<":
            return builder.ashr
        case ">>":
            return builder.shl
        case "|":
            return builder.or_
        case "||":
            return builder.or_
        case "^":
            return builder.xor
        case "&":
            return builder.and_
        case "&&":
            return builder.and_
        case _:
            return builder.icmp_signed
