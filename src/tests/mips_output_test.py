import os.path
import pytest
from pathlib import Path
from src.compilation.compiler import *
import subprocess

all = Path("../../example_source_files/CorrectCode").glob("*.c")
fundamental = Path("../../example_source_files/CorrectCode/").glob("*pass*.c")


def test_mips_fundamentals():
    failed = False
    compiler = Compiler()
    filtered = ["proj2_man_pass_pointerToPointer2.c"]
    filtered_all = [file for file in fundamental if file.name not in filtered]
    for path in filtered_all:
        filename = str(os.path.splitext(os.path.basename(path))[0])
        print("\nFilename:" + filename + ".c")
        llvm = compiler.compile_llvm(path)
        mips = compiler.compile_mips(llvm)
        compiler.export_mips(mips, Path(f"./{filename}/mips.asm"))
        # nc option to remove
        tested_output = subprocess.check_output(["mars", f"./{filename}/mips.asm", "nc"])
        # remove trailing newline
        tested_output = tested_output[:-1]
        subprocess.run(["gcc", "-std=gnu99", "-w", path])
        reference_output = subprocess.check_output([f"./a.out"])
        success = tested_output == reference_output
        success_str = "✔" if success else "X"
        print(f"{success_str}{path}")
        print(f"expected: {reference_output}")
        print(f"actual: {tested_output}")
        print()
        if not success:
            failed = True
    if failed:
        pytest.fail()


def test_all_mips():
    failed = False
    compiler = Compiler(None, {"all"})
    # filtered = ["prime.c", "fibonacciRecursive.c"]
    # filtered = ["proj2_floatcmp.c", "proj2_man_pass_"]
    filtered = ["comparisons1.c"]
    filtered_all = [file for file in all if file.name not in filtered]
    for path in filtered_all:
        filename = str(os.path.splitext(os.path.basename(path))[0])
        print("\nFilename:" + filename + ".c")
        llvm = compiler.compile_llvm(path)
        mips = compiler.compile_mips(llvm)
        compiler.export_mips(mips, Path(f"./{filename}/mips.asm"))
        # nc option to remove
        tested_output = subprocess.check_output(["mars", f"./{filename}/mips.asm", "nc"])
        # remove trailing newline
        tested_output = tested_output[:-1]
        subprocess.run(["gcc", "-std=gnu99", "-w", path])
        reference_output = subprocess.check_output([f"./a.out"])
        success = tested_output == reference_output
        success_str = "✔" if success else "X"
        print(f"{success_str}{path}")
        print(f"expected: {reference_output}")
        print(f"actual: {tested_output}")
        print()
        if not success:
            failed = True
    if failed:
        pytest.fail()
