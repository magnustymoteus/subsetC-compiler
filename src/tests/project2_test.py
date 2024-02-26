import os.path

import pytest
from src.main.main import *
from pathlib import Path
from src.parser.listener.error_listener import MyErrorListener
from src.parser.visitor.CST_visitor.visualization_visitor import *


pass_tests = Path("../../example_source_files").glob('proj2_*_pass_*.c')
syntaxErr_tests = Path("../../example_source_files").glob('proj2_*_syntaxErr_*.c')

def compile(path, cfold: bool):
    path_in_str = str(path)
    tokens = getTokens(path_in_str)
    parser = C_GrammarParser(tokens)
    parser.addErrorListener(MyErrorListener())
    tree = parser.program()

    print(os.path.basename(path))

    visualizeCST(tree, parser.ruleNames, os.path.basename(path))

    ast = getAST(tree)
    if cfold:
        applyConstantFolding(ast)
    return ast
def test_pass():
    for path in pass_tests:
        try:
            result = compile(path, False)
            visualizeAST(result, os.path.basename(path)+".gv")
        except Exception as e:
            pytest.fail("pass test "+ str(path), "failed: "+ e)

def test_syntaxErr():
    for path in syntaxErr_tests:
        try:
            result = compile(path, False)
        except SyntaxError:
            break
        pytest.fail("Expected to have syntax error")


