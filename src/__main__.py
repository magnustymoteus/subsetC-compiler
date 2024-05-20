import argparse
from src.compilation.compiler import *
from llvmlite.ir.module import Module


def c_file(param):
    base, ext = os.path.splitext(param)
    if ext.lower() not in (".c"):
        raise ValueError("File must be a .c file")
    return param


def main(argv):
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        "--disable",
        type=str,
        nargs="*",
        choices=["cfold", "cprop", "comments", "warnings", "dcode"],
        help="Things to disable",
    )

    arg_parser.add_argument(
        "--viz",
        type=str,
        nargs="*",
        choices=["all", "cst", "ast", "cfg", "symtab"],
        help="Things to be visualized",
        default=[],
    )

    arg_parser.add_argument("--path", type=c_file, required=True, help="glob path of the .c file(s) to be compiled")

    arg_parser.add_argument(
        "--targets", choices=["llvm", "mips"], nargs="+", required=True, help="Choose 1 or more languages to compile to"
    )
    args = arg_parser.parse_args(argv[1:])
    # compiler = Compiler(args.disable, args.viz)

    pass_tests = Path.cwd().glob(args.path)

    # MIPS
    """
    error: type 'AllocaInstr' not implemented
    file error occurs: mips_visitor.py
    function error occurs: handlestore
    affected files: proj2_man_pass_pointerToPointer2.c 
                    proj2_man_pass_pointerOperations2.c 
                    proj2_man_pass_pointerConstRessignment.c
                    variables6.c 
                    proj2_man_pass_customPostfixPtr1.c
                    unions.c
                    proj2_man_pass_conversionExplicitTypeCast.c
                    proj2_man_pass_pointerOperations1.c
                    proj2_opt_pass_constPointerToNonConstPointer3.c
                    proj2_man_pass_advancedPointerOperations.c
                    dereferenceAssignment.c
                    proj2_opt_pass_constPointerToNonConstPointer2.c
                    proj3_man_pass_typedef.c (type 'CastInstr' not implemented)
                    proj3_man_pass_typedef.c (type 'CastInstr' not implemented)  
                    proj2_man_pass_conversionImplicit.c (type 'CastInstr' not implemented)  
                    proj2_man_pass_simplePostfix.c (type 'LoadInstr' not implemented)
                    proj2_man_pass_decrement.c (type 'LoadInstr' not implemented)
                    
    """

    """
    error: AttributeError: 'FloatType' object has no attribute 'width'
    file error occurs: mips_visitor.py 
    function error occurs: case ir_inst.CastInstr():
    affected files: printf3.c, binaryOperations1.c, proj4_man_pass_ifChar.c, proj2_man_pass_variableNormal.c
    """

    """
    error: AssertionError, assert isinstance(alloc, ir.AllocaInstr) it is a GEPinstr we get
    file error occurs: mips_visitor.py 
    function error occurs: handle_store
    affected files: variables7.c, variables8.c, proj2_opt_pass_constPointerToNonConstPointer1.c
    """

    """
    error: AssertionError: assert isinstance(alloc, ir.AllocaInstr)
    file error occurs: mips_visitor.py 
    function error occurs: case ir_inst.LoadInstr()
    affected files: pointerArgument.c, 
                    structs.c, 
                    scoping.c (type 'GlobalVariable' not implemented), 
                    variables4.c, 
                    proj2_man_pass_simplePointerOperation.c,
                    proj2_man_pass_pointerToPointer.c
                    
    """

    """
    error: 'NoneType' object has no attribute 'offset'
    file error occurs: mips_visitor.py
    function error occurs: handle_store
    affected files: fibonacciRecursive.c
    """

    """
    error: assert gen.name in self.variables
    file error occurs: mips_visitor.py
    function error occurs: handle_store
    affected files: variables3.c, unaryOperations.c
    """

    # filtered = ['proj2_man_pass_pointerToPointer2.c',
    #             'proj2_man_pass_pointerOperations2.c',
    #             'proj4_man_pass_switchEnum.c',
    #             'variables7.c',
    #             'variables8.c',
    #             'printf3.c',
    #             'pointerArgument.c',
    #             'proj2_man_pass_pointerReassignment.c',
    #             'proj2_man_pass_pointerConstRessignment.c',
    #             'structs.c',
    #             'variables6.c',
    #             'scoping.c',
    #             'proj2_man_pass_customPostfixPtr1.c',
    #             'proj2_man_pass_conversionExplicitTypeCast.c',
    #             'binaryOperations1.c',
    #             'unions.c',
    #             'proj2_man_pass_simplePostfix.c',
    #             'proj2_man_pass_pointerOperations1.c',
    #             'proj2_opt_pass_constPointerToNonConstPointer3.c',
    #             'proj2_man_pass_advancedPointerOperations.c',
    #             'proj2_man_pass_conversionImplicit.c',
    #             'dereferenceAssignment.c',
    #             'proj4_man_pass_ifChar.c',
    #             'fibonacciRecursive.c',
    #             'proj2_opt_pass_constPointerToNonConstPointer2.c',
    #             'variables4.c',
    #             'proj2_man_pass_simplePointerOperation.c',
    #             'variables3.c',
    #             'proj2_man_pass_variableNormal.c',
    #             'unaryOperations.c',
    #             'proj2_man_pass_pointerToPointer.c',
    #             'proj2_opt_pass_constPointerToNonConstPointer1.c',
    #             ]

    filtered = []

    filtered_all = [file for file in pass_tests if file.name not in filtered]
    for path in filtered_all:
        compiler = Compiler(args.disable, args.viz)
        # path_in_str = str(path)
        try:
            module: Module = compiler.compile_llvm(path)
            filename, fileext = os.path.splitext(path)
            for target in args.targets:
                match target:
                    case "llvm":
                        compiler.export_llvm(module, Path(f"{filename}.ll"))
                    case "mips":
                        compiler.export_llvm(module, Path(f"{filename}.ll"))  # TODO remove, temporary for development
                        print(path)
                        mips_program: MipsProgram = compiler.compile_mips(module)
                        compiler.export_mips(mips_program, Path(f"{filename}.asm"))
                    case _:
                        raise ValueError(f"Unrecognized target: {target}")
        except PreprocessingError as e:
            print(f"{e}")
        except SyntaxError as e:
            print(f"{e}")
        except SemanticError as e:
            print(f"{e}")
        except Warning as w:
            if not "warnings" in args.disabled:
                print(f"{w}")


if __name__ == "__main__":
    main(sys.argv)
