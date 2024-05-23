import math
import struct

import llvmlite.ir as ir
import llvmlite.ir.instructions as ir_inst
from src.constructs.mips_program import Global, MipsProgram, Variables
from src.constructs.mips_program.node import Label, LabeledBlock, Reg, Regf
from src.constructs.mips_program.node import instr as mips_inst

from .alloca_mixin import MVHandleAllocaMixin
from .base import assert_type, get_args_size, get_type_size
from .branch_mixin import MVHandleBranchMixin
from .call_mixin import MVHandleCallMixin
from .conditional_branch_mixin import MVHandleConditionalBranchMixin
from .gep_mixin import MVHandleGEPMixin

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


class MipsVisitor(
    ir.Visitor,
    MVHandleAllocaMixin,
    MVHandleBranchMixin,
    MVHandleCallMixin,
    MVHandleConditionalBranchMixin,
    MVHandleGEPMixin,
):
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
            offset = get_args_size(
                func.args[arg_index:]
            )  # offset is size of argument to load and all following arguments
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

    def load_address(self, i: ir.Instruction | tuple[ir.Argument, ir.Function], value, r: Reg) -> mips_inst.Instruction:
        """
        Load the address of a pointer into the register.
        """
        if isinstance(i, ir.Argument):
            func: ir.Function = self.function
            arg_index: int = func.args.index(i)
            offset = get_args_size(func.args[arg_index:])
            return mips_inst.Addiu(r, Reg.fp, offset, mips_inst.Comment(f"Load address of argument {i.name}"))

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
            case 4 | 8:
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
        for glob in module.global_values:
            if isinstance(glob, ir.GlobalVariable):
                self.visit_Global(glob)
            elif isinstance(glob, ir.Function):
                self.visit_Function(glob)
            else:
                print("unhandled glob")

    def get_glob_type(self, glob_initializer, glob_type: ir.Type) -> str:
        if glob_initializer is not None:
            if isinstance(glob_initializer.constant, bytearray):
                return "ascii"
            else:
                match glob_type:
                    case ir.FloatType():
                        return "float"
                    case ir.IntType():
                        return "word" if get_type_size(glob_type) == 4 else "byte"
                    case ir.PointerType():
                        return "space"
                    case ir.ArrayType():
                        return self.get_glob_type(glob_initializer, glob_type.element)
                    case _:
                        assert False
        return "space"

    def get_glob_values(self, initializer, glob_type: ir.Type) -> list[str]:
        match initializer:
            case ir.Constant():
                if isinstance(initializer.constant, bytearray):
                    return [f'"{initializer.constant.decode("utf8").encode("unicode_escape").decode("utf8")}"']
                match initializer.type:
                    case ir.PointerType():
                        if initializer.constant.startswith("getelementptr"):
                            for elem in initializer.constant.split():
                                if elem[0] == "@":
                                    return ["$LC" + elem[2:-2]]
                        return [str(get_type_size(glob_type))]
                    case ir.ArrayType():
                        res = []
                        for element in initializer.constant:
                            res += self.get_glob_values(element, glob_type)
                        return res
                    case _:
                        return [initializer.constant]
            case None:
                return [str(get_type_size(glob_type))]
            case _:
                assert False

    def visit_Global(self, variable: ir.GlobalVariable):
        print(f"- {type(variable).__name__}")
        name = variable.name
        glob_type: str = self.get_glob_type(variable.initializer, variable.type.pointee)
        glob_values: list[str] = self.get_glob_values(variable.initializer, variable.type.pointee)
        # type of glob is string
        if glob_type == "ascii":
            name = "$LC" + name
        # glob value is a GEP to a string
        for glob_value in glob_values:
            if len(str(glob_value)) >= 3 and "$LC" == glob_value[:3]:
                glob_type = "word"
                break
        glob = Global(name, glob_type, glob_values)
        self.tree.data.append(glob)

    def visit_Function(self, func: ir_inst.Function):
        """Visit a function."""
        print(f"- {type(func).__name__}")

        self.variables.clear()
        self.stack_offset = 0
        self.new_function_started = True
        match func.name:
            case "printf":
                pass
            case "scanf":
                pass
            case _:
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
                super().handle_alloca(instr)

            case ir_inst.Branch():
                super().handle_branch(instr)

            case ir_inst.CallInstr():
                super().handle_call(instr)

            case ir_inst.ConditionalBranch():
                super().handle_conditional_branch(instr)

            case ir_inst.Comment():
                self.last_block.add_instr(mips_inst.CComment(instr.text))

            case ir_inst.GEPInstr():
                super().handle_gep(instr)

            case ir_inst.LoadInstr():
                assert len(instr.operands) == 1
                operand = instr.operands[0]
                assert isinstance(operand, (ir.AllocaInstr, ir.GEPInstr, ir.LoadInstr))

                # Allocate space for the new variable and store the loaded value
                size = get_type_size(operand.operands[0].type)
                self.align_to(operand.align)
                var = self.variables.new_var(Label(instr.name), self.stack_offset)
                self.stack_offset -= size

                is_float = isinstance(operand.type, ir.FloatType)

                if isinstance(instr.type, ir.PointerType):
                    # address of operand(=var) gets stored in $t1
                    assert isinstance(
                        instr.type.pointee, (ir.IntType, ir.FloatType, ir.PointerType)
                    ), "only pointers and ints implemented"
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

                else:
                    # Load the value directly if not a pointer
                    self.last_block.add_instr(
                        mips_inst.Lw(
                            Reg.t1,
                            Reg.fp,
                            self.variables[operand.name].offset,
                            mips_inst.Comment(f"Load value of %{operand.name}"),
                        ),
                    )
                    self.load_value(
                        operand, Regf.f0 if is_float else Reg.t1, mips_inst.Comment(f"Load {operand.name}  (LoadInstr)")
                    ),

                self.last_block.add_instr(
                    mips_inst.Addiu(Reg.sp, Reg.sp, -size, mips_inst.IrComment(f"{instr}")),
                    mips_inst.Sw(Reg.t1, Reg.fp, var.offset),  # Store value in new variable
                    mips_inst.Blank(),
                )

            case ir_inst.Ret():
                assert len(instr.operands) == 1  # ? likely wrong for structs
                ret_val: ir.Instruction = instr.operands[0]
                ret_size = get_type_size(ret_val.type)  # TODO unused
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
                self.handle_switch(instr)

            case ir_inst.ICMPInstr():
                self.handle_icmp(instr)

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

        # if it is a gep instruction for pointer arithmetic
        if isinstance(value, ir.GEPInstr):
            # self.last_block.add_instr(
            #     # Load address of the previously stored new address for the pointer
            #     self.load_address(value, value, Reg.t1),
            # )
            mips_inst.Blank(),

            # Check if the value to be stored is a pointer
        elif isinstance(value.type, ir.PointerType):
            # If value is a pointer, load the address it points to into the register
            self.last_block.add_instr(self.load_address(value, value, Reg.t1))

        # Check if the value to be stored is not a pointer and gen is a load instruction
        # special case for e.g.: *y = 500
        elif isinstance(gen, ir.LoadInstr):

            # previous was a load of a pointer
            # e.g: %"1" = load i32, i32* %"0", align 4
            # then an instruction
            # e.g:  %"2" = add i32 %"1", 1
            # then store i32 %"2", i32* %"0", align 4
            # store value of %"2" into address of %"0"
            if isinstance(gen.type, ir.PointerType) and isinstance(value, ir.Instruction):
                # Load the address of the variable pointed to by `gen` into $t1
                self.last_block.add_instr(
                    mips_inst.Lw(
                        Reg.t1,
                        Reg.fp,
                        self.variables[gen.operands[0].name].offset,
                        mips_inst.Comment(f"Load address of {gen.operands[0].name} for storing"),
                    )
                )

                # Assuming `value` is the result of an operation like addition,
                # and it's stored in a temporary variable, load this value into $t2.
                self.last_block.add_instr(
                    mips_inst.Lw(
                        Reg.t2,
                        Reg.fp,
                        self.variables[value.name].offset,
                        mips_inst.Comment(f"Load modified value of {value.name}"),
                    )
                )

                # Store the modified value back into the original address
                self.last_block.add_instr(
                    mips_inst.Sw(
                        Reg.t2,
                        Reg.t1,
                        0,
                        mips_inst.Comment(
                            f"Store modified value of {value.name} into address of {gen.operands[0].name}"
                        ),
                    )
                )

            elif isinstance(gen.type, ir.PointerType) and isinstance(value, ir.Constant):
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
            self.last_block.add_instr(self.load_value(value, Regf.f0 if is_float else Reg.t1))

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
                self.last_block.add_instr(
                    self.load_int(value, Reg.t1),
                    self.store_int(instr, Reg.t1, var.offset),
                )
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
                self.last_block.add_instr(mips_inst.Seq(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp eq")))
            case "ne":
                self.last_block.add_instr(mips_inst.Sne(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp ne")))
            case "ugt":
                self.last_block.add_instr(mips_inst.Sgtu(Reg.t1, Reg.t2, Reg.t1, mips_inst.Comment("icmp ugt")))
            case "uge":
                self.last_block.add_instr(mips_inst.Sgeu(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp uge")))
            case "ult":
                self.last_block.add_instr(mips_inst.Sleu(Reg.t1, Reg.t2, Reg.t1, mips_inst.Comment("icmp ult")))
            case "ule":
                self.last_block.add_instr(mips_inst.Sltu(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp ule")))
            case "sgt":
                self.last_block.add_instr(mips_inst.Sgt(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp sgt")))
            case "sge":
                self.last_block.add_instr(mips_inst.Sge(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp sge")))
            case "slt":
                self.last_block.add_instr(mips_inst.Slt(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp slt")))
            case "sle":
                self.last_block.add_instr(mips_inst.Sle(Reg.t1, Reg.t1, Reg.t2, mips_inst.Comment("icmp sle")))
            case _:
                raise ValueError(f"Unsupported icmp operation: '{instr.op}'")

        self.last_block.add_instr(
            self.store_int(instr, Reg.t1, var.offset),
            # mips_inst.Sw(Reg.t1, Reg.fp, var.offset),
            mips_inst.Addiu(Reg.sp, Reg.sp, -size),
            mips_inst.Blank(),
        )

    def handle_switch(self, instr: ir_inst.SwitchInstr):
        # Load the switch variable value into a register
        assert isinstance(instr.operands[0], ir.LoadInstr)
        self.last_block.add_instr(self.load_value(instr.operands[0], Reg.t0))

        # Placeholder for jump instructions to case labels
        jump_instructions = []

        # Generate labels for each case and compare with the switch variable
        for case_value, case_block in instr.cases:
            case_label = Label(f"{self.function.name}.{case_block.name}")
            # Compare and jump if equal
            jump_instructions.append(
                mips_inst.Beq(Reg.t0, case_value.constant, case_label, mips_inst.Comment(f"Case {case_value}"))
            )

        # Default case
        if instr.default is not None:
            default_label = Label(f"{self.function.name}.{instr.default.name}")
            jump_instructions.append(mips_inst.J(default_label, mips_inst.Comment("Default case")))

        # Add jump instructions to the block
        for jump_instr in jump_instructions:
            self.last_block.add_instr(jump_instr)

        # Add a label at the end of the switch for exiting
        exit_label = Label(f"{self.function.name}.switch.end")
        self.last_block.add_instr(mips_inst.J(exit_label, mips_inst.Comment("Default case")))

        # Note: Actual case and default block instructions should be handled in their respective visit methods
