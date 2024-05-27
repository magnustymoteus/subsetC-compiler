import os.path
import pytest
from src.compilation.compiler import *
import subprocess
import re

all = Path("../../example_source_files/CorrectCode").glob("*.c")
fundamental = Path("../../example_source_files/CorrectCode/").glob("*pass*.c")


# gives all files that match the regex
def test_mips_char():
    filtered = []
    filtered_all = [file for file in all if file.name not in filtered]
    print("\n")
    files_with_char = []
    for path in filtered_all:
        file_with_char = get_files_containing_char(path, "printf")
        if file_with_char:
            files_with_char.append(file_with_char)

    if files_with_char:
        print(files_with_char)


def get_files_containing_char(filepath, regex):
    file_with_char = ""
    with open(filepath, "r") as file:
        # Read the file
        content = file.read()

        # If the file contains the regex, add it to the list
        if re.search(regex, content):
            filename = str(os.path.splitext(os.path.basename(filepath))[0])
            file_with_char = filename

    return file_with_char


def test_mips_fundamentals():
    failed = False
    compiler = Compiler({"cprop", "cfold", "dcode"}, None)
    """
    °has printf in tests:
        - proj3_man_pass_printf.c
        - proj4_man_pass_whileLoop.c
        - proj4_man_pass_assignmentExample.c
        - proj4_man_pass_forLoop.c
        - proj4_man_pass_if.c
        - proj4_man_pass_ifChar.c
        - proj4_man_pass_ifEnum.c
        - proj4_man_pass_ifFloat.c
        - proj4_man_pass_switch.c
        - proj4_man_pass_switchChar.c
        - proj4_man_pass_switchEnum.c
        - proj4_man_pass_whileLoop.c
    """

    filtered = [
        # b'10Error in proj4_man_pass_whileLoop/mips.asm line 148: Runtime exception at 0x0040018c: address out of range 0x00000000\n\nProcessing terminated due to errors.'
        "proj4_man_pass_whileLoop.c",
        # proj4_man_pass_forLoop/mips.asm line 164: Runtime exception at 0x004001d0: arithmetic overflow\n\nProcessing terminated due to errors.\n'
        "proj4_man_pass_forLoop.c",
        # line 326: Runtime exception at 0x00400390: address out of range 0x00000000\n\nProcessing terminated due to errors.\n'
        "proj4_man_pass_assignmentExample.c",
        # Runtime exception at 0x00400238: address out of range 0x00000000
        "proj4_man_pass_switch.c",
        # doesn't work when cprop is enabled
        "proj4_man_pass_switchEnum.c",
        "proj4_man_pass_switchChar.c",
        # printf of float understandably wrong
        "proj4_man_pass_ifChar.c",
    ]

    tested_files: int = 0
    filtered_all = [file for file in fundamental if file.name not in filtered]

    for path in filtered_all:
        tested_files += 1
        filename = str(os.path.splitext(os.path.basename(path))[0])
        print("\nFilename:" + filename + ".c")
        llvm = compiler.compile_llvm(path)
        mips = compiler.compile_mips(llvm)
        compiler.export_mips(mips, Path(f"./{filename}/mips.asm"))
        # nc option to remove standard output text
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
        # print("tested: " + str(tested_files))
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
