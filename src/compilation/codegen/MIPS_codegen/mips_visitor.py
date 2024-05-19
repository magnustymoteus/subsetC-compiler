import llvmlite.ir as ir
import llvmlite.ir.instructions as ir_inst

from src.constructs.mips_program import MipsProgram, Variables, Global
from src.constructs.mips_program.node import LabeledBlock, Reg, instr as mips_inst, Label

"""
MIPS code layout:
- module name
- data (static vars)
- text (code)
  - labels
  - instructions


LLVM structure:
Module
- Function
  - Block
    - Instruction
    - Instruction
  - Block
    - Instruction
    - Instruction
- Function
- ...
"""

# TODO:
#  -printf
#  -scanf
#

# pseudo instructions may only use $t0 !!!


def assert_type(value, typename):
    assert type(value).__name__ == typename, f"type '{type(value).__name__}' not implemented"

def get_type_size(type: ir.Type) -> int:
    """Get the size of the type in bytes."""
    # TODO allow for arrays
    match type:
        case ir.IntType():
            return int(type.width / 8)
        case ir.PointerType():
            return get_type_size(type.pointee)
        case ir.FloatType():
            return 4
        case _:
            assert False


class MipsVisitor(ir.Visitor):
    tree: MipsProgram
    "Tree of the mips program blocks with instructions."

    @property
    def last_block(self):
        """Current block being visited."""
        return self.tree.blocks[-1]

    globals: list[Global]
    "List of global variables"

    variables: Variables
    "List of passed variables in current function scope"

    stack_offset: int
    "Largest stack offset used"

    new_function_started: bool
    "True if a new function has just started. Used to indicate to the block visit a new stack frame should be created."

    def __init__(self) -> None:
        self.tree = MipsProgram()
        self.variables = Variables()
        self.stack_offset = 0
        super().__init__()

    def load_value(self, i: ir.Instruction, r: Reg) -> mips_inst.Instruction:
        """Load a value from an instruction or a constant into the register."""
        if isinstance(i, ir.Constant):
            return mips_inst.Li(r, i.constant)  # TODO support full i32 range load
        else:
            return mips_inst.Lw(r, Reg.fp, self.variables[i.name].offset)

    def visit(self, module: ir.Module):
        """Visit a module. Top level visit function."""
        print(type(module).__name__)
        super().visit(module)

    def visit_Function(self, func: ir_inst.Function):
        """Visit a function."""
        print(f"- {type(func).__name__}")

        self.variables.clear()
        self.stack_offset = 0
        self.new_function_started = True
        super().visit_Function(func)

    def visit_BasicBlock(self, bb: ir_inst.Block):
        """Visit a basic block."""
        print(f"  - {type(bb).__name__}")

        self.tree.add_block(LabeledBlock(Label(f"{self.function.name}.{bb.name}")))

        # if new function started, start by creating new stack frame
        if self.new_function_started:
            self.last_block.add_instr(
                # store frame pointer at top of stack
                mips_inst.Sw(Reg.fp, Reg.sp, 0, "new stack frame"),  # sw  $fp, 0($sp)
                # set frame pointer
                mips_inst.Move(Reg.fp, Reg.sp),  # move    $fp, $sp
                # store return address on stack
                mips_inst.Sw(Reg.ra, Reg.fp, -4),  # sw  $ra, -4($fp)
                # move stack pointer down
                mips_inst.Addiu(Reg.sp, Reg.sp, -8),  # subiu   $sp, $sp, 8
                mips_inst.Blank(),
            )
            self.new_function_started = False
            self.stack_offset -= 8  # offset stack by 2 words (fp, ra)
        super().visit_BasicBlock(bb)

    def visit_Instruction(self, instr: ir_inst.Instruction):
        print(f"    - {type(instr).__name__}")

        """Visit an instruction."""
        match instr:
            case ir_inst.AllocaInstr():
                """
                :count: array size
                :size: size of array content, in bytes
                advance sp by :count: * :size:
                save stack offset of array start

                addiu $sp, $sp, -:count:*:size:
                # save variable offset from $fp
                """
                assert len(instr.operands) == 1

                # size of the allocated type
                size = get_type_size(instr.operands[0].type)
                # add variable to the list of variables of that function scope
                self.variables.new_var(Label(instr.name), self.stack_offset)
                self.stack_offset -= size

                # add instruction to the block and create new space on the stack for the var
                self.last_block.add_instr(
                    # move the stack pointer by the size of the variable
                    mips_inst.Addiu(Reg.sp, Reg.sp, -size, mips_inst.IrComment(f"{instr}")),  # addiu $sp, $sp, -size
                    mips_inst.Blank(),
                )
            case ir_inst.Branch():
                print("unhandled!")

            case ir_inst.CallInstr():
                """
                function call stack layout:
                +-----------------+  ┓
                | stack of caller |  ┃
                +-----------------+  ┃
                | function return |  ┃ responsibility of caller
                +-----------------+  ┃
                | function args   |  ┛
                +-----------------+  ┓
                | old $fp         |  ┃
                +-----------------+  ┃
                | new $ra         |  ┃ responsibility of callee
                +-----------------+  ┃
                | stack of callee |  ┃
                +-----------------+  ┛
                """
                print("unhandled!")

            case ir_inst.ConditionalBranch():
                print("unhandled!")

            case ir_inst.Comment():
                self.last_block.add_instr(mips_inst.CComment(instr.text))

            case ir_inst.GEPInstr():
                print("unhandled!")

            case ir_inst.LoadInstr():
                assert len(instr.operands) == 1
                alloc: ir.AllocaInstr = instr.operands[0]  # TODO wrong, operand is just the previous step not always alloca
                assert isinstance(alloc, (ir.AllocaInstr, ir.GEPInstr))

                size = get_type_size(alloc.operands[0].type)
                var = self.variables.new_var(Label(instr.name), self.stack_offset)
                self.stack_offset -= size
                self.last_block.add_instr(
                    mips_inst.Addiu(Reg.sp, Reg.sp, -size, mips_inst.IrComment(f"{instr}")),
                    # load value into reg
                    mips_inst.Lw(Reg.t1, Reg.fp, self.variables[alloc.name].offset),  # lw $t1, $fp, src
                    # store value in new variable
                    mips_inst.Sw(Reg.t1, Reg.fp, var.offset),  # lw $t1, $fp, dest
                    mips_inst.Blank(),
                )

            case ir_inst.Ret():
                assert len(instr.operands) == 1  # ? likely wrong for structs
                ret_val: ir.Instruction = instr.operands[0]
                # size = get_type_size(ret_val.type) # TODO unused
                self.last_block.add_instr(
                    mips_inst.IrComment(f"{instr}"),
                    mips_inst.Comment("clean up stack frame"),
                    # load return value and store it at return address on the stack
                    self.load_value(ret_val, Reg.t1),
                    # mips_inst.Lw(Reg.t1, Reg.fp, self.variables[ret_val.name].offset),  # lw $t1, $fp, src
                    mips_inst.Sw(Reg.t1, Reg.fp, 4),  # sw $t1, $fp, 4
                    # restore return register
                    mips_inst.Lw(Reg.ra, Reg.fp, -4),  # lw  $ra, -4($fp)
                    # restore stack pointer to start of frame
                    mips_inst.Move(Reg.sp, Reg.fp),  # move    $sp, $fp
                    # restore previous frame pointer
                    mips_inst.Lw(Reg.fp, Reg.sp),  # lw  $fp, 0($sp)
                    # jump back to caller
                    mips_inst.Jr(Reg.ra),  # jr  $ra
                    mips_inst.Blank(),
                )

            case ir_inst.StoreInstr():
                self.handle_store(instr)

            case ir_inst.SwitchInstr():
                print("unhandled!")

            case ir_inst.ICMPInstr():
                """
                Performs integer comparison
                """

                self.variables.new_var(Label(instr.name), self.stack_offset)
                size: int = int(instr.type.width / 8)  # TODO allow for arrays
                self.last_block.add_instr(mips_inst.IrComment(f"{instr}"))
                assert len(instr.operands) == 2

                self.last_block.add_instr(
                    self.load_value(instr.operands[0], Reg.t1),
                    self.load_value(instr.operands[1], Reg.t2),
                )

                match instr.op:
                    case "eq":
                        print("\t\t -eq")
                        self.last_block.add_instr(mips_inst.Sle(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp eq")))
                    case "ne":
                        print("ne")
                        self.last_block.add_instr(mips_inst.Sne(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp ne")))
                    case "ugt":
                        print("unhandled : ugt")
                    case "uge":
                        print("unhandled : uge")
                    case "ult":
                        print("unhandled : ult")
                    case "ule":
                        print("unhandled : ule")
                    case "sgt":
                        print("unhandled : sgt")
                    case "sge":
                        print("unhandled : sge")
                    case "slt":
                        print("unhandled : slt")
                    case "sle":
                        print("unhandled : sle")
                    case _:
                        raise ValueError(f"Unsupported icmp operation: '{instr.op}'")

                self.last_block.add_instr(
                    mips_inst.Sw(Reg.t1, Reg.fp, self.variables[instr.name].offset),
                    mips_inst.Addiu(Reg.sp, Reg.sp, -size),
                    mips_inst.Blank(),
                )

                self.stack_offset -= size

            case ir_inst.CompareInstr():
                print("unhandled!")

            case ir_inst.CastInstr():
                assert len(instr.operands) == 1
                # ? instruction ignored because mips is 32bit, possibly a problem in future
                if isinstance(instr.operands[0], ir.Constant):
                    size = get_type_size(instr.operands[0].type)
                    var = self.variables.new_var(Label(instr.name), self.stack_offset)
                    self.stack_offset += size
                    self.last_block.add_instr(
                        mips_inst.Li(Reg.t0, instr.operands[0].constant, mips_inst.IrComment(f"{instr}")),  # TODO support full i32 range load
                        mips_inst.Sw(Reg.t1, Reg.fp, var.offset),
                        mips_inst.Addiu(Reg.sp, Reg.sp, -size),  # addiu $sp, $sp, -size
                        mips_inst.Blank(),
                    )
                    self.stack_offset -= size
                else:
                    self.variables.new_alias(Label(instr.name), self.variables[instr.operands[0].name])
                    self.last_block.add_instr(mips_inst.IrComment(f"{instr}"))

            case ir_inst.Instruction():
                assert len(instr.operands) == 2  # ? possibly needs to be <= 2 for unary ops
                assert_type(instr, "Instruction")
                self.handle_instruction(instr)

            case _:
                raise ValueError(f"Unsupported type: '{type(instr).__name__}'")

    def handle_store(self, instr: ir_inst.StoreInstr):
        value: ir.Instruction = instr.operands[0]
        "value to be stored"

        gen: ir.AllocaInstr = instr.operands[1]
        "instruction that allocated the value space (expect alloca or gep)"

        assert isinstance(gen, (ir.AllocaInstr, ir.GEPInstr))
        assert len(instr.operands) == 2

        self.last_block.add_instr(mips_inst.IrComment(f"{instr}"))

        # create store value
        self.last_block.add_instr(self.load_value(value, Reg.t1))

        # store created value
        assert gen.name in self.variables
        var = self.variables[gen.name]
        self.last_block.add_instr(
            mips_inst.Sw(Reg.t1, Reg.fp, var.offset),
            mips_inst.Blank(),
        )

    def handle_instruction(self, instr: ir.Instruction):
        var = self.variables.new_var(Label(instr.name), self.stack_offset)
        size = get_type_size(instr.type)
        self.last_block.add_instr(mips_inst.Addiu(Reg.sp, Reg.sp, -size, mips_inst.IrComment(f"{instr}")))
        assert len(instr.operands) == 2

        self.last_block.add_instr(
            self.load_value(instr.operands[0], Reg.t1),
            self.load_value(instr.operands[1], Reg.t2),
        )

        match instr.opname:
            case "add":
                self.last_block.add_instr(mips_inst.Addu(Reg.t1, Reg.t1, Reg.t2))
            case "sub":
                self.last_block.add_instr(mips_inst.Subu(Reg.t1, Reg.t1, Reg.t2))
            case "mul":
                self.last_block.add_instr(mips_inst.Mul(Reg.t1, Reg.t1, Reg.t2))
            case "sdiv":
                self.last_block.add_instr(
                    mips_inst.Div(Reg.t1, Reg.t2),
                    mips_inst.Mflo(Reg.t1),
                )
            case "udiv":
                self.last_block.add_instr(
                    mips_inst.Divu(Reg.t1, Reg.t2),
                    mips_inst.Mflo(Reg.t1),
                )
            case "srem":
                self.last_block.add_instr(
                    mips_inst.Div(Reg.t1, Reg.t2),
                    mips_inst.Mfhi(Reg.t1),
                )
            case "urem":
                self.last_block.add_instr(
                    mips_inst.Divu(Reg.t1, Reg.t2),
                    mips_inst.Mfhi(Reg.t1),
                )
            case "and":
                self.last_block.add_instr(mips_inst.And(Reg.t1, Reg.t1, Reg.t2))
            case "or":
                self.last_block.add_instr(mips_inst.Or(Reg.t1, Reg.t1, Reg.t2))
            case "xor":
                self.last_block.add_instr(mips_inst.Xor(Reg.t1, Reg.t1, Reg.t2))
            case _:
                print(f"Unhandled instruction: '{instr.opname}'")

        self.last_block.add_instr(
            mips_inst.Sw(Reg.t1, Reg.fp, var.offset),
            mips_inst.Blank(),
        )

        self.stack_offset -= size
