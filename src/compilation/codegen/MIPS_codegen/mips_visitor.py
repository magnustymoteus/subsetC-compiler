import llvmlite.ir as ir
import llvmlite.ir.instructions as ir_inst

from src.constructs.mips_program import MipsProgram, Variable, Variables, Global
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

        self.tree.add_block(LabeledBlock(Label(f"{self.function.name}_{bb.name}")))

        # if new function started, start by creating new stack frame
        if self.new_function_started:
            self.last_block.add_instr(
                mips_inst.Comment("new stack frame"),
                mips_inst.Sw(Reg.fp, Reg.sp, 0),      # sw  $fp, 0($sp)         # store frame pointer at top of stack
                mips_inst.Move(Reg.fp, Reg.sp),       # move    $fp, $sp        # set frame pointer
                mips_inst.Addiu(Reg.sp, Reg.sp, -8),  # subiu   $sp, $sp, 8     # move stack pointer down
                mips_inst.Sw(Reg.ra, Reg.fp, -4),     # sw  $ra, -4($fp)        # store return address on stack
            )
            self.new_function_started = False
            self.stack_offset -= 8 # offset stack by 2 words (fp, ra)
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

                self.variables.add_var(Variable(Label(instr.name), self.stack_offset))
                self.last_block.add_instr(
                    mips_inst.Comment("alloca"),
                    mips_inst.Addiu(Reg.sp, Reg.sp, -size),
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
                self.last_block.add_instr(mips_inst.Comment(instr.text))
            case ir_inst.GEPInstr():
                print("unhandled!")
            case ir_inst.LoadInstr():
                print("unhandled!")
            case ir_inst.Ret():
                self.last_block.add_instr(
                    mips_inst.Comment("ret"),
                    mips_inst.Lw(Reg.ra, Reg.fp, -4),  # lw  $ra, -4($fp)    # restore return register
                    mips_inst.Move(Reg.sp, Reg.fp),    # move    $sp, $fp    # restore stack pointer to start of frame
                    mips_inst.Lw(Reg.fp, Reg.sp),      # lw  $fp, 0($sp)     # restore previous frame pointer
                    mips_inst.Jr(Reg.ra),              # jr  $ra             # jump back to caller
                )
            case ir_inst.StoreInstr():
                value: ir.Constant = instr.operands[0]
                alloc: ir.AllocaInstr = instr.operands[1]
                assert isinstance(value, ir.Constant)
                assert isinstance(alloc, ir.AllocaInstr)

                assert alloc.name in self.variables
                var = self.variables[alloc.name]
                self.last_block.add_instr(
                    mips_inst.Comment("store"),
                    mips_inst.Li(Reg.t0, value.constant),  # TODO support full i32 range load
                    mips_inst.Sw(Reg.t0, Reg.fp, var.offset),
                )
            case ir_inst.SwitchInstr():
                print("unhandled!")

            case ir_inst.ICMPInstr():
                """
                Performs integer comparison
                """
                # print("unhandled!")
                pass

            case ir_inst.CompareInstr():
                # print("unhandled!")
                pass

            case ir_inst.CastInstr():
                # print("unhandled!")
                pass

            case ir_inst.Instruction():
                # print("unhandled!")
                pass
            case ir_inst.Instruction():
                print("unhandled!")
            case _:
                raise ValueError(f"Unsupported instruction: {type(instr).__name__}")