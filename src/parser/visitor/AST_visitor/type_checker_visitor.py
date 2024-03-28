from src.parser.visitor.AST_visitor.ast_visitor import *
from copy import deepcopy
'''Here we traverse in post order and assign for almost each node a type. We then check for incompatible types or constant assignment.'''
class TypeCheckerVisitor(ASTVisitor):
    type_ranks: list[str] = ["char", "int", "float"]
    def __init__(self, ast: Ast):
        super().__init__(ast)

    @staticmethod
    def typeCoercion(primitive_types : list[str], is_constant: bool) -> PrimitiveType:
        current_rank = 0
        for current_type in primitive_types:
            index = TypeCheckerVisitor.type_ranks.index(current_type)
            if index > current_rank:
                current_rank = index
        return PrimitiveType(TypeCheckerVisitor.type_ranks[current_rank], is_constant)

    def checkImplicitDemotion(self, assignee_type: PrimitiveType, value_type: PrimitiveType):
        if TypeCheckerVisitor.type_ranks.index(assignee_type.type) < TypeCheckerVisitor.type_ranks.index(value_type.type):
            self.raiseWarning(f"Implicit demotion from {value_type} to {assignee_type} (possible loss of information)")

    def checkDiscardedPointerQualifier(self, assignee_type: PrimitiveType, value_type: PrimitiveType):
        if assignee_type.ptr_count > 0 and value_type.ptr_count > 0:
            if (not assignee_type.is_constant and value_type.is_constant):
                self.raiseWarning(f"Assignment of {assignee_type} to {value_type} discards const qualifier")


    def checkAssignee(self, assignee_w: Wrapper):
        is_identifier = isinstance(assignee_w.n, Identifier)
        is_deref = isinstance(assignee_w.n, DerefOp)
        if is_identifier or is_deref:
            symtype = assignee_w.n.type
            # TODO: with constant pointers?
            if symtype.ptr_count == 0 and symtype.is_constant:
                self.raiseSemanticErr(f"assignment of readonly variable {symtype}")
        else:
            self.raiseSemanticErr("lvalue required as left operand of assignment")
    def checkPointerTypes(self, left_type: PrimitiveType, right_type: PrimitiveType):
        left_copy = deepcopy(left_type)
        right_copy = deepcopy(right_type)
        if left_copy.ptr_count > 0 and right_copy.ptr_count == 0:
            if right_copy.type != 'int':
                # case where a pointer gets assigned to a non integer non pointer
                self.raiseSemanticErr(f"Cannot assign pointer {left_copy} to {right_copy}")
            # case where a pointer gets assigned to a non pointer integer
        elif left_copy.ptr_count != right_copy.ptr_count:
            # case where two pointers dont match
            self.raiseSemanticErr(f"Incompatible pointer types {left_copy} and {right_copy}")
    def program(self, node_w: Wrapper[Program]):
        super().program(node_w)
    def bin_op(self, node_w: Wrapper[BinaryOp]):
        super().bin_op(node_w)
        self.checkPointerTypes(node_w.n.lhs_w.n.type, node_w.n.rhs_w.n.type)
        node_w.n.type = TypeCheckerVisitor.typeCoercion([node_w.n.lhs_w.n.type.type, node_w.n.rhs_w.n.type.type], True)

    def un_op(self, node_w: Wrapper[UnaryOp]):
        super().un_op(node_w)
        node_w.n.type = deepcopy(node_w.n.operand_w.n.type)
        if node_w.n.is_postfix:
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

    def lit(self, node_w: Wrapper[Literal]):
        match node_w.n:
            case IntLiteral():
                type_str = "int"
            case FloatLiteral():
                type_str = "float"
            case CharLiteral():
                type_str = "char"
            case _:
                raise ValueError("unrecognized literal type")
        node_w.n.type = PrimitiveType(type_str, True)

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
        super().variable_decl(node_w)
        if node_w.n.definition_w.n is not None:
            self.checkPointerTypes(node_w.n.type, node_w.n.definition_w.n.type)
            self.checkImplicitDemotion(node_w.n.type, node_w.n.definition_w.n.type)
            self.checkDiscardedPointerQualifier(node_w.n.type, node_w.n.definition_w.n.type)






