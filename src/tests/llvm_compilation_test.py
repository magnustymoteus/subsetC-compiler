import os.path

import pytest
from src.__main__ import *
from src.compilation.compiler import *

def compile(path):
    compiler = Compiler()
    compiler.compile_llvm(path)
def success(glob_path):
    failed = False
    for path in glob_path:
        try:
            compile(path)
            print(f"\n✔ {str(os.path.basename(path))} passed", end='')
        except Exception as e:
            print(f"\nX {e} for {str(os.path.basename(path))}", end='')
            failed = True
    if failed:
        pytest.fail("Expected to have no errors")

def syntaxErr(glob_path):
    failed = False
    for path in glob_path:
        try:
            compile(path)
        except SyntaxError as e:
            print(f"\n✔ {e} for {str(os.path.basename(path))}", end='')
            continue
        print(f"\nX Expected to have a syntax error for {str(os.path.basename(path))}", end='')
        failed = True
    if failed:
        pytest.fail("Expected to have syntax error")

def semanticErr(glob_path):
    failed = False
    for path in glob_path:
        try:
            compile(path)
        except SemanticError as e:
            print(f"\n✔ {e} for {str(os.path.basename(path))}", end='')
            continue
        except:
            continue
        print(f"\nX Expected to have a semantic error for {str(os.path.basename(path))}", end='')
        failed = True
    if failed:
        pytest.fail("Expected to have semantic errors for a test")

pass_tests_all = Path("../../example_source_files/CorrectCode").glob('*.c')
syntaxErr_tests_all = Path("../../example_source_files/SyntaxError").glob('*.c')
semanticErr_tests_all = Path("../../example_source_files/SemanticError").glob('*.c')

pass_tests_fundamental = Path("../../example_source_files/CorrectCode/").glob('*pass*.c')
syntaxErr_tests_fundamental = Path("../../example_source_files/SyntaxError").glob('*syntaxErr*.c')
semanticErr_tests_fundamental = Path("../../example_source_files/SemanticError").glob('*semanticErr*.c')
def test_pass_fundamentals():
    success(pass_tests_fundamental)
def test_syntaxErr_fundamentals():
    syntaxErr(syntaxErr_tests_fundamental)
def test_semanticErr_fundamentals():
    semanticErr(semanticErr_tests_fundamental)
def test_pass_all():
    success(pass_tests_all)
def test_syntaxErr_all():
    syntaxErr(syntaxErr_tests_all)
def test_semanticErr_all():
    semanticErr(semanticErr_tests_all)
