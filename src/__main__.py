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
    compiler = Compiler(args.disable, args.viz)

    pass_tests = Path.cwd().glob(args.path)
    for path in pass_tests:
        path_in_str = str(path)
        try:
            module: Module = compiler.compile_llvm(path)
            filename, fileext = os.path.splitext(path)
            for target in args.targets:
                match target:
                    case "llvm":
                        compiler.export_llvm(module, Path(f"{filename}.ll"))
                    case "mips":
                        compiler.export_llvm(module, Path(f"{filename}.ll"))  # TODO remove, temporary for development
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
