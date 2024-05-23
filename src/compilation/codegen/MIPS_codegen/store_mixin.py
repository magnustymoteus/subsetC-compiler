import llvmlite.ir as ir
from src.constructs.mips_program.node import instr as mips_inst
from src.compilation.codegen.MIPS_codegen.base import MVBase
from src.constructs.mips_program.node.reg import Reg, Regf


class MVHandleStoreMixin(MVBase):
    def handle_store(self, instr: ir.StoreInstr):
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
