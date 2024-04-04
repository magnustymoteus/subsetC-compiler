from typing import Generator
from src.parser.AST.node import *


def main():
    ast = Ast()
    n1: Wrapper[BinaryOp] = wrap(BinaryOp("+"))
    n2: Wrapper[BinaryOp] = wrap(BinaryOp("+"))
    n3: Wrapper[IntLiteral] = wrap(IntLiteral("1"))
    n4: Wrapper[IntLiteral] = wrap(IntLiteral("2"))
    n5: Wrapper[UnaryOp] = wrap(UnaryOp("-"))
    n6: Wrapper[IntLiteral] = wrap(IntLiteral("3"))

    ast.set_root(n1)
    n1.n.lhs_w = n2
    n1.n.rhs_w = n3
    n2.n.lhs_w = n4
    n2.n.rhs_w = n5
    n5.n.operand_w = n6

    graph = ast.to_dot_graph()
    graph.save(filename="graph.gv")

    for node in ast.iter(AstIter):
        print(node.n)


class Stack:
    """
    Iteration stack. Contains a number of frames queues.
    ```
    The datastructure looks as follows:
                        |= the first node of each frame is always the "active" node for that frame
                        |          |= later nodes are queued to be processed after the current node is finished
    Stack [          |          |
        FrameQueue [Node3-1, Node3-2, Node3-3] <- the top frame is always the "active" frame
        FrameQueue [Node2-1]
        FrameQueue [Node1-1, Node1-2]
    ]
    ```
    """
    class FrameQueue:
        """Frame queue. Each frames has a number of items which are popped FIFO order."""

        def __init__(self, nodes: Wrapper[Basic] | list[Wrapper[Basic]]) -> None:
            self.queue: list[Wrapper[Basic]]
            match nodes:
                case list():
                    self.queue = nodes
                case Wrapper():
                    self.queue = [nodes]
            self.first_visited: bool = False

        @property
        def front(self) -> Wrapper[Basic]:
            """Return the node at the front of the queue."""
            return self.queue[0]

        def pop_front(self) -> Wrapper[Basic]:
            """Remove and return the node at the front of the queue."""
            self.first_visited = False
            return self.queue.pop(0)

        def from_start(self, index: int) -> Wrapper[Basic]:
            """Get the node at given index, starting from the front."""
            return self.queue[index]

        def empty(self) -> bool:
            """Check if the queue is empty."""
            return len(self.queue) == 0

        def __len__(self) -> int:
            return len(self.queue)

        def __repr__(self) -> str:
            repr: str = "FrameQueue: ["
            for node in self.queue[0:-1]:
                repr += f"{node.n}, "
            repr += f"{self.queue[-1].n}]"
            return repr

    # =====================================================================

    def __init__(self, start_node: Wrapper[Basic]) -> None:
        self.frame_stack: list[Stack.FrameQueue] = []
        self.new_frame(start_node)

    def next(self) -> Wrapper[Basic]:
        """Remove and return the next node on the top frame."""
        next: Wrapper[Basic] = self.top.pop_front()
        if self.top.empty():
            self.frame_stack.pop()
        return next

    def peek_next(self) -> Wrapper[Basic]:
        """Return the next node on the top frame."""
        return self.top.front

    @property
    def top(self) -> FrameQueue:
        """Get the top frame queue."""
        return self.frame_stack[-1]

    def from_top(self, index: int) -> FrameQueue:
        """Get the frame queue at provided index, starting from the top."""
        return self.frame_stack[-index]

    def from_bottom(self, index: int) -> FrameQueue:
        """Get the frame queue at provided index, starting from the bottom."""
        return self.frame_stack[index]

    def new_frame(self, frame: Wrapper[Basic] | list[Wrapper[Basic]] | FrameQueue):
        """Add a new frame to the top of the frame stack."""
        match frame:
            case Wrapper() | list():
                self.frame_stack.append(Stack.FrameQueue(frame))
            case Stack.FrameQueue():
                self.frame_stack.append(frame)

    def __len__(self) -> int:
        return len(self.frame_stack)

    def __repr__(self) -> str:
        repr: str = "Stack: [\n"
        for frame in range(len(self.frame_stack), 0, -1):
            repr += f"  {self.frame_stack[frame-1]}\n"
        repr += "]"
        return repr


class Ast:
    pass


class AstIter:
    """Iterate over all nodes in postorder."""

    def __init__(self, ast: Ast) -> None:
        self.ast = ast

    def __iter__(self) -> Generator[Wrapper[Basic], None, None]:
        self.stack: Stack = Stack(self.ast.root_w)

        while len(self.stack) > 0:
            if not self.stack.top.first_visited:
                self.stack.top.first_visited = True
                match self.stack.peek_next().n:
                    case Program():
                        self.expand_program(self.stack.top.front)
                    case BinaryOp():
                        self.expand_bin_op(self.stack.top.front)
                    case UnaryOp():
                        self.expand_un_op(self.stack.top.front)
                    case CastOp():
                        self.expand_cast_op(self.stack.top.front)
                    case Assignment():
                        self.expand_assign(self.stack.top.front)
                    case CompoundStatement():
                        self.expand_compound_stmt(self.stack.top.front)
                    case FunctionDefinition():
                        self.expand_func_def(self.stack.top.front)
                    case VariableDeclaration():
                        self.expand_variable_decl(self.stack.top.front)
                    case PrintStatement():
                        self.expand_print_stmt(self.stack.top.front)
                    case Literal():
                        pass
                    case Identifier():
                        pass
                    case Enumeration():
                        pass
                    case _:
                        # TODO proper exception type
                        raise Exception("Unhandled node type")
            else:
                yield self.stack.next()

    def expand_program(self, node_w: Wrapper[Program]):
        """Method called when encountering a BinOp node."""
        self.stack.new_frame([stmt for stmt in node_w.n.children])

    def expand_bin_op(self, node_w: Wrapper[BinaryOp]):
        """Method called when encountering a BinOp node."""
        self.stack.new_frame([node_w.n.lhs_w, node_w.n.rhs_w])

    def expand_un_op(self, node_w: Wrapper[UnaryOp]):
        """Method called when encountering a UnOp node."""
        self.stack.new_frame(node_w.n.operand_w)

    def expand_print_stmt(self, node_w: Wrapper[PrintStatement]):
        self.stack.new_frame(node_w.n.argument_w)

    def expand_cast_op(self, node_w: Wrapper[CastOp]):
        self.stack.new_frame([node_w.n.expression_w])

    def expand_assign(self, node_w: Wrapper[Assignment]):
        """Method called when encountering a Assign node."""
        self.stack.new_frame([node_w.n.assignee_w, node_w.n.value_w])

    def expand_compound_stmt(self, node_w: Wrapper[CompoundStatement]):
        """Method called when encountering a Compound Statement node."""
        if len(node_w.n.statements) > 0:
            self.stack.new_frame([stmt for stmt in node_w.n.statements])
    def expand_func_def(self, node_w: Wrapper[FunctionDefinition]):
        """Method called when encountering a Function Definition node."""
        self.stack.new_frame([node_w.n.body_w])
    def expand_variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        """Method called when encountering a Variable Declaration node."""
        if node_w.n.definition_w.n is not None:
            self.stack.new_frame([node_w.n.definition_w])



class AstVisit(ABC):
    """
    Generic AST iteration type.
    Provides common methods for each node type all derived iterators must implement.

    Derived iterators should yield node wrappers rather than actual nodes.
    This way the reference in the wrapper can be changed and a node can be replaced by an entirely different one.
    """

    def visit(self):
        self.__iter__()
    def __init__(self, ast: Ast) -> None:
        self.ast = ast

    def __iter__(self) -> Generator[Wrapper[Basic], None, None]:
        self.stack: Stack = Stack(self.ast.root_w)

        while len(self.stack) > 0:
            if not self.stack.top.first_visited:
                self.stack.top.first_visited = True
                match self.stack.peek_next().n:
                    case Program():
                        self.expand_program(self.stack.top.front)
                    case BinaryOp():
                        self.expand_bin_op(self.stack.top.front)
                    case UnaryOp():
                        self.expand_un_op(self.stack.top.front)
                    case CastOp():
                        self.expand_cast_op(self.stack.top.front)
                    case Assignment():
                        self.expand_assign(self.stack.top.front)
                    case CompoundStatement():
                        self.expand_compound_stmt(self.stack.top.front)
                    case FunctionDefinition():
                        self.expand_func_def(self.stack.top.front)
                    case VariableDeclaration():
                        self.expand_variable_decl(self.stack.top.front)
                    case PrintStatement():
                        self.expand_print_stmt(self.stack.top.front)
                    case Literal():
                        pass
                    case Identifier():
                        pass
                    case _:
                        raise Exception  # TODO proper exception type
            else:
                next = self.stack.next()
                match next.n:
                    case Program():
                        self.program(next)
                    case BinaryOp():
                        self.bin_op(next)
                    case UnaryOp():
                        self.un_op(next)
                    case Assignment():
                        self.assign(next)
                    case CompoundStatement():
                        self.compound_stmt(next)
                    case FunctionDefinition():
                        self.func_def(next)
                    case VariableDeclaration():
                        self.variable_decl(next)
                    case Literal():
                        self.lit(next)
                    case Identifier():
                        self.identifier(next)
                    case PrintStatement():
                        self.print_stmt(next)
                    case _:
                        raise Exception  # TODO proper exception type

    def expand_program(self, node_w: Wrapper[Program]):
        """Method called when encountering a Program node."""
        self.stack.new_frame([stmt for stmt in node_w.n.children])

    def expand_bin_op(self, node_w: Wrapper[BinaryOp]):
        """Method called when encountering a BinOp node."""
        self.stack.new_frame([node_w.n.lhs_w, node_w.n.rhs_w])

    def expand_un_op(self, node_w: Wrapper[UnaryOp]):
        """Method called when encountering a UnOp node."""
        self.stack.new_frame([node_w.n.operand_w])

    def expand_cast_op(self, node_w: Wrapper[CastOp]):
        self.stack.new_frame([node_w.n.expression_w])

    def expand_assign(self, node_w: Wrapper[Assignment]):
        """Method called when encountering a Assign node."""
        self.stack.new_frame([node_w.n.assignee_w, node_w.n.value])

    def expand_compound_stmt(self, node_w: Wrapper[CompoundStatement]):
        """Method called when encountering a Compound Statement node."""
        self.stack.new_frame([stmt for stmt in node_w.n.statements])
    def expand_func_def(self, node_w: Wrapper[FunctionDefinition]):
        """Method called when encountering a Function Definition node."""
        self.stack.new_frame([node_w.n.body_w])
    def expand_variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        """Method called when encountering a Variable Declaration node."""
        self.stack.new_frame([node_w.n.definition_w])
    def expand_print_stmt(self, node_w: Wrapper[PrintStatement]):
        self.stack.new_frame([node_w.n.argument_w])

    @abstractmethod
    def program(self, node_w: Wrapper[Program]):
        """Method called when encountering a Program node."""
        raise Exception  # TODO proper exception type

    @abstractmethod
    def print_stmt(self, node_w: Wrapper[PrintStatement]):
        raise Exception

    @abstractmethod
    def bin_op(self, node_w: Wrapper[BinaryOp]):
        """Method called when encountering a BinOp node."""
        raise Exception  # TODO proper exception type

    @abstractmethod
    def un_op(self, node_w: Wrapper[UnaryOp]):
        """Method called when encountering a UnOp node."""
        raise Exception  # TODO proper exception type

    @abstractmethod
    def cast_op(self, node_w: Wrapper[CastOp]):
        raise Exception

    @abstractmethod
    def lit(self, node_w: Wrapper[Literal]):
        """Method called when encountering a UnOp node."""
        raise Exception  # TODO proper exception type

    @abstractmethod
    def assign(self, node_w: Wrapper[Assignment]):
        """Method called when encountering a Assign node."""
        raise Exception  # TODO proper exception type

    @abstractmethod
    def identifier(self, node_w: Wrapper[Identifier]):
        """Method called when encountering a Assign node."""
        raise Exception  # TODO proper exception type

    @abstractmethod
    def compound_stmt(self, node_w: Wrapper[CompoundStatement]):
        """Method called when encountering a Assign node."""
        raise Exception  # TODO proper exception type

    @abstractmethod
    def func_def(self, node_w: Wrapper[FunctionDefinition]):
        """Method called when encountering a Assign node."""
        raise Exception  # TODO proper exception type

    @abstractmethod
    def variable_decl(self, node_w: Wrapper[VariableDeclaration]):
        """Method called when encountering a Assign node."""
        raise Exception  # TODO proper exception type



class Ast:
    def __init__(self) -> None:
        self.root_w: Wrapper[Basic] = wrap()

    def iter(self, iter_method: AstIter) -> Generator[Wrapper[Basic], None, None]:
        """
        Iterate over the nodes of the tree.
        What elements and in which order is decided by the handler functions from the `iter_method`.
        """
        return iter_method(self)

    def set_root(self, root: Wrapper[Basic]) -> None:
        self.root_w = root

    def to_dot_graph(self) -> Digraph:
        """
        Export the AST to a dot graph.
        """
        graph = Digraph(strict="true")
        self.root_w.n.append_to_graph(graph, None)

        return graph


if __name__ == "__main__":
    main()
