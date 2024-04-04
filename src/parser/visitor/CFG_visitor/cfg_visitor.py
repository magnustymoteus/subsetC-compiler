from src.parser.visitor.AST_visitor.ast_visitor import *
from src.parser.CFG import *

class CFGVisitor(ASTVisitor):
    def __init__(self, cfg: ControlFlowGraph):
        self.visit(cfg.bblock_list)

    def visit(self, node_w: Wrapper[CFGNode]):
        match node_w.n:
            case BasicBlockList():
                self.basic_block_list(node_w)
            case BasicBlock():
                self.basic_block(node_w)
            case Assignment():
                self.assign(node_w)
            case BinaryOp():
                self.bin_op(node_w)
            case DerefOp():
                self.deref_op(node_w)
            case AddressOfOp():
                self.addressof_op(node_w)
            case UnaryOp():
                self.un_op(node_w)
            case CastOp():
                self.cast_op(node_w)
            case FunctionDefinition():
                self.func_def(node_w)
            case VariableDeclaration():
                self.variable_decl(node_w)
            case Literal():
                self.lit(node_w)
            case Identifier():
                self.identifier(node_w)
            case PrintStatement():
                self.print(node_w)
            case Enumeration():
                self.enum(node_w)
            case _:
                raise Exception


    def basic_block_list(self, node_w: Wrapper[BasicBlockList]):
        for basic_block in node_w.n.basic_blocks:
            self.visit(basic_block)
    def basic_block(self, node_w: Wrapper[BasicBlock]):
        for ast_item in node_w.n.ast_items:
            self.visit(ast_item)




