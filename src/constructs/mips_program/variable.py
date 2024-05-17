from __future__ import annotations

from src.constructs.mips_program.node.label import Label


class Global:
    """
    Mips global variable
    """

    type: str
    "Type of global"

    name: str
    "Name of the variable"

    def __init__(self, type: str, name: str) -> None:
        self.type = type
        self.name = name


class Variable:
    """
    MIPS variable
    """

    label: Label
    "Name of the variable"

    offset: int
    "Variable stack offset from the start of the frame"

    def __init__(self, label: Label, offset: int) -> None:
        self.label = label
        self.offset = offset

class VariableAlias(Variable):
    """
    Alias to a MIPS variable
    """

    var: Variable
    "Variable being aliased"

    @property
    def offset(self) -> Label:
        """Offset hook, returns offset of the aliased variable instead of its own"""
        return self.var.offset
    
    def __init__(self, label: Label, ref: Variable) -> None:
        self.label = label
        self.var = ref


class Variables:
    """
    List of MIPS variables
    """

    vars: dict[str, Variable]

    def __init__(self) -> None:
        self.vars = {}

    def __contains__(self, var: Variable | str) -> bool:
        return self.vars.get(var if isinstance(var, str) else var.label.label) is not None

    def __getitem__(self, var: Variable | str) -> Variable | None:
        return self.vars.get(var if isinstance(var, str) else var.label.label)

    def add_var(self, var: Variable):
        assert var not in self
        self.vars[var.label.label] = var

    def new_var(self, label: Label, offset: int = 0) -> Variable:
        var = Variable(label, offset)
        self.add_var(var)
        return var

    def new_alias(self, label: Label, ref: Variable) -> VariableAlias:
        var = VariableAlias(label, ref)
        self.add_var(var)
        return var

    def clear(self):
        self.vars.clear()
