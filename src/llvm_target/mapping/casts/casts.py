from llvmlite.ir import IRBuilder


def get_casts(builder: IRBuilder) -> dict[tuple[str, str], IRBuilder.function]:
    # {("from_type", "to_type"): llvmlite_castfunc}
    casts: dict[tuple[str, str], IRBuilder.function] = {
        ("float", "int"): builder.fptosi,
        ("float", "char"): builder.fptosi,
        ("int", "float"): builder.sitofp,
        ("int", "char"): builder.sext,
        ("char", "float"): builder.sitofp,
        ("char", "int"): builder.sext,
    }
    return casts
