from llvmlite import ir, binding
from src.parser.visitor.CFG_visitor.cfg_visitor import *
from .mapping import *
from src.parser.visitor.AST_visitor.type_checker_visitor import *
from ..parser.CFG.node.basic_block import BasicBlock

'''This visitor assumes that the AST/CFG is in TAC form'''
class LLVMVisitor(CFGVisitor):

    def _create_reg(self) -> str:
        result: str = str(self.reg_counter)
        self.reg_counter += 1
        return result

    def __init__(self, cfg: ControlFlowGraph, name: str):
        self.cfg = cfg
        self.no_load: bool = False
        self.regs: dict[str, ir.Instruction] = {}
        self.refs: set[str] = set()

        self.jump_stack: list[tuple[ir.Block | None, ir.Block | None]] = []# stack for jump statements with tuple = (continue block, break block)

        self.module: ir.Module = ir.Module(name=name)
        self.reg_counter: int = 0
        self.module.triple = binding.get_default_triple()

        printf_type = ir.FunctionType(ir.IntType(32), [ir.IntType(8).as_pointer()], var_arg=True)
        self.printf = ir.Function(self.module, printf_type, name="printf")

        void_type = ir.VoidType()
        fnty = ir.FunctionType(void_type, ())
        func = ir.Function(self.module, fnty, name="main")
        entry = func.append_basic_block(self._create_reg())
        self.builder: ir.IRBuilder = ir.IRBuilder(entry)
        # We're only visiting from the first basic block since we should be able to reach others from there
        self.visit(cfg.basic_blocks[0])
        self.builder.ret_void()


    def _load_if_pointer(self, value: ir.Instruction):
        if value.type.is_pointer:
            return self.builder.load(value, self._create_reg(), 4)
        return value

    def visit(self, node_w: Wrapper[AbstractNode]):
        '''if isinstance(node_w.n, Basic):
            comments = node_w.n.comments + ([node_w.n.source_code_line] if node_w.n.source_code_line is not None else [])
            for comment in comments:
                for subcomment in comment.split("\n"):
                    self.builder.comment(subcomment)'''
        return super().visit(node_w)


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

    def basic_block(self, node_w: Wrapper[BasicBlock]):
        for i in range(0, len(node_w.n.ast_items)-1):
            self.visit(node_w.n.ast_items[i])
        return self.visit(node_w.n.ast_items[-1])

    def jump(self, node_w: Wrapper[JumpStatement]):
        match node_w.n.label:
            case "continue":
                return self.builder.branch(self.jump_stack[-1][0])
            case "break":
                return self.builder.branch(self.jump_stack[-1][1])
            case _:
                raise ValueError("Unrecognized jump statement")

    def conditional(self, node_w: Wrapper[ConditionalStatement]):
        condition_w: Wrapper[Expression] = node_w.n.condition_w
        true_branch_w: Wrapper[CompoundStatement] = node_w.n.true_branch_w
        if node_w.n.false_branch_w is not None:  # if
            with self.builder.if_else(self.builder.trunc(self.visit(condition_w), ir.IntType(1))) as (then, otherwise):
                with then:
                    self.visit(true_branch_w)
                with otherwise:
                    self.visit(node_w.n.false_branch_w)
        else:  # if else
            with self.builder.if_then(self.builder.trunc(self.visit(condition_w), ir.IntType(1))):
                self.visit(true_branch_w)

    def switch(self, node_w: Wrapper[SwitchStatement]):
        end_block = self.builder.append_basic_block("switch.end")
        default_block = self.builder.append_basic_block("default") if node_w.n.default_index is not None else end_block
        self.jump_stack.append((None, end_block))
        switch = self.builder.switch(self.visit(node_w.n.value_w), default_block)
        case_blocks = []
        for case_w in node_w.n.conditions:
            case_block = self.builder.append_basic_block("case")
            case_blocks.append(case_block)
            switch.add_case(self.visit(case_w), case_block)
        if node_w.n.default_index is not None:
            case_blocks.insert(node_w.n.default_index, default_block)
        for i, case_block in enumerate(case_blocks):
            with self.builder.goto_block(case_block):
                self.visit(node_w.n.branches[i])
                if not case_block.is_terminated:
                    next_block = end_block if i == len(case_blocks)-1 else case_blocks[i+1]
                    self.builder.branch(next_block)
        self.builder.position_at_end(end_block)
        self.jump_stack.pop()


    def iteration(self, node_w: Wrapper[IterationStatement]):
        conditional_block = self.builder.append_basic_block("condition")
        self.builder.branch(conditional_block)
        continue_block = conditional_block
        if node_w.n.adv_w is not None:
            advancement_block = self.builder.append_basic_block("advancement")
            continue_block = advancement_block
            with self.builder.goto_block(advancement_block):
                self.visit(node_w.n.adv_w)
                self.builder.branch(conditional_block)
        body_block = self.builder.append_basic_block("loop.body")
        false_block = self.builder.append_basic_block("end.loop")
        self.jump_stack.append((continue_block, false_block))
        with self.builder.goto_block(body_block):
            self.visit(node_w.n.body_w)
            if not self.builder.block.is_terminated:
                self.builder.branch(continue_block)
        with self.builder.goto_block(conditional_block):
            self.builder.cbranch(self.builder.trunc(self.visit(node_w.n.condition_w),ir.IntType(1)), body_block, false_block)
        self.builder.position_at_end(false_block)
        self.jump_stack.pop()


    # probably here until proper function calls get implemented
    def print(self, node_w: Wrapper[PrintStatement]):
        format_string = ir.GlobalVariable(self.module, ir.ArrayType(ir.IntType(8), len(node_w.n.format) + 1),
                                          self._create_reg())
        format_string.global_constant = True
        format_string.initializer = ir.Constant(ir.ArrayType(ir.IntType(8), len(node_w.n.format) + 1),
                                                [ir.IntType(8)(ord(c)) for c in f"{node_w.n.format}\00"])

        # Get a pointer to the first element of the array
        format_string_ptr = self.builder.gep(format_string,
                                             [ir.Constant(ir.IntType(64), 0), ir.Constant(ir.IntType(64), 0)])
        argument = self.visit(node_w.n.argument_w)
        if isinstance(argument.type, ir.FloatType):
            argument = self.builder.fpext(argument, ir.DoubleType(), self._create_reg())
        return self.builder.call(self.printf, [format_string_ptr, argument])

    def lit(self, node_w: Wrapper[Literal]) -> ir.Constant:
        return self._get_type(node_w.n.type)[0](node_w.n.value)

    def identifier(self, node_w: Wrapper[Identifier]) -> ir.Instruction:
        return self._load_if_pointer(self.regs[node_w.n.name]) if not (self.no_load or node_w.n.name in self.refs) else self.regs[node_w.n.name]

    def _cast(self, value, from_type: PrimitiveType, to_type: PrimitiveType):
        result = do_cast(self.builder, from_type, to_type)
        return result(value, self._get_type(to_type)[0], self._create_reg()) if result is not None else value

    def _get_bin_op_func(self, lhs_value, lhs_type, rhs_value, rhs_type, operator) -> Callable:
        coerced_type: PrimitiveType = TypeCheckerVisitor.typeCoercion([lhs_type.type, rhs_type.type], True)
        lhs_is_pointer: bool = lhs_type.ptr_count > 0
        rhs_is_pointer: bool = rhs_type.ptr_count > 0
        if lhs_type != rhs_type and not (lhs_is_pointer ^ rhs_is_pointer):

            cast_choice = ((not lhs_is_pointer and rhs_is_pointer)
                           or (rhs_type.type == coerced_type.type and rhs_is_pointer)
                           or (rhs_type.type == coerced_type.type and not lhs_is_pointer))
            if cast_choice:
                lhs_value = self._cast(lhs_value, lhs_type, rhs_type)
            else:
                rhs_value = self._cast(rhs_value, rhs_type, lhs_type)
        return get_binary_op(lhs_value, rhs_value, operator, self.builder, self._create_reg)

    def bin_op(self, node_w: Wrapper[BinaryOp]):
        return self._get_bin_op_func(self.visit(node_w.n.lhs_w), node_w.n.lhs_w.n.type,
                                self.visit(node_w.n.rhs_w), node_w.n.rhs_w.n.type,
                                node_w.n.operator)()

    def addressof_op(self, node_w: Wrapper[AddressOfOp]):
        self.no_load = True
        result = self.visit(node_w.n.operand_w)
        self.no_load = False
        return result
    def deref_op(self, node_w: Wrapper[DerefOp]):
        result = self._load_if_pointer(self.visit(node_w.n.operand_w))
        return result

    def cast_op(self, node_w: Wrapper[CastOp]):
        return self._cast(self.visit(node_w.n.expression_w), node_w.n.expression_w.n.type, node_w.n.target_type)

    def un_op(self, node_w: Wrapper[UnaryOp]):
        self.no_load = node_w.n.operator in ["++", "--"]
        operand = self.visit(node_w.n.operand_w)
        self.no_load = False if node_w.n.operator in ["++", "--"] else self.no_load
        operand_value = operand
        match node_w.n.operator:
            case "+":
                return self.builder.add(operand_value.type(0), operand_value, self._create_reg())
            case "-":
                return self.builder.sub(operand_value.type(0), operand_value, self._create_reg())
            case "!":
                return self._get_bin_op_func(operand_value, node_w.n.operand_w.n.type, ir.Constant(ir.IntType(1), 0),  PrimitiveType('int', True), '==')()
            case "~":
                return self.builder.not_(operand_value, self._create_reg())
            case "++":
                loaded_operand = self._load_if_pointer(operand_value)
                increment = self._get_bin_op_func(loaded_operand, node_w.n.operand_w.n.type,
                                         ir.Constant(ir.IntType(32), 1),
                                         PrimitiveType("int", True), "+")()
                self.builder.store(increment, operand_value, self._get_type(node_w.n.operand_w.n.type)[1])
                if not node_w.n.is_postfix:
                    return increment
                return loaded_operand
            case "--":
                loaded_operand = self._load_if_pointer(operand_value)
                decrement = self._get_bin_op_func(loaded_operand, node_w.n.operand_w.n.type,
                                          ir.Constant(ir.IntType(32), 1),
                                          PrimitiveType("int", True), "-")()
                self.builder.store(decrement, operand_value, self._get_type(node_w.n.operand_w.n.type)[1])
                if not node_w.n.is_postfix:
                    return decrement
                return loaded_operand
            case _:
                raise ValueError(f"Unrecognized unary operator")

    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        decl_ir_type = self._get_type(node_w.n.type)
        if node_w.n.definition_w.n is not None:
            if isinstance(node_w.n.definition_w.n, DerefOp):
                self.no_load = True
            self.regs[node_w.n.identifier] = self.visit(node_w.n.definition_w)
            if isinstance(node_w.n.definition_w.n, AddressOfOp):
                self.refs.add(node_w.n.identifier)
            self.no_load = False
        else:
            allocaInstr = self.builder.alloca(decl_ir_type[0], decl_ir_type[1], node_w.n.identifier)
            self.regs[node_w.n.identifier] = allocaInstr

    def assign(self, node_w: Wrapper[Assignment]):
        self.no_load = True
        assignee = self.visit(node_w.n.assignee_w)
        self.no_load = False

        value = self.visit(node_w.n.value_w)
        if node_w.n.type.type != node_w.n.value_w.n.type.type:
            value = self._cast(self._load_if_pointer(value), node_w.n.value_w.n.type, node_w.n.type)
        self.builder.store(value, assignee, self._get_type(node_w.n.type)[1])



