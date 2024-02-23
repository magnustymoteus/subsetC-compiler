import os.path

import pytest
from src.main.main import *
from pathlib import Path
from src.main.listener.error_listener import MyErrorListener


pass_tests = Path("../../example_source_files").glob('proj1_*_pass_*.c')
syntaxErr_tests = Path("../../example_source_files").glob('proj1_*_syntaxErr_*.c')

def compile(path: str):
    tokens = getTokens(path)
    parser = C_ExpressionsParser(tokens)
    parser.addErrorListener(MyErrorListener())
    tree = parser.program()
    ast = getAST(tree)
    applyConstantFolding(ast)
    return ast
def test_pass():
    for path in pass_tests:
        path_in_str = str(path)
        try:
            result = compile(path_in_str)
            visualizeAST(result, os.path.basename(path)+".gv")
        except Exception as e:
            pytest.fail(e)

def test_syntaxErr():
    for path in syntaxErr_tests:
        path_in_str = str(path)
        try:
            result = compile(path_in_str)
        except SyntaxError:
            return
        pytest.fail("Expected to have syntax error")


