import os.path
import pytest
from pathlib import Path
from src.compilation.compiler import *
import subprocess


all = Path("../../example_source_files/CorrectCode").glob('[!scanf]*.c')
fundamental = Path("../../example_source_files/CorrectCode/").glob('*pass*.c')


def test_fundamentals():
    failed = False
    compiler = Compiler()
    for path in fundamental:
        filename = str(os.path.splitext(os.path.basename(path))[0])
        module = compiler.compile_llvm(path)
        compiler.export_llvm(module, Path(f"./{filename}/llvm.ll"))
        tested_output = subprocess.check_output(["lli", f"./{filename}/llvm.ll"])
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



def test_all():
    failed = False
    compiler = Compiler(None, {"all"})
    filtered_all = [file for file in all if file.name != 'prime.c']
    for path in filtered_all:
        filename = str(os.path.splitext(os.path.basename(path))[0])
        module = compiler.compile_llvm(path)
        compiler.export_llvm(module, Path(f"./{filename}/llvm.ll"))
        tested_output = subprocess.check_output(["lli", f"./{filename}/llvm.ll"])
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
