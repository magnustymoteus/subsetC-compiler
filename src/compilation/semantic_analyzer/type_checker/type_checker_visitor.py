from src.compilation.visitor.AST_visitor.ast_visitor import *
from copy import deepcopy

class TypeCheckerVisitor(ASTVisitor):
    """
    The TypeCheckerVisitor class is responsible for performing type checking on the abstract syntax tree (AST).
    It visits each node in the AST and checks the validity of the types used in expressions and assignments.
    """

    def __init__(self, ast: Ast):
        super().__init__(ast)

    @staticmethod
    def is_comparison(operator: str):
        """
        Check if the given operator is a comparison operator.

        Args:
            operator (str): The operator to check.

        Returns:
            bool: True if the operator is a comparison operator, False otherwise.
        """
        return operator in ['<', '>', '>=', '<=', '==', '!=', '&&', '||', '!']


    def checkValidPrimitiveType(self, type: PrimitiveType):
        """
        Check if the given primitive type is valid.

        Args:
            type (PrimitiveType): The primitive type to check.

        Raises:
            SemanticError: If the type is not valid.
        """
        if type.type not in PrimitiveType.type_ranks:
            self.raiseSemanticErr(f"Unknown type {type}")

    def checkImplicitDemotion(self, assignee_type: PrimitiveType, value_type: PrimitiveType):
        """
        Check if there is implicit demotion from the value type to the assignee type.

        Args:
            assignee_type (PrimitiveType): The type of the assignee.
            value_type (PrimitiveType): The type of the value being assigned.

        Raises:
            Warning: If there is implicit demotion.
        """
        if PrimitiveType.type_ranks.index(assignee_type.type) < PrimitiveType.type_ranks.index(value_type.type):
            self.raiseWarning(f"Implicit demotion from {value_type} to {assignee_type} (possible loss of information)")

    def checkDiscardedPointerQualifier(self, assignee_type: PrimitiveType, value_type: PrimitiveType):
        """
        Check if there is a discarded pointer qualifier in the assignment.

        Args:
            assignee_type (PrimitiveType): The type of the assignee.
            value_type (PrimitiveType): The type of the value being assigned.

        Raises:
            Warning: If there is a discarded pointer qualifier.
        """
        if assignee_type.ptr_count > 0 and value_type.ptr_count > 0:
            if (not assignee_type.is_constant and value_type.is_constant):
                self.raiseWarning(f"Assignment of {assignee_type} to {value_type} discards const qualifier")

    def checkAssignee(self, assignee_w: Wrapper):
        """
        Check if the assignee is valid.

        Args:
            assignee_w (Wrapper): The wrapper containing the assignee node.

        Raises:
            SemanticError: If the assignee is not valid.
        """
        is_lvalue = isinstance(assignee_w.n, (Identifier, DerefOp, ArrayAccess))
        if is_lvalue:
            symtype = assignee_w.n.type
            # TODO: with constant pointers?
            if symtype.ptr_count == 0 and symtype.is_constant:
                self.raiseSemanticErr(f"assignment of readonly variable {symtype}")
        else:
            self.raiseSemanticErr("lvalue required as left operand of assignment")

    def checkPointerTypes(self, left_type: PrimitiveType, right_type: PrimitiveType):
        """
        Check if the pointer types are compatible.

        Args:
            left_type (PrimitiveType): The type of the left operand.
            right_type (PrimitiveType): The type of the right operand.

        Raises:
            SemanticError: If the pointer types are not compatible.
        """
        left_copy = deepcopy(left_type)
        right_copy = deepcopy(right_type)
        if left_copy.ptr_count > 0 and right_copy.ptr_count == 0:
            if right_copy.type != 'int':
                # case where a pointer gets assigned to a non integer non pointer
                self.raiseSemanticErr(f"Cannot bind pointer {left_copy} to {right_copy}")
            # case where a pointer gets assigned to a non pointer integer
        elif left_copy.ptr_count != right_copy.ptr_count:
            # case where two pointers dont match
            self.raiseSemanticErr(f"Incompatible pointer types {left_copy} and {right_copy}")
    def checkReturnType(self, return_type: PrimitiveType, returned_type: PrimitiveType):
        self.checkImplicitDemotion(return_type, returned_type)
        self.checkPointerTypes(return_type, returned_type)
        if return_type.type == "void" and returned_type != return_type:
            self.raiseSemanticErr(f"Cannot return type {returned_type} as void")
    def checkArrayInitialization(self, node_w: Wrapper[VariableDeclaration]):
        arr_type: ArrayType = node_w.n.type
        definition_type = node_w.n.definition_w.n.type
        if not isinstance(definition_type, ArrayType):
            self.raiseSemanticErr(f"Cannot initialize array {arr_type} with {definition_type}")
        for i in range(0, len(arr_type.dimension)):
            if arr_type.dimension[i] < definition_type.dimension[i]:
                self.raiseWarning(f"Excess elements in scalar initializer: {arr_type.dimension[i]} < {definition_type.dimension[i]}")
        node_w.n.definition_w.n.adjust(arr_type.dimension, arr_type.element_type)


    def bin_op(self, node_w: Wrapper[BinaryOp]):
        super().bin_op(node_w)
        self.checkPointerTypes(node_w.n.lhs_w.n.type, node_w.n.rhs_w.n.type)
        if TypeCheckerVisitor.is_comparison(node_w.n.operator):
            node_w.n.type = PrimitiveType('int', True)
        else:
            node_w.n.type = PrimitiveType.typeCoercion([node_w.n.lhs_w.n.type.type, node_w.n.rhs_w.n.type.type], True)

    def un_op(self, node_w: Wrapper[UnaryOp]):
        super().un_op(node_w)
        if TypeCheckerVisitor.is_comparison(node_w.n.operator):
            node_w.n.type = PrimitiveType('int', True)
        else:
            node_w.n.type = deepcopy(node_w.n.operand_w.n.type)
        if node_w.n.operator in ["--", "++"]:
            self.checkAssignee(node_w.n.operand_w)

    def deref_op(self, node_w: Wrapper[DerefOp]):
        super().deref_op(node_w)
        new_type: PrimitiveType = deepcopy(node_w.n.operand_w.n.type)
        if new_type.ptr_count == 0:
            self.raiseSemanticErr(f"Cannot dereference non pointer")
        new_type.decrease_ptr_count()
        node_w.n.type = new_type

    def addressof_op(self, node_w: Wrapper[AddressOfOp]):
        super().addressof_op(node_w)
        if not (isinstance(node_w.n.operand_w.n, Identifier) or isinstance(node_w.n.operand_w.n, DerefOp)):
            self.raiseSemanticErr(f"Cannot get the address of an rvalue")
        new_type: PrimitiveType = deepcopy(node_w.n.operand_w.n.type)
        new_type.increase_ptr_count()
        node_w.n.type = new_type

    def cast_op(self, node_w: Wrapper[CastOp]):
        super().cast_op(node_w)
        node_w.n.type = node_w.n.target_type

    def assign(self, node_w: Wrapper[Assignment]):
        super().assign(node_w)
        node_w.n.type = deepcopy(node_w.n.assignee_w.n.type)
        self.checkImplicitDemotion(node_w.n.assignee_w.n.type, node_w.n.value_w.n.type)
        self.checkAssignee(node_w.n.assignee_w)
        self.checkPointerTypes(node_w.n.assignee_w.n.type, node_w.n.value_w.n.type)
        self.checkDiscardedPointerQualifier(node_w.n.assignee_w.n.type, node_w.n.value_w.n.type)

    def identifier(self, node_w: Wrapper[Identifier]):
        node_w.n.type = deepcopy(node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.name).type)

    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        self.checkValidPrimitiveType(node_w.n.type)
        super().variable_decl(node_w)
        if node_w.n.definition_w.n is not None:
            self.checkPointerTypes(node_w.n.type, node_w.n.definition_w.n.type)
            self.checkImplicitDemotion(node_w.n.type, node_w.n.definition_w.n.type)
            self.checkDiscardedPointerQualifier(node_w.n.type, node_w.n.definition_w.n.type)
            if isinstance(node_w.n.type, ArrayType):
                self.checkArrayInitialization(node_w)
    def array_access(self, node_w: Wrapper[ArrayAccess]):
        super().array_access(node_w)
        for index_w in node_w.n.indices:
            if index_w.n.type.type not in ['int', 'char']:
                self.raiseSemanticErr(f"Cannot access array {node_w.n.identifier_w.n.name}: index {index_w.n} not an integer")
        ptr_count: int = node_w.n.identifier_w.n.type.ptr_count
        resulting_dim: int = ptr_count - len(node_w.n.indices)
        if resulting_dim < 0:
            self.raiseSemanticErr(f"Cannot access array {node_w.n.identifier_w.n.name}: trying to access dimension {len(node_w.n.indices)} but array has {ptr_count}")
        node_w.n.type = PrimitiveType(node_w.n.identifier_w.n.type.type, node_w.n.identifier_w.n.type.is_constant, ptr_count-1)

    def array_lit(self, node_w: Wrapper[ArrayLiteral]):
        super().array_lit(node_w)
        values = node_w.n.value
        types: list[str] = [elem_w.n.type.type for elem_w in values]
        coerced_type = PrimitiveType.typeCoercion(types, False)
        array_types = [elem_w.n.type for elem_w in values if isinstance(elem_w.n.type, ArrayType)]
        dim_max = max(array_types, key=lambda type: type.dimension[0]) if len(array_types) > 0 else None
        dim = [len(values)] + dim_max.dimension if dim_max is not None else [len(values)]
        node_w.n.type = ArrayType(coerced_type, dim)


    def switch(self, node_w: Wrapper[SwitchStatement]):
        super().switch(node_w)
        if node_w.n.value_w.n.type.type not in ['int', 'char']:
            self.raiseSemanticErr(f"Switch value must be an integer")

    def func_call(self, node_w: Wrapper[FunctionCall]):
        super().func_call(node_w)
        entry: SymbolTableEntry = node_w.n.local_symtab_w.n.lookup_symbol(node_w.n.func_name)
        func_type: FunctionType = entry.type
        node_w.n.type = func_type.return_type

        arg_count = len(node_w.n.arguments)
        param_count = len(func_type.parameter_types)
        if arg_count != param_count:
            more_or_less_str: str = "Too many" if arg_count > param_count else "Too few"
            self.raiseSemanticErr(f"{more_or_less_str} arguments to function {node_w.n.func_name}")
        for i in range(0, arg_count):
            arg_type = node_w.n.arguments[i].n.type
            param_type = func_type.parameter_types[i]
            self.checkImplicitDemotion(param_type, arg_type)
            self.checkPointerTypes(param_type, arg_type)
            self.checkDiscardedPointerQualifier(param_type, arg_type)


    def return_stmt(self, node_w: Wrapper[ReturnStatement]):
        super().return_stmt(node_w)
        if node_w.n.expr_w is not None:
            node_w.n.type = node_w.n.expr_w.n.type
        function_signature: FunctionType = node_w.n.local_symtab_w.n.get_enclosing_function_type()
        self.checkReturnType(function_signature.return_type, node_w.n.type)









