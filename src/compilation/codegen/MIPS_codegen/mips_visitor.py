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

def assert_type(value, typename):
    assert type(value).__name__ == typename, f"type '{type(value).__name__}' not implemented"


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
                mips_inst.Comment("new stack frame"),
                # store frame pointer at top of stack
                mips_inst.Sw(Reg.fp, Reg.sp, 0),      # sw  $fp, 0($sp)
                # set frame pointer
                mips_inst.Move(Reg.fp, Reg.sp),       # move    $fp, $sp
                # store return address on stack
                mips_inst.Sw(Reg.ra, Reg.fp, -4),     # sw  $ra, -4($fp)
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
                size: int = int(instr.operands[0].type.width / 8)  # TODO allow for arrays

                self.variables.new_var(Label(instr.name), self.stack_offset)
                self.last_block.add_instr(
                    mips_inst.IrComment(f"{instr}"),
                    # move the stack pointer by the size of the variable
                    mips_inst.Addiu(Reg.sp, Reg.sp, -size),  # addiu $sp, $sp, -size
                    mips_inst.Blank(),
                )
                self.stack_offset -= size
            case ir_inst.Branch():
                print("unhandled!")

            case ir_inst.CallInstr():
                """
                # MIPS code:
                """
                print("unhandled!")

            case ir_inst.ConditionalBranch():
                print("unhandled!")

            case ir_inst.Comment():
                self.last_block.add_instr(mips_inst.CComment(instr.text))

            case ir_inst.GEPInstr():
                print("unhandled!")

            case ir_inst.LoadInstr():
                alloc: ir.AllocaInstr = instr.operands[0]
                assert isinstance(alloc, ir.AllocaInstr)

                self.variables.new_var(Label(instr.name), self.stack_offset)
                self.last_block.add_instr(
                    mips_inst.IrComment(f"{instr}"),
                    # load value into reg
                    mips_inst.Lw(Reg.t0, Reg.fp, self.variables[alloc.name].offset), # lw $t0, $fp, src
                    # store value in new variable
                    mips_inst.Sw(Reg.t0, Reg.fp, self.variables[instr.name].offset), # lw $t0, $fp, dest
                    mips_inst.Blank(),
                )

            case ir_inst.Ret():
                self.last_block.add_instr(
                    mips_inst.IrComment(f"{instr}"),
                    # restore return register
                    mips_inst.Lw(Reg.ra, Reg.fp, -4),  # lw  $ra, -4($fp)
                    # restore stack pointer to start of frame
                    mips_inst.Move(Reg.sp, Reg.fp),    # move    $sp, $fp
                    # restore previous frame pointer
                    mips_inst.Lw(Reg.fp, Reg.sp),      # lw  $fp, 0($sp)
                    # jump back to caller
                    mips_inst.Jr(Reg.ra),              # jr  $ra
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
                print("unhandled! aliased")
                self.variables.new_alias(Label(instr.name), self.variables[instr.operands[0].name])
                self.last_block.add_instr(mips_inst.IrComment(f"{instr}"))

            case ir_inst.CompareInstr():
                assert_type(instr, "CompareInstr")
                print("unhandled!")

            case ir_inst.CastInstr():
                # ? instruction ignored because mips is 32bit, possibly a problem in future
                self.variables.new_alias(Label(instr.name), self.variables[instr.operands[0].name])
                self.last_block.add_instr(mips_inst.IrComment(f"{instr}"))

            case ir_inst.Instruction():
                assert_type(instr, "Instruction")
                print("unhandled! aliased")
                self.variables.new_alias(Label(instr.name), self.variables[instr.operands[0].name])
                self.last_block.add_instr(mips_inst.IrComment(f"{instr}"))

            case _:
                raise ValueError(f"Unsupported type: '{type(instr).__name__}'")

    def handle_store(self, instr: ir_inst.StoreInstr):
        value: ir.Instruction = instr.operands[0]
        alloc: ir.AllocaInstr = instr.operands[1]
        assert isinstance(alloc, ir.AllocaInstr)
        assert len(instr.operands) == 2

        self.last_block.add_instr(
            mips_inst.IrComment(f"{instr}"),
        )

        # create store value
        match value:
            case ir.Constant():
                self.last_block.add_instr(
                    mips_inst.Li(Reg.t0, value.constant),  # TODO support full i32 range load
                )
            case ir.Instruction():
                # ? assuming this will be the same for all non-constant instruction and can be generalised
                assert_type(value, "Instruction")
                self.last_block.add_instr(
                    mips_inst.Lw(Reg.t0, Reg.fp, self.variables[value.name].offset),
                )

        # store created value
        assert alloc.name in self.variables
        var = self.variables[alloc.name]
        self.last_block.add_instr(mips_inst.Sw(Reg.t0, Reg.fp, var.offset), mips_inst.Blank())
