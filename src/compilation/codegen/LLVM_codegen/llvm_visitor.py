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

    def _get_reg(self, key: str) -> ir.Instruction:
        result = self.regs.get(key, None)
        if result is None:
            # check if its global
            result = self.regs_stack[0][key]
        return result

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

    def __init__(self, ast: Ast, name: str, disable_comments: bool = False, included_stdio: bool = False):
        self.disable_comments: bool = disable_comments
        self.no_load: bool = False
        self.regs_stack: list[dict[str, ir.Instruction | ir.Function | ir.GlobalVariable]] = [{}]
        self.reg_counters: list[int] = [0]
        self.refs: set[str] = set()
        self.jump_stack: list[tuple[
            ir.Block | None, ir.Block | None]] = []  # stack for jump statements with tuple = (continue block, break block)

        self.module: ir.Module = ir.Module(name=name)
        self.module.triple = binding.get_default_triple()
        self.module.context = ir.Context()

        self.io_functions: dict[str, ir.Function] = {}

        io_type = ir.FunctionType(ir.IntType(32), [ir.IntType(8).as_pointer()], var_arg=True)
        if included_stdio:
            self.io_functions["printf"] = ir.Function(self.module, io_type, name="printf")
            self.io_functions["scanf"] = ir.Function(self.module, io_type, name="scanf")
        self.builder: ir.IRBuilder = ir.IRBuilder()

        self.visit(ast.root_w)


    def _load_if_pointer(self, value: ir.Instruction):
        if value.type.is_pointer:
            if isinstance(value.type.pointee, ir.ArrayType):
                result =  self.builder.gep(value, [ir.Constant(ir.IntType(64), 0), ir.Constant(ir.IntType(64), 0)], self._create_reg())
                return result
            return self.builder.load(value, self._create_reg(), 4)
        return value

    def _get_llvm_type_size(self, type: ir.Type):
        match type:
            case ir.PointerType():
                return 64
            case ir.ArrayType():
                return type.count * self._get_llvm_type_size(type.element)
            case ir.BaseStructType():
                return sum([self._get_llvm_type_size(element) for element in type.elements])
            case _:
                return type.width


    def visit(self, node_w: Wrapper[AbstractNode]):
        if not self.disable_comments and self.builder.block is not None:
            comments = node_w.n.comments + ([node_w.n.source_code_line] if node_w.n.source_code_line is not None else [])
            for comment in comments:
                for subcomment in comment.split("\n"):
                    self.builder.comment(subcomment)
        return super().visit(node_w)

    def _get_llvm_type(self, type: PrimitiveType | CompositeType) -> tuple[ir.Type, int]:
        result: list[ir.Type, int] = [None, 0]
        if isinstance(type, ArrayType):
            for i, dim in enumerate(reversed(type.dimension)):
                if i == 0:
                    elem_type = self._get_llvm_type(type.element_type)
                    result[1] = elem_type[1]
                    result[0] = ir.ArrayType(elem_type[0], dim)
                else:
                    result[0] = ir.ArrayType(result[0], dim)
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
                case "struct":
                    result = [self._get_reg(type.name), 4]
                case "union":
                    result = [self._get_reg(type.name), 4]
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

    def string_lit(self, node_w: Wrapper[StringLiteral]):
        str_value = (node_w.n.string+"\00").encode("utf8").decode("unicode_escape")
        str = ir.Constant(ir.ArrayType(ir.IntType(8), len(str_value)),
                    bytearray(str_value.encode("utf8")))
        var = ir.GlobalVariable(self.module, str.type, self._create_global_reg())
        var.initializer = str
        var.linkage = 'private'
        var.align = 1
        return var.gep([ir.Constant(ir.IntType(64),0)]*2)

    def func_call(self, node_w: Wrapper[FunctionCall]):
        args = [self.visit(arg) for arg in node_w.n.arguments]
        func = self.regs_stack[0][node_w.n.func_name]
        params = node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.func_name).type.parameter_types
        for i in range(0, len(node_w.n.arguments)):
            if not self.types_compatible(node_w.n.arguments[i].n.type, params[i]):
                args[i] = self._cast(self._load_if_pointer(args[i]), node_w.n.arguments[i].n.type, params[i])
        return self.builder.call(func, args, node_w.n.func_name)
    def add_func_attrs(self, func: ir.Function):
        func.linkage = "dso_local"
        func.attributes.add('noinline')
        func.attributes.add('nounwind')
        func.attributes.add('optnone')
        func.attributes.add('uwtable')

    def func_decl(self, node_w: Wrapper[FunctionDeclaration]):
        param_types = [self._get_llvm_type(param)[0] for param in node_w.n.type.parameter_types]
        fnty = ir.FunctionType(self._get_llvm_type(node_w.n.type.return_type)[0], param_types)
        func = ir.Function(self.module, fnty, name=node_w.n.name)
        self.add_func_attrs(func)
        self.regs[node_w.n.name] = func
        self.regs_stack.append({})
        self.reg_counters.append(0)
        self.builder: ir.IRBuilder = ir.IRBuilder(func.append_basic_block("entry"))
        for i, param_w in enumerate(node_w.n.parameters):
            alloced = self.visit(param_w)
            self.builder.store(func.args[i], alloced)
        self.visit(node_w.n.body_w)
        if not self.builder.block.is_terminated:
            if isinstance(fnty.return_type, ir.VoidType):
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
        branch_block = self.builder.block
        if node_w.n.false_branch_w:
            both_return: bool = False
            with self.builder.if_else(self.builder.trunc(self.visit(condition_w), ir.IntType(1))) as (then, otherwise):
                with then:
                    self.visit(true_branch_w)
                    both_return = isinstance(self.builder.block.instructions[-1], ir.Ret)
                with otherwise:
                    self.visit(node_w.n.false_branch_w)
                    both_return = both_return and isinstance(self.builder.block.instructions[-1], ir.Ret)
            if both_return:
                self.builder.function.basic_blocks.remove(self.builder.block)
        else:  # if else
            with self.builder.if_then(self.builder.trunc(self.visit(condition_w), ir.IntType(1))):
                self.visit(true_branch_w)
        return branch_block.instructions[-1]


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
        return switch

    def iteration(self, node_w: Wrapper[IterationStatement]):
        conditional_block = self.builder.append_basic_block("condition")
        br = self.builder.branch(conditional_block)
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
        return br

    def io(self, node_w: Wrapper[IOStatement]):
        # Get a pointer to the first element of the array
        arguments = [self.visit(argument_w) for argument_w in node_w.n.arguments]
        for i, argument in enumerate(arguments):
            if isinstance(argument.type, ir.FloatType):
                arguments[i] = self.builder.fpext(argument, ir.DoubleType(), self._create_reg())
        return self.builder.call(self.io_functions[node_w.n.name], [self.visit(node_w.n.contents_w)]+arguments)

    def array_lit(self, node_w: Wrapper[ArrayLiteral]):
        return self._get_llvm_type(node_w.n.type)[0]([self.visit(value_w) for value_w in node_w.n.value])
    def lit(self, node_w: Wrapper[Literal]) -> ir.Constant:
        return self._get_llvm_type(node_w.n.type)[0](node_w.n.value)

    def identifier(self, node_w: Wrapper[Identifier]) -> ir.Instruction:
        if not (self.no_load or node_w.n.name in self.refs):
            result = self._load_if_pointer(self._get_reg(node_w.n.name))
            return result
        return self._get_reg(node_w.n.name)

    def _in_place_cast(self, value, from_type: PrimitiveType, to_type: PrimitiveType):
        result = do_cast(value, from_type, to_type)
        return result(self._get_llvm_type(to_type)[0]) if result is not None else value

    def _cast(self, value, from_type: PrimitiveType, to_type: PrimitiveType):
        result = do_cast(self.builder, from_type, to_type)
        return result(value, self._get_llvm_type(to_type)[0], self._create_reg()) if result is not None else value
    def types_compatible(self, l_type: PrimitiveType, r_type: PrimitiveType) -> bool:
        return l_type.type == r_type.type and l_type.ptr_count == r_type.ptr_count

    def _get_bin_op_func(self, lhs_value, lhs_type, rhs_value, rhs_type, operator) -> Callable:
        coerced_type: PrimitiveType = PrimitiveType.typeCoercion([lhs_type, rhs_type], True)
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
        no_load = self.no_load
        self.no_load = True
        result = self.visit(node_w.n.operand_w)
        self.no_load = no_load
        return result

    def deref_op(self, node_w: Wrapper[DerefOp]):
        result = self._load_if_pointer(self.visit(node_w.n.operand_w))
        return result

    def cast_op(self, node_w: Wrapper[CastOp]):
        return self._cast(self.visit(node_w.n.expression_w), node_w.n.expression_w.n.type, node_w.n.target_type)

    def array_access(self, node_w: Wrapper[ArrayAccess]):
        indices = [self.visit(wrap(IntLiteral(0))), self._load_if_pointer(self.visit(node_w.n.index_w))]
        no_load = self.no_load
        self.no_load = True
        accessed = self.visit(node_w.n.accessed_w)
        current_index: ir.GEPInstr = self.builder.gep(accessed, indices, True, self._create_reg())
        self.no_load = no_load
        result = self._load_if_pointer(current_index) if not self.no_load else current_index
        return result
    def un_op(self, node_w: Wrapper[UnaryOp]):
        no_load = self.no_load
        self.no_load = node_w.n.operator in ["++", "--"]
        operand = self.visit(node_w.n.operand_w)
        self.no_load = no_load if node_w.n.operator in ["++", "--"] else self.no_load
        operand_value = operand
        match node_w.n.operator:
            case "+":
                return operand
            case "-":
                return self._get_bin_op_func(ir.Constant(ir.IntType(32), 0), PrimitiveType("int", True),
                                             operand_value, node_w.n.operand_w.n.type, "-")()
            case "!":
                return self._get_bin_op_func(operand_value, node_w.n.operand_w.n.type, ir.Constant(ir.IntType(1), 0),
                                             PrimitiveType('int', True), '==')()
            case "~":
                return self.builder.not_(operand_value, self._create_reg())
            case "++":
                loaded_operand = self._load_if_pointer(operand_value)
                int_type =  PrimitiveType("int", True)
                increment = self._get_bin_op_func(loaded_operand, node_w.n.operand_w.n.type,
                                                  ir.Constant(ir.IntType(32), 1),
                                                  int_type, "+")()
                if not self.types_compatible(node_w.n.type, int_type):
                    increment = self._cast(increment, int_type, node_w.n.operand_w.n.type)
                self.builder.store(increment, operand_value, self._get_llvm_type(node_w.n.operand_w.n.type)[1])
                if not node_w.n.is_postfix:
                    return increment
                return loaded_operand
            case "--":
                loaded_operand = self._load_if_pointer(operand_value)
                int_type =  PrimitiveType("int", True)
                decrement = self._get_bin_op_func(loaded_operand, node_w.n.operand_w.n.type,
                                                  ir.Constant(ir.IntType(32), 1),
                                                  int_type, "-")()
                if not self.types_compatible(node_w.n.type, int_type):
                    decrement = self._cast(decrement, int_type, node_w.n.operand_w.n.type)
                self.builder.store(decrement, operand_value, self._get_llvm_type(node_w.n.operand_w.n.type)[1])
                if not node_w.n.is_postfix:
                    return decrement
                return loaded_operand
            case _:
                raise ValueError(f"Unrecognized unary operator")
    def composite_decl(self, node_w: Wrapper[CompositeDeclaration]):
        context = self.module.context
        result = context.get_identified_type(node_w.n.identifier)
        self.regs[node_w.n.identifier] = result
        member_types = [self._get_llvm_type(member_w.n.type)[0] for member_w in node_w.n.definition_w.n.statements]
        if node_w.n.type.type == "union":
            sizes = [self._get_llvm_type_size(member_type) for member_type in member_types]
            if len(sizes):
                index = sizes.index(max(sizes))
                member_types = [member_types[index]]
        result.set_body(*member_types)
        return result

    def object_access(self, node_w: Wrapper[ObjectAccess]):
        no_load: bool = self.no_load
        self.no_load = True
        obj = self.visit(node_w.n.object_w)
        self.no_load = no_load
        if node_w.n.object_w.n.type.type == "struct":
            object_type: CompositeType = node_w.n.object_w.n.type
            composite_def: CompoundStatement = node_w.n.local_symtab_w.n.lookup_symbol(object_type.name).definition_w.n
            member_name: str = node_w.n.member_w.n.name
            for i, member_w in enumerate(composite_def.statements):
                if member_w.n.identifier == member_name:
                    obj = self.builder.gep(obj,
                                     [ir.Constant(ir.IntType(32), 0),
                                      ir.Constant(ir.IntType(32), i)],
                                     True,
                                     self._create_reg())
        else:
            obj = self.builder.bitcast(obj, self._get_llvm_type(node_w.n.member_w.n.type)[0].as_pointer(), self._create_reg())
        result = obj if no_load else self._load_if_pointer(obj)
        return result


    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        if node_w.n.storage_class_specifier != "typedef":
            no_load = self.no_load
            if node_w.n.local_symtab_w.n.has_parent():
                decl_ir_type = self._get_llvm_type(node_w.n.type)
                if node_w.n.definition_w.n is not None:
                    if isinstance(node_w.n.definition_w.n, (DerefOp, ObjectAccess)):
                        self.no_load = True
                    self.regs[node_w.n.identifier] = self.visit(node_w.n.definition_w)
                    if isinstance(node_w.n.definition_w.n, AddressOfOp):
                        self.refs.add(node_w.n.identifier)
                    self.no_load = no_load
                    return self._get_reg(node_w.n.identifier)
                else:
                    allocaInstr = self.builder.alloca(decl_ir_type[0], 1, node_w.n.identifier)
                    allocaInstr.align = decl_ir_type[1]
                    self.regs[node_w.n.identifier] = allocaInstr
                    return allocaInstr

            else:
                llvm_type = self._get_llvm_type(node_w.n.type)
                result = ir.GlobalVariable(self.module, llvm_type[0], node_w.n.identifier)
                result.linkage = "dso_local"
                result.align = llvm_type[1]
                if node_w.n.definition_w.n is not None:
                    visited = self.visit(node_w.n.definition_w)
                    if not self.types_compatible(node_w.n.definition_w.n.type, node_w.n.type):
                        visited = self._in_place_cast(self._load_if_pointer(visited), node_w.n.definition_w.n.type, node_w.n.type)
                    result.initializer = visited
                self.regs[node_w.n.identifier] = result
                return result

    def assign(self, node_w: Wrapper[Assignment]):
        no_load = self.no_load
        self.no_load = True
        assignee = self.visit(node_w.n.assignee_w)
        self.no_load = no_load

        value = self.visit(node_w.n.value_w)
        if not self.types_compatible(node_w.n.type, node_w.n.value_w.n.type):
            value = self._cast(self._load_if_pointer(value), node_w.n.value_w.n.type, node_w.n.type)
        self.builder.store(value, assignee, self._get_llvm_type(node_w.n.type)[1])
        return value

    def return_stmt(self, node_w: Wrapper[ReturnStatement]):
        if node_w.n.expr_w is None:
            return self.builder.ret_void()
        returned_value = self.visit(node_w.n.expr_w)
        return_type = node_w.n.local_symtab_w.n.get_enclosing_function_type().return_type
        if not self.types_compatible(node_w.n.type, return_type):
            returned_value = self._cast(self._load_if_pointer(returned_value), node_w.n.type, return_type)
        return self.builder.ret(returned_value)
