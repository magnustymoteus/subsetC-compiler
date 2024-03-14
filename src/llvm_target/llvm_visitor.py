from llvmlite import ir
from src.parser.visitor.CFG_visitor.cfg_visitor import *
from .mapping import *

'''This visitor assumes that the AST/CFG is in TAC form'''

class LLVMVisitor(CFGVisitor):
    def _create_reg(self) -> str:
        result: str = str(self.reg_counter)
        self.reg_counter += 1
        return result

    def __init__(self, cfg: ControlFlowGraph, name: str):
        self.regs = {}

        self.module: ir.Module = ir.Module(name=name)
        self.reg_counter: int = 0
        void_type = ir.VoidType()
        fnty = ir.FunctionType(void_type, ())
        func = ir.Function(self.module, fnty, name="main")
        block = func.append_basic_block(name="entry")
        self.builder: ir.IRBuilder = ir.IRBuilder(block)
        super().__init__(cfg)
        self.builder.ret_void()

    def visit(self, node_w: Wrapper[CFGNode]):
        match node_w.n:
            case BasicBlockList():
                return self.basic_block_list(node_w)
            case BasicBlock():
                return self.basic_block(node_w)
            case Assignment():
                return self.assign(node_w)
            case BinaryOp():
                return self.bin_op(node_w)
            case DerefOp():
                return self.deref_op(node_w)
            case AddressOfOp():
                return self.addressof_op(node_w)
            case UnaryOp():
                return self.un_op(node_w)
            case CastOp():
                return self.cast_op(node_w)
            case FunctionDefinition():
                return self.func_def(node_w)
            case VariableDeclaration():
                return self.variable_decl(node_w)
            case Literal():
                return self.lit(node_w)
            case Identifier():
                return self.identifier(node_w)
            case _:
                raise Exception

    def _get_type(self, type: PrimitiveType) -> tuple[ir.Type, int]:
        result: list[ir.Type, int] = []
        match type.type:
            case "int":
                result = [ir.IntType(32), 4]
            case "char":
                result = [ir.IntType(8), 4]
            case "float":
                result = [ir.FloatType(), 4]
            case _:
                raise ValueError(f"Critical Error: unrecognized type")
        for ptr in range(0, type.ptr_count):
            result[0] = ir.PointerType(result[0])
            result[1] = 8
        return result[0], result[1]

    def lit(self, node_w: Wrapper[Literal]) -> ir.Constant:
        return self._get_type(node_w.n.type)[0](node_w.n.value)

    def identifier(self, node_w: Wrapper[Identifier]) -> ir.Instruction:
        return self.regs[node_w.n.name]

    def _load_if_pointer(self, value: ir.Instruction):
        if isinstance(value.type, ir.PointerType):
            return self.builder.load(value, self._create_reg())
        return value


    def bin_op(self, node_w: Wrapper[BinaryOp]):
        lhs_value = self._load_if_pointer(self.visit(node_w.n.lhs_w))
        rhs_value = self._load_if_pointer(self.visit(node_w.n.rhs_w))
        match node_w.n.type.type:
            case "int":
                return get_signed_int_binary_op_mapping(node_w.n.operator, self.builder)(lhs_value, rhs_value,
                                                                                         self._create_reg())
            case "float":
                return get_float_binary_op_mapping(node_w.n.operator, self.builder)(lhs_value, rhs_value,
                                                                                    self._create_reg())
            case _:
                raise ValueError(f"Critical Error: unrecognized type")
    def un_op(self, node_w: Wrapper[UnaryOp]):
        operand_value = self._load_if_pointer(self.visit(node_w.n.operand_w))
        match node_w.n.operator:
            case "+":
                return self.builder.add(operand_value.type(0), operand_value, self._create_reg())
            case "-":
                return self.builder.sub(operand_value.type(0), operand_value, self._create_reg())
            case "!":
                return self.builder.not_(operand_value, self._create_reg())
            case "~":
                return self.builder.not_(operand_value, self._create_reg())
            case "++":
                pass
            case "--":
                pass


    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        decl_ir_type = self._get_type(node_w.n.type)
        if node_w.n.definition_w.n is not None:
            self.regs[node_w.n.identifier] = self.visit(node_w.n.definition_w)
        else:
            allocaInstr = self.builder.alloca(decl_ir_type[0], decl_ir_type[1], node_w.n.identifier)
            self.regs[node_w.n.identifier] = allocaInstr

    def assign(self, node_w: Wrapper[Assignment]):
        value = self.visit(node_w.n.value_w)
        assignee = self.visit(node_w.n.assignee_w)
        self.builder.store(value, assignee)



