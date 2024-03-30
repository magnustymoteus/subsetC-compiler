import os.path

import pytest
from pathlib import Path
from src.parser.listener.error_listener import MyErrorListener
from src.parser.visitor.CST_visitor.visualization_visitor import *
from src.parser.optimizations import *
from src.llvm_target import *
from src.__main__ import *

pass_tests = Path("../../example_source_files/CorrectCode").glob('*.c')
syntaxErr_tests = Path("../../example_source_files/SyntaxError").glob('*.c')
semanticErr_tests = Path("../../example_source_files/SemanticError").glob('*.c')


def compile(path, cfold: bool = True, cprop: bool = True):
    path_in_str = str(path)
    tokens = getTokens(path_in_str)
    parser = C_GrammarParser(tokens)
    parser.addErrorListener(MyErrorListener())
    tree = parser.program()
    #visualizeCST(tree, parser.ruleNames, "./viz/cst/"+str(os.path.basename(path)))
    ast = getAST(tree, tokens)
    #visualizeAST(ast, "./viz/ast/ast-viz/" + str(os.path.basename(path)) + ".gv")
    SymbolTableVisitor(ast)
    #visualizeAST(ast, "./viz/ast/symtab-ast/" + str(os.path.basename(path)) + ".gv")
    TypeCheckerVisitor(ast)
    #visualizeAST(ast, "viz/ast/type-checked-ast/" + str(os.path.basename(path)) + ".gv")
    if cprop:
        OptimizationVisitor(ast)
        #visualizeAST(ast, "viz/ast/cpropped-ast/" + str(os.path.basename(path)) + ".gv")
    if cfold:
        applyConstantFolding(ast)
    #visualizeAST(ast, "viz/ast/optimized-ast/" + str(os.path.basename(path)) + ".gv")
    cfg: ControlFlowGraph = BasicBlockVisitor(ast).cfg
    TACVisitor(cfg)
    #visualizeCFG(cfg, "viz/cfg/tac-cfg/" + str(os.path.basename(path)) + ".gv")
    LLVMVisitor(cfg, os.path.basename(path))
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


