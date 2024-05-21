import math, struct

import llvmlite.ir as ir
import llvmlite.ir.instructions as ir_inst

from src.constructs.mips_program import MipsProgram, Variables, Global
from src.constructs.mips_program.node import LabeledBlock, Reg, Regf, instr as mips_inst, Label

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
            res = math.ceil(type.width / 8)
        case ir.PointerType():
            res = get_type_size(type.pointee)
        case ir.FloatType():
            res = 4
        case _:
            assert False
    assert res > 0
    return res


def get_args_size(args) -> int:
    """Get the size of the provided arguments in bytes."""
    return sum(get_type_size(arg.type) for arg in args)


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

    def align_to(self, alignment: int):
        """Align the stack to the given alignment in bytes"""
        shift_bits = int(math.log2(alignment))
        self.stack_offset = math.floor(self.stack_offset / alignment) * alignment
        self.last_block.add_instr(
            mips_inst.Srl(Reg.sp, Reg.sp, shift_bits),
            mips_inst.Sll(Reg.sp, Reg.sp, shift_bits),
        )

    def load_float(
        self, i: ir.Instruction | tuple[ir.Argument, ir.Function], r: Regf, text: str | mips_inst.Comment = ""
    ) -> mips_inst.Instruction:
        """Load a value from an instruction or a constant into the register."""
        assert isinstance(i.type, ir.FloatType)

        if isinstance(i, ir.Constant):  # if loading instruction is a constant
            assert isinstance(i.type, ir.FloatType)
            h = hex(struct.unpack("<I", struct.pack("<f", i.constant))[0])
            return (mips_inst.Li(Reg.t1, h, text), mips_inst.Mtc1(Reg.t1, r))
        elif isinstance(i, ir.Argument):  # if loading instruction is a function argument
            func: ir.Function = self.function
            arg_index: int = func.args.index(i)
            offset = get_args_size(func.args[arg_index:])  # offset is size of argument to load and all following arguments
            return mips_inst.L_s(r, Reg.fp, offset, text)  # lw $r, offset($fp)
        else:  # all other instructions
            return mips_inst.L_s(r, Reg.fp, self.variables[i.name].offset, text)  # lw $r, offset($fp)

    def load_int(
        self, i: ir.Instruction | tuple[ir.Argument, ir.Function], r: Reg, text: str | mips_inst.Comment = ""
    ) -> mips_inst.Instruction:
        """Load a value from an instruction or a constant into the register."""
        assert isinstance(i.type, (ir.IntType, ir.PointerType))

        load_instr = None
        # decide what load instruction to use based on the size of the type
        match get_type_size(i.type):
            case 4:
                load_instr = mips_inst.Lw
            case 2:
                load_instr = mips_inst.Lh
            case 1:
                load_instr = mips_inst.Lb
            case _:
                assert False

        if isinstance(i, ir.Constant):  # if loading instruction is a constant
            return mips_inst.Li(r, i.constant, text)
        elif isinstance(i, ir.Argument):  # if loading instruction is a function argument
            func: ir.Function = self.function
            arg_index: int = func.args.index(i)
            offset = get_args_size(func.args[arg_index:])
            return load_instr(r, Reg.fp, offset, text)  # lw $r, offset($fp)
        else:  # all other instructions
            return load_instr(r, Reg.fp, self.variables[i.name].offset, text)  # lw $r, offset($fp)

    def load_value(
        self, i: ir.Instruction | tuple[ir.Argument, ir.Function], r: Reg | Regf, text: str | mips_inst.Comment = ""
    ) -> mips_inst.Instruction:
        """
        Load an instruction result or constant into the normal/float register.
        For normal registers the size of the type is used to determine the load type.
        Eg. a type of 1 byte uses `lb` instead of `lw`.
        """
        # decide to load float or int based on the register type to load into
        if isinstance(r, Regf):
            return self.load_float(i, r, text)
        return self.load_int(i, r, text)

    def load_address(self, value, r: Reg) -> mips_inst.Instruction:
        """
        Load the address of a pointer into the register.
        """
        # Ensure the value is a variable with an allocated memory space
        assert value.name in self.variables, f"Variable {value.name} not found in allocated variables."

        # Retrieve the variable's offset
        var_offset = self.variables[value.name].offset

        # TODO: add support for function

        # Load the address into the register by adding the variable's offset to the frame pointer
        return mips_inst.Addiu(r, Reg.fp, var_offset, mips_inst.Comment(f"Store address of {value.name}"))

    def store_float(self, r: Regf, offset: int, text: str | mips_inst.Comment = "") -> mips_inst.Instruction:
        """Store a float in register ``r`` at ``offset`` from the frame pointer."""
        return mips_inst.S_s(r, Reg.fp, offset, text)

    def store_int(
        self, i: ir.Instruction, r: Reg, offset: int, text: str | mips_inst.Comment = ""
    ) -> mips_inst.Instruction:
        """Store an int in register ``r`` at ``offset`` from the frame pointer."""
        # decide what store instruction to use based on the size of the type
        match get_type_size(i.type):
            case 4:
                return mips_inst.Sw(r, Reg.fp, offset, text)
            case 2:
                return mips_inst.Sh(r, Reg.fp, offset, text)
            case 1:
                return mips_inst.Sb(r, Reg.fp, offset, text)
        assert False, "unsupported type size"

    def store_value(
        self, i: ir.Instruction, r: Reg | Regf, offset: int, text: str | mips_inst.Comment = ""
    ) -> mips_inst.Instruction:
        """Store content of a normal/float register ``r`` at ``offset`` from the frame pointer."""
        if isinstance(r, Regf):
            return self.store_float(r, offset, text)
        return self.store_int(i, r, offset, text)

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
        """Visit an instruction."""
        print(f"    - {type(instr).__name__}")

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
                self.align_to(instr.align)
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
                block: ir.Block = instr.operands[0]
                assert isinstance(block, ir.Block)
                self.last_block.add_instr(
                    mips_inst.J(Label(f"{self.function.name}.{block.name}"), mips_inst.IrComment(f"{instr}")),
                )

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
                func: ir.Function = instr.operands[0]
                ret_size = get_type_size(func.return_value.type)
                arg_size = get_args_size(func.args)
                tot_size = ret_size + arg_size
                self.align_to(ret_size)
                var = self.variables.new_var(Label(instr.name), self.stack_offset)
                # only increase stack offset by return size to overwrite arguments after call ends
                # in mips the stack pointer is increased by total size and reset before return jump
                self.stack_offset -= ret_size 

                self.last_block.add_instr(
                    
                    # allocate stack space for function and return arguments
                    mips_inst.Addiu(Reg.sp, Reg.sp, -tot_size, mips_inst.IrComment(f"{instr}")),  # addiu $sp, $sp, -(ret_size + arg_size)
                    [
                        (
                            # load argument value into t1 or f0
                            self.load_value(oper, Regf.f0 if isinstance(oper.type, ir.FloatType) else Reg.t1, mips_inst.Comment(f"load arg {i}")),
                            # store argument value on stack. stored at return offset (negative) - return size - argument size up to stored argument
                            self.store_value(
                                oper,
                                Regf.f0 if isinstance(oper.type, ir.FloatType) else Reg.t1,
                                var.offset - ret_size - get_args_size(func.args[:i]),
                                mips_inst.Comment(f"store arg {i}"),
                            ),
                        )
                        for i, oper in enumerate(instr.operands[1:])
                    ],
                    mips_inst.Jal(Label(f"{func.name}.{func.basic_blocks[0].name}")),
                    mips_inst.Blank(),
                )

            case ir_inst.ConditionalBranch():
                condition, true_block, false_block = instr.operands

                self.last_block.add_instr(
                    # Load the condition value into a register
                    self.load_int(condition, Reg.t1),
                    # Branch if the condition is true
                    mips_inst.Bne(
                        Reg.t1,
                        Reg.zero,
                        Label(f"{self.function.name}.{true_block.name}"),
                        mips_inst.Comment(f"{instr} condition true"),
                    ),
                    # Branch to the false block if the condition is zero
                    mips_inst.J(
                        Label(f"{self.function.name}.{false_block.name}"), mips_inst.Comment(f"{instr} condition false")
                    ),
                )

            case ir_inst.Comment():
                self.last_block.add_instr(mips_inst.CComment(instr.text))

            case ir_inst.GEPInstr():
                print("unhandled!")

            # case ir_inst.LoadInstr():
            #     assert len(instr.operands) == 1
            #     # TODO wrong, operand is just the previous step not always alloca
            #     alloc: ir.AllocaInstr = instr.operands[0]
            #     assert isinstance(alloc, (ir.AllocaInstr, ir.GEPInstr, ir.LoadInstr))
            #
            #     size = get_type_size(alloc.operands[0].type)
            #     var = self.variables.new_var(Label(instr.name), self.stack_offset)
            #     self.stack_offset -= size
            #     self.last_block.add_instr(
            #         mips_inst.Addiu(Reg.sp, Reg.sp, -size, mips_inst.IrComment(f"{instr}")),
            #         # load value into reg
            #         mips_inst.Lw(Reg.t1, Reg.fp, self.variables[alloc.name].offset),  # lw $t1, $fp, src
            #         # store value in new variable
            #         mips_inst.Sw(Reg.t1, Reg.fp, var.offset),  # lw $t1, $fp, dest
            #         mips_inst.Blank(),
            #     )

            case ir_inst.LoadInstr():
                assert len(instr.operands) == 1
                operand = instr.operands[0]
                assert isinstance(operand, (ir.AllocaInstr, ir.GEPInstr, ir.LoadInstr))

                # Allocate space for the new variable and store the loaded value
                size = get_type_size(operand.operands[0].type)
                self.align_to(operand.align)
                var = self.variables.new_var(Label(instr.name), self.stack_offset)
                self.stack_offset -= size

                if isinstance(instr.type, ir.PointerType):
                    # address of operand(=var) gets stored in $t1
                    assert not isinstance(instr.type.pointee, (ir.IntType, ir.PointerType)), "only pointers and ints implemented"
                    self.last_block.add_instr(
                        # mips_inst.Lw(
                        #     Reg.t1,
                        #     Reg.fp,
                        #     self.variables[operand.name].offset,
                        #     mips_inst.Comment(f"Load {operand.name}  (LoadInstr)"),
                        # ),
                        self.load_int(operand, Reg.t1, mips_inst.Comment(f"Load {operand.name}  (LoadInstr)")),
                        # Dereference the address to get the value
                        mips_inst.Lw(Reg.t1, Reg.t1, 0, mips_inst.Comment(f"Dereference {operand.name}")),
                        # TODO support more than only integer/pointer types
                    )

                # dereference pointer and turn address into value
                # elif isinstance(instr.type, ir.IntType) and isinstance(operand.type, ir.PointerType):
                #     # address of operand(=var) gets stored in $t1
                #     # self.last_block.add_instr(
                #     #     mips_inst.Lw(
                #     #         Reg.t1,
                #     #         Reg.fp,
                #     #         self.variables[operand.name].offset,
                #     #         mips_inst.Comment(f"Load {operand.name}  (LoadInstr)"),
                #     #     ),
                #     #     # Dereference the address to get the value
                #     #     mips_inst.Lw(Reg.t1, Reg.t1, 0, mips_inst.Comment(f"Dereference {operand.name}")),
                #     # )
                #
                #     self.last_block.add_instr(
                #         mips_inst.Lw(
                #             Reg.t1,
                #             Reg.fp,
                #             self.variables[operand.name].offset,
                #             mips_inst.Comment(f"Load value of {operand.name}"),
                #         ),
                #     )

                else:
                    # Load the value directly if not a pointer
                    self.last_block.add_instr(
                        mips_inst.Lw(
                            Reg.t1,
                            Reg.fp,
                            self.variables[operand.name].offset,
                            mips_inst.Comment(f"Load value of {operand.name}"),
                        ),
                    )
                    self.load_value(operand, Regf.f0 if is_float else Reg.t1, mips_inst.Comment(f"Load {operand.name}  (LoadInstr)")),

                self.last_block.add_instr(
                    mips_inst.Addiu(Reg.sp, Reg.sp, -size, mips_inst.IrComment(f"{instr}")),
                    mips_inst.Sw(Reg.t1, Reg.fp, var.offset),  # Store value in new variable
                    mips_inst.Blank(),
                )

            case ir_inst.Ret():
                assert len(instr.operands) == 1  # ? likely wrong for structs
                ret_val: ir.Instruction = instr.operands[0]
                ret_size = get_type_size(ret_val.type) # TODO unused
                arg_size = get_args_size(self.function.args)
                tot_size = arg_size + ret_size

                is_float = isinstance(ret_val.type, ir.FloatType)

                self.last_block.add_instr(
                    mips_inst.Comment("clean up stack frame"),
                    # load return value and store it at return address on the stack
                    self.load_value(ret_val, Regf.f0 if is_float else Reg.t1, mips_inst.IrComment(f"{instr}")),
                    # mips_inst.Sw(Reg.t1, Reg.fp, tot_size),  # sw $t1, $fp, 4
                    self.store_value(ret_val, Regf.f0 if is_float else Reg.t1, tot_size),
                    # self.copy_data(Reg.fp, self.variables[ret_val.name].offset, Reg.fp, tot_size, ret_size),
                    # restore return register
                    mips_inst.Lw(Reg.ra, Reg.fp, -4),  # lw  $ra, -4($fp)
                    # restore stack pointer to start of frame
                    mips_inst.Move(Reg.sp, Reg.fp),  # move    $sp, $fp
                    # restore previous frame pointer
                    mips_inst.Lw(Reg.fp, Reg.sp),  # lw  $fp, 0($sp)
                    # reset stack by size of arguments
                    mips_inst.Addiu(Reg.sp, Reg.sp, arg_size),  # reset stack pointer to "deallocate" arguments
                    # jump back to caller
                    mips_inst.Jr(Reg.ra),  # jr  $ra
                    mips_inst.Blank(),
                )

            case ir_inst.StoreInstr():
                self.handle_store(instr)

            case ir_inst.SwitchInstr():
                print("unhandled!")

            case ir_inst.ICMPInstr():
                self.handleICMP(instr)

            case ir_inst.FCMPInstr():
                self.handle_fcmp(instr)

            case ir_inst.CompareInstr():
                print("unhandled!")

            case ir_inst.CastInstr():
                self.handle_cast(instr)

            case ir_inst.Instruction():
                assert_type(instr, "Instruction")
                self.handle_instruction(instr)

            case _:
                raise ValueError(f"Unsupported type: '{type(instr).__name__}'")

    def handle_store(self, instr: ir_inst.StoreInstr):
        assert len(instr.operands) == 2
        value: ir.Instruction = instr.operands[0]
        "value to be stored"

        gen: ir.AllocaInstr = instr.operands[1]
        "instruction that allocated the value space (expect alloca or gep)"

        assert isinstance(gen, (ir.AllocaInstr, ir.GEPInstr, ir.LoadInstr))
        assert len(instr.operands) == 2

        is_float = isinstance(value.type, ir.FloatType)
        # Check if the value to be stored is a pointer
        if isinstance(value.type, ir.PointerType):
            # If value is a pointer, load the address it points to into the register
            self.last_block.add_instr(self.load_address(value, Reg.t1))

        # Check if the value to be stored is not a pointer and gen is a load instruction
        elif isinstance(gen, ir.LoadInstr):
            assert isinstance(value, ir.Constant), "Expected 'value' to be an ir.Constant"

            if isinstance(gen.type, ir.PointerType):
                # Undo the dereference of the pointer

                self.last_block.add_instr(
                    mips_inst.Lw(
                        Reg.t1,
                        Reg.fp,
                        self.variables[gen.operands[0].name].offset,
                        mips_inst.Comment(f"Load {gen.operands[0].name} (StoreInstr) undo dereference"),
                    ),
                    # load constant value into $t2
                    mips_inst.Li(Reg.t2, value.constant, mips_inst.Comment(f"Load constant {value.constant} into $t1")),
                    mips_inst.Sw(
                        Reg.t2,
                        Reg.t1,
                        0,
                        mips_inst.Comment("Store value from $t2 into address of $t1"),
                    ),
                    mips_inst.Blank(),
                )

            else:
                self.last_block.add_instr(
                    # load variable of load instruction(e.g. %0) into $t1
                    mips_inst.Lw(
                        Reg.t1,
                        Reg.fp,
                        self.variables[gen.name].offset,
                        mips_inst.Comment(f"Load {gen.name} (StoreInstr)"),
                    ),
                    # load constant value into $t2
                    mips_inst.Li(Reg.t2, value.constant, mips_inst.Comment(f"Load constant {value.constant} into $t1")),
                    mips_inst.Sw(
                        Reg.t2,
                        Reg.t1,
                        0,
                        mips_inst.Comment("Store value from $t2 into address of $t1"),
                    ),
                    mips_inst.Blank(),
                )

        else:
            # If value is not a pointer, load the value itself into the register
            self.last_block.add_instr(self.load_value(value, Reg.t1))

        # create store value
        # self.last_block.add_instr(
        #     self.load_value(value, Regf.f0 if is_float else Reg.t1, mips_inst.IrComment(f"{instr}"))
        # )

        # store created value
        if not isinstance(gen, ir.LoadInstr):
            assert gen.name in self.variables
            var = self.variables[gen.name]
            self.last_block.add_instr(
                self.store_value(value, Regf.f0 if is_float else Reg.t1, var.offset),
                mips_inst.Blank(),
            )

    def handle_fcmp(self, instr: ir_inst.FCMPInstr):
        assert len(instr.operands) == 2

        value1: ir.Instruction = instr.operands[0]
        value2: ir.Instruction = instr.operands[1]

        size = get_type_size(instr.type)
        self.align_to(size)
        var = self.variables.new_var(Label(instr.name), self.stack_offset)
        self.stack_offset -= size

        branch_true_label = Label(f"{self.function.name}.{self.basic_block.name}.{instr.name}.true")
        branch_false_label = Label(f"{self.function.name}.{self.basic_block.name}.{instr.name}.false")
        branch_end_label = Label(f"{self.function.name}.{self.basic_block.name}.{instr.name}.end")

        self.last_block.add_instr(
            mips_inst.Addiu(Reg.sp, Reg.sp, -size, mips_inst.IrComment(f"{instr}")),
            self.load_float(value1, Regf.f0),
            self.load_float(value2, Regf.f2),
        )

        match instr.op:
            case "false":
                self.last_block.add_instr(mips_inst.J(branch_false_label))
            case "ueq":
                self.last_block.add_instr(
                    mips_inst.C_eq_s(Regf.f0, Regf.f2),
                    mips_inst.Bc1t(branch_true_label),
                    mips_inst.Bc1f(branch_false_label),
                )
            case "ugt":
                self.last_block.add_instr(
                    mips_inst.C_le_s(Regf.f0, Regf.f2),
                    mips_inst.Bc1t(branch_false_label),
                    mips_inst.Bc1f(branch_true_label),
                )
            case "uge":
                self.last_block.add_instr(
                    mips_inst.C_lt_s(Regf.f0, Regf.f2),
                    mips_inst.Bc1t(branch_false_label),
                    mips_inst.Bc1f(branch_true_label),
                )
            case "ult":
                self.last_block.add_instr(
                    mips_inst.C_lt_s(Regf.f0, Regf.f2),
                    mips_inst.Bc1t(branch_true_label),
                    mips_inst.Bc1f(branch_false_label),
                )
            case "ule":
                self.last_block.add_instr(
                    mips_inst.C_le_s(Regf.f0, Regf.f2),
                    mips_inst.Bc1t(branch_true_label),
                    mips_inst.Bc1f(branch_false_label),
                )
            case "une":
                self.last_block.add_instr(
                    mips_inst.C_eq_s(Regf.f0, Regf.f2),
                    mips_inst.Bc1t(branch_false_label),
                    mips_inst.Bc1f(branch_true_label),
                )
            case "true":
                self.last_block.add_instr(mips_inst.J(branch_true_label))
            case "oeq" | "ogt" | "oge" | "olt" | "ole" | "one" | "ord" | "uno":
                print("unhandled: ", instr.op)
                assert False
            case _:
                assert False

        self.tree.add_block(LabeledBlock(branch_true_label))
        self.last_block.add_instr(
            mips_inst.Li(Reg.t1, 1, mips_inst.Comment(f"branch if true")),
            mips_inst.J(branch_end_label),
        )
        self.tree.add_block(LabeledBlock(branch_false_label))
        self.last_block.add_instr(
            mips_inst.Li(Reg.t1, 0, mips_inst.Comment(f"branch if false")),
            mips_inst.J(branch_end_label),
        )
        self.tree.add_block(LabeledBlock(branch_end_label))
        self.last_block.add_instr(self.store_value(instr, Reg.t1, var.offset))

    def handle_cast(self, instr: ir_inst.CastInstr):
        assert len(instr.operands) == 1

        size = get_type_size(instr.type)
        self.align_to(size)
        var = self.variables.new_var(Label(instr.name), self.stack_offset)
        self.stack_offset -= size

        value = instr.operands[0]

        is_float = isinstance(value.type, ir.FloatType)
        "whether the result is a float"

        self.last_block.add_instr(
            mips_inst.Addiu(Reg.sp, Reg.sp, -size, mips_inst.IrComment(f"{instr}")),  # addiu $sp, $sp, -size
        )

        match instr.opname:
            case "trunc":
                assert not is_float
                self.last_block.add_instr(
                    self.load_int(value, Reg.t1),
                    self.store_int(instr, Reg.t1, var.offset),
                )
            case "zext":
                assert not is_float
                self.last_block.add_instr(
                    self.load_int(value, Reg.t1),
                    self.store_int(instr, Reg.t1, var.offset),
                )
            case "sext":
                assert not is_float
                print("unhandled: sext")
            case "fptosi":
                assert is_float
                self.last_block.add_instr(
                    self.load_float(value, Regf.f0),
                    mips_inst.Cvt_w_s(Regf.f0, Regf.f0),
                    mips_inst.Mfc1(Reg.t1, Regf.f0),
                    self.store_int(value, Reg.t1, var.offset),
                )
            case "sitofp":
                assert not is_float
                self.last_block.add_instr(
                    self.load_int(value, Reg.t1),
                    mips_inst.Mtc1(Reg.t1, Regf.f0),
                    mips_inst.Cvt_s_w(Regf.f0, Regf.f0),
                    self.store_float(Regf.f0, var.offset),
                )
            case "ptrtoint":
                print("unhandled: ptrtoint")
            case "inttoptr":
                print("unhandled: inttoptr")
            case "bitcast":
                print("unhandled: bitcast")
            case "addrspacecast":
                print("unhandled: addrspacecast")

            case "fptoui":
                print("no mips support: unhandled: fptoui")
                assert False
            case "uitofp":
                print("no mips support: unhandled: uitofp")
                assert False
            case "fptrunc":
                print("only float support: unhandled: fptrunc")
                assert False
            case "fpext":
                print("only float support: unhandled: fpext")
                assert False
            case _:
                raise ValueError(f"Unsupported cast operation: '{instr.opname}'")

        self.last_block.add_instr(mips_inst.Blank())

    def handle_instruction(self, instr: ir.Instruction):
        assert 0 < len(instr.operands) <= 2

        size = get_type_size(instr.type)
        self.align_to(size)
        var = self.variables.new_var(Label(instr.name), self.stack_offset)
        self.stack_offset -= size

        is_float = isinstance(instr.type, ir.FloatType)

        self.last_block.add_instr(
            mips_inst.Addiu(Reg.sp, Reg.sp, -size, mips_inst.IrComment(f"{instr}")),  # addiu $sp, $sp, -size
            self.load_value(instr.operands[0], Regf.f0 if is_float else Reg.t1),
            (self.load_value(instr.operands[1], Regf.f2 if is_float else Reg.t2) if len(instr.operands) == 2 else ()),
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
                self.last_block.add_instr(mips_inst.And(Reg.t1, Reg.t1, Reg.t2), mips_inst.Comment("and"))
            case "or":
                self.last_block.add_instr(mips_inst.Or(Reg.t1, Reg.t1, Reg.t2), mips_inst.Comment("or"))
            case "xor":
                self.last_block.add_instr(mips_inst.Xor(Reg.t1, Reg.t1, Reg.t2), mips_inst.Comment("xor"))
            case "shl":
                self.last_block.add_instr(
                    mips_inst.Sll(Reg.t1, Reg.t1, instr.operands[1].constant, mips_inst.Comment("Shl")),
                )
            case "ashr":
                self.last_block.add_instr(
                    mips_inst.Srl(Reg.t1, Reg.t1, instr.operands[1].constant, mips_inst.Comment("Slr")),
                )
            case "fadd":
                self.last_block.add_instr(mips_inst.Add_s(Regf.f0, Regf.f0, Regf.f2))
            case "fsub":
                self.last_block.add_instr(mips_inst.Sub_s(Regf.f0, Regf.f0, Regf.f2, "fsub"))
            case "fmul":
                self.last_block.add_instr(mips_inst.Mul_s(Regf.f0, Regf.f0, Regf.f2))
            case "fdiv":
                self.last_block.add_instr(mips_inst.Div_s(Regf.f0, Regf.f0, Regf.f2))
            case "fneg" if is_float:
                self.last_block.add_instr(mips_inst.Neg_s(Regf.f0, Regf.f0))
            case _:
                print(f"Unhandled instruction: '{instr.opname}'")

        self.last_block.add_instr(
            self.store_value(instr, Regf.f0 if is_float else Reg.t1, var.offset),
            mips_inst.Blank(),
        )

    def handle_icmp(self, instr: ir_inst.ICMPInstr):
        """
        Performs integer comparison
        """

        assert len(instr.operands) == 2

        size: int = get_type_size(instr.type)  # TODO allow for arrays
        self.align_to(size)
        var = self.variables.new_var(Label(instr.name), self.stack_offset)
        self.stack_offset -= size

        self.last_block.add_instr(
            self.load_int(instr.operands[0], Reg.t1, mips_inst.IrComment(f"{instr}")),
            self.load_int(instr.operands[1], Reg.t2),
        )

        match instr.op:
            case "eq":
                print("\t\t -eq")
                self.last_block.add_instr(mips_inst.Seq(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp eq")))
            case "ne":
                print("\t\t ne")
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
                print("\t\t slt")
                self.last_block.add_instr(mips_inst.Slt(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp slt")))
            case "sle":
                print("unhandled : sle")
            case _:
                raise ValueError(f"Unsupported icmp operation: '{instr.op}'")

        self.last_block.add_instr(
            self.store_int(instr, Reg.t1, var.offset),
            # mips_inst.Sw(Reg.t1, Reg.fp, var.offset),
            mips_inst.Addiu(Reg.sp, Reg.sp, -size),
            mips_inst.Blank(),
        )
