from llvmlite import binding
from src.compilation.visitor.CFG_visitor.cfg_visitor import *
from .mapping import *
from src.constructs import *
from src.compilation.semantic_analyzer.type_checker import *

'''This visitor assumes that the AST/CFG is in TAC form'''


class LLVMVisitor(CFGVisitor):
    @property
    def regs(self) -> dict[str, ir.Instruction]:
        return self.regs_stack[-1]

    @property
    def reg_counter(self):
        return self.reg_counters[-1]

    @reg_counter.setter
    def reg_counter(self, value: int):
        self.reg_counters[-1] = value

    def _create_reg(self) -> str:
        result: str = str(self.reg_counter)
        self.reg_counter += 1
        return result
    def _create_global_reg(self) -> str:
        result: str = str(self.reg_counters[0])
        self.reg_counters[0] += 1
        return result

    def push_regs_stack(self):
        self.regs_stack.append({})

    def __init__(self, ast: Ast, name: str, disable_comments: bool = False):
        self.disable_comments: bool = disable_comments
        self.no_load: bool = False
        self.regs_stack: list[dict[str, ir.Instruction | ir.Function]] = [{}]
        self.reg_counters: list[int] = [0]
        self.refs: set[str] = set()

        self.jump_stack: list[tuple[
            ir.Block | None, ir.Block | None]] = []  # stack for jump statements with tuple = (continue block, break block)

        self.module: ir.Module = ir.Module(name=name)
        self.module.triple = binding.get_default_triple()

        printf_type = ir.FunctionType(ir.IntType(32), [ir.IntType(8).as_pointer()], var_arg=True)
        self.printf = ir.Function(self.module, printf_type, name="printf")

        self.builder = None
        self.visit(ast.root_w)

    def _load_if_pointer(self, value: ir.Instruction):
        if value.type.is_pointer:
            return self.builder.load(value, self._create_reg(), 4)
        return value

    def visit(self, node_w: Wrapper[AbstractNode]):
        if not self.disable_comments and self.builder is not None and isinstance(node_w.n, Basic):
            comments = node_w.n.comments + ([node_w.n.source_code_line] if node_w.n.source_code_line is not None else [])
            for comment in comments:
                for subcomment in comment.split("\n"):
                    self.builder.comment(subcomment)
        return super().visit(node_w)

    def _get_llvm_type(self, type: PrimitiveType) -> tuple[ir.Type, int]:
        result: list[ir.Type, int] = [None, 0]
        if isinstance(type, ArrayType):
            for i, dim in enumerate(reversed(type.dimension)):
                if i == 0:
                    elem_type = self._get_llvm_type(type.element_type)
                    result[1] = dim * elem_type[1]
                    result[0] = ir.ArrayType(elem_type[0], dim)
                else:
                    result[0] = ir.ArrayType(result[0], dim)
                    result[1] *= dim
        else:
            match type.type:
                case "int":
                    result = [ir.IntType(32), 4]
                case "char":
                    result = [ir.IntType(8), 4]
                case "float":
                    result = [ir.FloatType(), 4]
                case "void":
                    result = [ir.VoidType(), 0]
                case _:
                    raise ValueError(f"Critical Error: unrecognized type")
            for ptr in range(0, type.ptr_count):
                result[0] = ir.PointerType(result[0])
                result[1] = 8
        return result[0], result[1]
    def _get_type(self, type: ir.Type) -> PrimitiveType:
        match type:
            case ir.IntType():
                return PrimitiveType("char" if type.get_abi_size(type) == 1 else "int")
            case ir.FloatType():
                return PrimitiveType("float")
            case ir.PointerType():
                ptr_count: int = 0
                while type.is_pointer:
                    type = type.pointee
                    ptr_count += 1
                return PrimitiveType(self._get_type(type).type, False, ptr_count)
            case _:
                raise ValueError(f"Unrecognized LLVM type")


    def func_call(self, node_w: Wrapper[FunctionCall]):
        args = [self.visit(arg) for arg in node_w.n.arguments]
        func = self.regs_stack[0][node_w.n.func_name]
        params = node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.func_name).type.parameter_types
        for i in range(0, len(node_w.n.arguments)):
            if not self.types_compatible(node_w.n.arguments[i].n.type, params[i]):
                args[i] = self._cast(self._load_if_pointer(args[i]), node_w.n.arguments[i].n.type, params[i])
        return self.builder.call(func, args, node_w.n.func_name)

    def func_decl(self, node_w: Wrapper[FunctionDeclaration]):
        param_types = [self._get_llvm_type(param)[0] for param in node_w.n.type.parameter_types]
        fnty = ir.FunctionType(self._get_llvm_type(node_w.n.type.return_type)[0], param_types)
        func = ir.Function(self.module, fnty, name=node_w.n.name)
        self.regs[node_w.n.name] = func
        self.regs_stack.append({})
        self.reg_counters.append(0)
        self.builder: ir.IRBuilder = ir.IRBuilder(func.append_basic_block("entry"))
        for i, param_w in enumerate(node_w.n.parameters):
            alloced = self.visit(param_w)
            self.builder.store(func.args[i], alloced)
        self.visit(node_w.n.body_w)
        if not self.builder.block.is_terminated and isinstance(fnty.return_type, ir.VoidType):
            self.builder.ret_void()
        self.regs_stack.pop()
        self.reg_counters.pop()
        return func

    def basic_block(self, node_w: Wrapper[BasicBlock]):
        for i in range(0, len(node_w.n.ast_items) - 1):
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
                    next_block = end_block if i == len(case_blocks) - 1 else case_blocks[i + 1]
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
            self.builder.cbranch(self.builder.trunc(self.visit(node_w.n.condition_w), ir.IntType(1)), body_block,
                                 false_block)
        self.builder.position_at_end(false_block)
        self.jump_stack.pop()

    # probably here until proper function calls get implemented
    def print(self, node_w: Wrapper[PrintStatement]):
        format_string = ir.GlobalVariable(self.module, ir.ArrayType(ir.IntType(8), len(node_w.n.format) + 1),
                                          self._create_global_reg())
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

    def array_lit(self, node_w: Wrapper[ArrayLiteral]):
        return self._get_llvm_type(node_w.n.type)[0]([self.visit(value_w) for value_w in node_w.n.value])
    def lit(self, node_w: Wrapper[Literal]) -> ir.Constant:
        return self._get_llvm_type(node_w.n.type)[0](node_w.n.value)

    def identifier(self, node_w: Wrapper[Identifier]) -> ir.Instruction:
        return self._load_if_pointer(self.regs[node_w.n.name]) if not (self.no_load or node_w.n.name in self.refs) else \
        self.regs[node_w.n.name]

    def _cast(self, value, from_type: PrimitiveType, to_type: PrimitiveType):
        result = do_cast(self.builder, from_type, to_type)
        return result(value, self._get_llvm_type(to_type)[0], self._create_reg()) if result is not None else value
    def types_compatible(self, l_type: PrimitiveType, r_type: PrimitiveType) -> bool:
        return l_type.type == r_type.type and l_type.ptr_count == r_type.ptr_count

    def _get_bin_op_func(self, lhs_value, lhs_type, rhs_value, rhs_type, operator) -> Callable:
        coerced_type: PrimitiveType = PrimitiveType.typeCoercion([lhs_type.type, rhs_type.type], True)
        lhs_is_pointer: bool = lhs_type.ptr_count > 0
        rhs_is_pointer: bool = rhs_type.ptr_count > 0
        if (lhs_type.type != coerced_type.type or rhs_type.type != coerced_type.type) and not (
                lhs_is_pointer ^ rhs_is_pointer):
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

    def array_access(self, node_w: Wrapper[ArrayAccess]):
        indices = [wrap(IntLiteral(0))]+node_w.n.indices
        current_index = self.builder.gep(self.regs[node_w.n.identifier_w.n.name], [self.visit(index_w) for index_w in indices], True, self._create_reg())
        return self._load_if_pointer(current_index) if not self.no_load else current_index
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
                return self._get_bin_op_func(operand_value, node_w.n.operand_w.n.type, ir.Constant(ir.IntType(1), 0),
                                             PrimitiveType('int', True), '==')()
            case "~":
                return self.builder.not_(operand_value, self._create_reg())
            case "++":
                loaded_operand = self._load_if_pointer(operand_value)
                increment = self._get_bin_op_func(loaded_operand, node_w.n.operand_w.n.type,
                                                  ir.Constant(ir.IntType(32), 1),
                                                  PrimitiveType("int", True), "+")()
                self.builder.store(increment, operand_value, self._get_llvm_type(node_w.n.operand_w.n.type)[1])
                if not node_w.n.is_postfix:
                    return increment
                return loaded_operand
            case "--":
                loaded_operand = self._load_if_pointer(operand_value)
                decrement = self._get_bin_op_func(loaded_operand, node_w.n.operand_w.n.type,
                                                  ir.Constant(ir.IntType(32), 1),
                                                  PrimitiveType("int", True), "-")()
                self.builder.store(decrement, operand_value, self._get_llvm_type(node_w.n.operand_w.n.type)[1])
                if not node_w.n.is_postfix:
                    return decrement
                return loaded_operand
            case _:
                raise ValueError(f"Unrecognized unary operator")

    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        if node_w.n.local_symtab_w.n.has_parent():
            decl_ir_type = self._get_llvm_type(node_w.n.type)
            if node_w.n.definition_w.n is not None:
                if isinstance(node_w.n.definition_w.n, DerefOp):
                    self.no_load = True
                self.regs[node_w.n.identifier] = self.visit(node_w.n.definition_w)
                if isinstance(node_w.n.definition_w.n, AddressOfOp):
                    self.refs.add(node_w.n.identifier)
                self.no_load = False
                return self.regs[node_w.n.identifier]
            else:
                allocaInstr = self.builder.alloca(decl_ir_type[0], decl_ir_type[1], node_w.n.identifier)
                self.regs[node_w.n.identifier] = allocaInstr
                return allocaInstr

        else:
            type = self._get_llvm_type(node_w.n.type)
            result = ir.GlobalVariable(self.module, type[0], node_w.n.identifier)
            if node_w.n.definition_w.n is not None:
                self.regs[node_w.n.identifier] = self.visit(node_w.n.definition_w)
                result.initializer = self.regs[node_w.n.identifier]
            return result

    def assign(self, node_w: Wrapper[Assignment]):
        self.no_load = True
        assignee = self.visit(node_w.n.assignee_w)
        self.no_load = False

        value = self.visit(node_w.n.value_w)
        if not self.types_compatible(node_w.n.type, node_w.n.value_w.n.type):
            value = self._cast(self._load_if_pointer(value), node_w.n.value_w.n.type, node_w.n.type)
        self.builder.store(value, assignee, self._get_llvm_type(node_w.n.type)[1])

    def return_stmt(self, node_w: Wrapper[ReturnStatement]):
        if node_w.n.expr_w is None:
            return self.builder.ret_void()
        returned_value = self.visit(node_w.n.expr_w)
        return_type = node_w.n.local_symtab_w.n.get_enclosing_function_type().return_type
        if not self.types_compatible(node_w.n.type, return_type):
            returned_value = self._cast(self._load_if_pointer(returned_value), node_w.n.type, return_type)
        return self.builder.ret(returned_value)
