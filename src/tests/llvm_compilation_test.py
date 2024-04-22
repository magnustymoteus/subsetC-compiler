import os.path

import pytest
from src.__main__ import *
from llvmlite import binding

def compile(path, cfold: bool = True, cprop: bool = True):
    path_in_str = str(path)
    preprocessed_code = getPreprocessedCode(path_in_str)
    # Lexes the input file
    tokens = getTokens(preprocessed_code)
    parser = C_GrammarParser(tokens)
    parser.addErrorListener(MyErrorListener())
    tree = parser.program()
    #visualizeCST(tree, parser.ruleNames, "./viz/cst/"+str(os.path.basename(path)))
    ast = getAST(tree, tokens)
    ResolverVisitor(ast)
    #visualizeAST(ast, "./viz/ast/ast-viz/" + str(os.path.basename(path)) + ".gv")
    SymbolTableVisitor(ast)
    #visualizeAST(ast, "./viz/ast/symtab-ast/" + str(os.path.basename(path)) + ".gv")
    TypeCheckerVisitor(ast)
    #visualizeAST(ast, "viz/ast/type-checked-ast/" + str(os.path.basename(path)) + ".gv")
    SimplifierVisitor(ast)
    if cprop:
        ConstantPropagationVisitor(ast)
        #visualizeAST(ast, "viz/ast/cpropped-ast/" + str(os.path.basename(path)) + ".gv")
    if cfold:
        ConstantFoldingVisitor(ast)
    DeadCodeVisitor(ast)
    #visualizeAST(ast, "viz/ast/optimized-ast/" + str(os.path.basename(path)) + ".gv")
    cfg: ControlFlowGraph = BasicBlockVisitor(ast).cfg
    TACVisitor(cfg)
    #visualizeCFG(cfg, "viz/cfg/tac-cfg/" + str(os.path.basename(path)) + ".gv")
    llvm = LLVMVisitor(ast, os.path.basename(path))
    for function in llvm.module.functions:
        if function.name == 'main':
            s = graphviz.Source(binding.get_function_cfg(function), filename=f"./{str(os.path.basename(path))}/viz/llvm_cfg.gv")
            s.save()
    llvm_file = Path(f"./{str(os.path.basename(path))}/llvm.ll")
    llvm_file.parent.mkdir(parents=True, exist_ok=True)
    f = open(f"./{str(os.path.basename(path))}/llvm.ll", "w")
    f.write(str(llvm.module))
    f.close()
    return ast
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
