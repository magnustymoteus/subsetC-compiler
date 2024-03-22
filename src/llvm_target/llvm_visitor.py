from llvmlite import ir
from src.parser.visitor.CFG_visitor.cfg_visitor import *
from .mapping import *
from src.parser.visitor.AST_visitor.type_checker_visitor import *


'''This visitor assumes that the AST/CFG is in TAC form'''
class LLVMVisitor(CFGVisitor):

    def _create_reg(self) -> str:
        result: str = str(self.reg_counter)
        self.reg_counter += 1
        return result


    def __init__(self, cfg: ControlFlowGraph, name: str):
        self.in_lhs_assignment: bool = False
        self.regs = {}
        self.postfix_function = None
        self.module: ir.Module = ir.Module(name=name)
        self.reg_counter: int = 0
        void_type = ir.VoidType()
        fnty = ir.FunctionType(void_type, ())
        func = ir.Function(self.module, fnty, name="main")
        block = func.append_basic_block(name="entry")
        self.builder: ir.IRBuilder = ir.IRBuilder(block)
        super().__init__(cfg)
        self.builder.ret_void()

    def _load_if_pointer(self, value: ir.Instruction):
        if isinstance(value.type, ir.PointerType):
            return self.builder.load(value, self._create_reg(), 4)
        return value

    def _apply_inc_or_dec(self, add_or_sub, operand, operand_value):
        added = add_or_sub(operand_value, operand_value.type(1), self._create_reg())
        self.builder.store(added, operand, 4)

    def visit(self, node_w: Wrapper[AbstractNode]):
        if self.postfix_function is not None:
            self.postfix_function()
            self.postfix_function = None
        if isinstance(node_w.n, Basic):
            for comment in node_w.n.comments:
                for subcomment in comment.split("\n"):
                    self.builder.comment(subcomment)
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
        return self._load_if_pointer(self.regs[node_w.n.name]) if not self.in_lhs_assignment else self.regs[node_w.n.name]

    def _cast(self, value, from_type: PrimitiveType, to_type: PrimitiveType):
        cast_function: IRBuilder.function = get_casts(self.builder)[(from_type.type, to_type.type)]
        return cast_function(value, self._get_type(to_type)[0], self._create_reg())

    def bin_op(self, node_w: Wrapper[BinaryOp]):
        lhs_value = self.visit(node_w.n.lhs_w)
        rhs_value = self.visit(node_w.n.rhs_w)

        lhs_type: PrimitiveType = node_w.n.lhs_w.n.type
        rhs_type: PrimitiveType = node_w.n.rhs_w.n.type

        if lhs_type.type != rhs_type.type:
            coerced_type: PrimitiveType = TypeCheckerVisitor.typeCoercion([lhs_type.type, rhs_type.type], True)
            if lhs_type.type != coerced_type:
                lhs_value = self._cast(self._load_if_pointer(lhs_value), lhs_type, rhs_type)
            else:
                rhs_value = self._cast(self._load_if_pointer(rhs_value), rhs_type, lhs_type)
        return get_binary_op(lhs_value, rhs_value, node_w.n.operator, self.builder, self._create_reg)()

    def addressof_op(self, node_w: Wrapper[AddressOfOp]):
        self.in_lhs_assignment = True
        result = self.visit(node_w.n.operand_w)
        self.in_rhs_assignment = False
        return result
    def deref_op(self, node_w: Wrapper[DerefOp]):
        return self._load_if_pointer(self.visit(node_w.n.operand_w))

    def cast_op(self, node_w: Wrapper[CastOp]):
        pass
        '''match node_w.n.target_type.type:
            case "int":
                self.builder.'''

    def un_op(self, node_w: Wrapper[UnaryOp]):
        operand = self.visit(node_w.n.operand_w)
        operand_value = operand
        match node_w.n.operator:
            case "+":
                return self.builder.add(operand_value.type(0), operand_value, self._create_reg())
            case "-":
                return self.builder.sub(operand_value.type(0), operand_value, self._create_reg())
            case "!":
                return self.builder.not_(operand_value, self._create_reg())
            case "~":
                return self.builder.not_(operand_value, self._create_reg())
            # TODO: prefix, postfix for both non pointers and pointers
            case "++":
                '''if not node_w.n.is_postfix:
                    self._apply_inc_or_dec(self.builder.add, operand, operand_value)
                else:
                    self.postfix_function = lambda : self._apply_inc_or_dec(self.builder.add, operand, operand_value)'''
                return operand_value
            case "--":
                '''if not node_w.n.is_postfix:
                    self._apply_inc_or_dec(self.builder.sub, operand, operand_value)
                else:
                    self.postfix_function = lambda : self._apply_inc_or_dec(self.builder.sub, operand, operand_value)'''
                return operand_value
            case _:
                raise ValueError(f"Unrecognized unary operator")

    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        decl_ir_type = self._get_type(node_w.n.type)
        if node_w.n.definition_w.n is not None:
            self.regs[node_w.n.identifier] = self.visit(node_w.n.definition_w)
        else:
            allocaInstr = self.builder.alloca(decl_ir_type[0], decl_ir_type[1], node_w.n.identifier)
            self.regs[node_w.n.identifier] = allocaInstr

    def assign(self, node_w: Wrapper[Assignment]):
        self.in_lhs_assignment = True
        assignee = self.visit(node_w.n.assignee_w)
        self.in_lhs_assignment = False
        value = self.visit(node_w.n.value_w)
        if node_w.n.type.type != node_w.n.value_w.n.type.type:
            value = self._cast(self._load_if_pointer(value), node_w.n.value_w.n.type, node_w.n.type)
        self.builder.store(value, assignee, self._get_type(node_w.n.type)[1])



