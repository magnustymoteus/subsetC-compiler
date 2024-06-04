import os.path
import pytest
from src.compilation.compiler import *
import subprocess
import re


all = Path("../../example_source_files/CorrectCode").glob("*.c")

fundamental = Path("../../example_source_files/CorrectCode/")
regex = re.compile(r"proj[123].*pass.*\.c$")

matching_files = [f for f in fundamental.glob("*.c") if regex.match(f.name)]


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

    filtered = []

    tested_files: int = 0
    filtered_all = [file for file in matching_files if file.name not in filtered]

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
        subprocess.run(["gcc", "-ansi", "-pedantic", path])
        reference_output = subprocess.check_output([f"./a.out"])
        success = tested_output == reference_output
        success_str = "✔" if success else "X"
        print(f"{success_str}{path}")
        print(f"expected: {reference_output}")
        print(f"actual: {tested_output}")
        print("tested: " + str(tested_files))
        print()
        if not success:
            failed = True
    if failed:
        pytest.fail()


def test_all_mips():
    failed = False
    compiler = Compiler({"cprop", "cfold", "dcode"}, None)

    filtered = []

    tested_files: int = 0
    filtered_all = [file for file in all if file.name not in filtered]

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
        subprocess.run(["gcc", "-ansi", "-pedantic", path])
        reference_output = subprocess.check_output([f"./a.out"])
        success = tested_output == reference_output
        success_str = "✔" if success else "X"
        print(f"{success_str}{path}")
        print(f"expected: {reference_output}")
        print(f"actual: {tested_output}")
        print("tested: " + str(tested_files))
        print()
        if not success:
            failed = True
    if failed:
        pytest.fail()
