from src.compilation.visitor.CFG_visitor.cfg_visitor import *
from copy import copy

'''Converts AST so that expressions have at most two operands by creating intermediate variables'''
class TACVisitor(CFGVisitor):
    def __init__(self, cfg: ControlFlowGraph):
        self.interm_var_count: int = 0
        self.tacs: dict[CompoundStatement | BasicBlock, list[tuple[Wrapper[Basic], int]]] = {}
        self.subject_stack: list[list[CompoundStatement | BasicBlock, int]] = []
        super().__init__(cfg)
        for subject in self.tacs:
            current_index: int = 0
            for element in self.tacs[subject]:
                if isinstance(subject, CompoundStatement):
                    subject.statements.insert(element[1]+current_index, element[0])
                else:
                    subject.ast_items.insert(element[1]+current_index, element[0])
                current_index += 1


    def compound_stmt(self, node_w: Wrapper[CompoundStatement]):
        self.subject_stack.append([node_w.n, 0])
        stack_index = len(self.subject_stack) - 1
        for statement_w in node_w.n.statements:
            self.visit(statement_w)
            self.subject_stack[stack_index][1] += 1
        self.subject_stack.pop()

    def basic_block(self, node_w: Wrapper[BasicBlock]):
        self.subject_stack.append([node_w.n, 0])
        stack_index = len(self.subject_stack) - 1
        for ast_item_w in node_w.n.ast_items:
            self.visit(ast_item_w)
            self.subject_stack[stack_index][1] += 1
        self.subject_stack.pop()

    def add_node_to_subject(self, node_w: Wrapper[Basic], custom_index: int = None):
        subject = self.subject_stack[-1]
        if self.tacs.get(subject[0], None) is None:
            self.tacs[subject[0]] = []
        if custom_index is None:
            self.tacs[subject[0]].append((node_w, subject[1]))
        else:
            self.tacs[subject[0]].append((node_w, custom_index))



    def addTACNode(self, node_w: Wrapper[Expression], custom_index: int | None = None) -> Wrapper[Identifier]:
        symbol_name: str = f"tac{self.interm_var_count}"
        new_type: PrimitiveType = copy(node_w.n.type)

        identifier: Identifier = Identifier(symbol_name)
        identifier.type = new_type

        def_node: VariableDeclaration = VariableDeclaration(identifier.name, identifier.type)
        def_node.definition_w = node_w
        def_node.local_symtab_w = node_w.n.local_symtab_w

        self.add_node_to_subject(wrap(def_node))

        self.interm_var_count += 1


        return wrap(identifier)

    def bin_op(self, node_w: Wrapper[BinaryOp]):
        super().bin_op(node_w)
        if not (isinstance(node_w.n.lhs_w.n, Identifier) or isinstance(node_w.n.lhs_w.n, Literal)):
            node_w.n.lhs_w = self.addTACNode(node_w.n.lhs_w)
        if not (isinstance(node_w.n.rhs_w.n, Identifier) or isinstance(node_w.n.rhs_w.n, Literal)):
            node_w.n.rhs_w = self.addTACNode(node_w.n.rhs_w)
    def deref_op(self, node_w: Wrapper[DerefOp]):
        super().un_op(node_w)
        if not (isinstance(node_w.n.operand_w.n, Identifier) or isinstance(node_w.n.operand_w.n, Literal)):
            node_w.n.operand_w = self.addTACNode(node_w.n.operand_w)
    def un_op(self, node_w: Wrapper[UnaryOp]):
        super().un_op(node_w)
        if not (isinstance(node_w.n.operand_w.n, Identifier) or isinstance(node_w.n.operand_w.n, Literal)):
                node_w.n.operand_w = self.addTACNode(node_w.n.operand_w)
    def cast_op(self, node_w: Wrapper[CastOp]):
        super().cast_op(node_w)
        if not (isinstance(node_w.n.expression_w.n, Identifier) or isinstance(node_w.n.expression_w.n, Literal)):
            node_w.n.expression_w = self.addTACNode(node_w.n.expression_w)

    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        super().variable_decl(node_w)
        if node_w.n.local_symtab_w.n.has_parent:
            if node_w.n.definition_w.n is not None:
                assign_node = Assignment("=")
                assign_node.assignee_w.n = Identifier(copy(node_w.n.identifier))
                assign_node.value_w.n = copy(node_w.n.definition_w.n)
                assign_node.type = copy(node_w.n.type)
                assign_node.assignee_w.n.type = node_w.n.type
                assign_node.local_symtab_w = node_w.n.local_symtab_w
                node_w.n.definition_w.n = None

                self.add_node_to_subject(wrap(copy(node_w.n)), 0)

                node_w.n = assign_node
        else:
            if node_w.n.definition_w.n is not None:
                if not isinstance(node_w.n.definition_w.n, Literal):
                    self.raiseSemanticErr("Global variable definition must be a compile time constant")





