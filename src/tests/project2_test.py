import os.path

import pytest
from src.main.main import *
from pathlib import Path
from src.parser.listener.error_listener import MyErrorListener
from src.parser.visitor.CST_visitor.visualization_visitor import *


pass_tests = Path("../../example_source_files").glob('proj2_*_pass_*.c')
syntaxErr_tests = Path("../../example_source_files").glob('proj2_*_syntaxErr_*.c')
semanticErr_tests = Path("../../example_source_files").glob('proj2_*_semanticErr_*.c')

def compile(path, cfold: bool = True):
    path_in_str = str(path)
    tokens = getTokens(path_in_str)
    parser = C_GrammarParser(tokens)
    parser.addErrorListener(MyErrorListener())
    tree = parser.program()
    visualizeCST(tree, parser.ruleNames, "cst-viz/"+str(os.path.basename(path)))
    ast = getAST(tree)
    if cfold:
        applyConstantFolding(ast)
    SymbolTableVisitor(ast)
    visualizeAST(ast, "ast-viz/" + str(os.path.basename(path)) + ".gv")
    return ast

def test_pass():
    failed = False
    for path in pass_tests:
        try:
            compile(path)
            print(f"\n✔ {str(os.path.basename(path))} passed", end='')
        except Exception as e:
            print(f"\nX {e} for {str(os.path.basename(path))}", end='')
            failed = True
    if failed:
        pytest.fail("Expected to have no errors")

def test_syntaxErr():
    failed = False
    for path in syntaxErr_tests:
        try:
            compile(path)
        except SyntaxError as e:
            print(f"\n✔ {e} for {str(os.path.basename(path))}", end='')
            continue
        print(f"\nX Expected to have a syntax error for {str(os.path.basename(path))}", end='')
        failed = True
    if failed:
        pytest.fail("Expected to have syntax error")

def test_semanticErr():
    failed = False
    for path in semanticErr_tests:
        try:
            compile(path)
        except SemanticError as e:
            print(f"\n✔ {e} for {str(os.path.basename(path))}", end='')
            continue
        print(f"\nX Expected to have a semantic error for {str(os.path.basename(path))}", end='')
        failed = True
    if failed:
        pytest.fail("Expected to have semantic errors for a test")


