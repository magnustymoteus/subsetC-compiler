from __future__ import annotations

from src.constructs.mips_program.node.label import Label



class BaseVariable():
    label: Label
    "Name of the variable"
    def __init__(self, label: Label) -> None:
        self.label: Label = label
class Variable(BaseVariable):
    """
    MIPS variable
    """

    offset: int
    "Variable stack offset from the start of the frame"

    def __init__(self, label: Label, offset: int) -> None:
        self.offset = offset
        super().__init__(label)
class Global(BaseVariable):
    """
    Mips global variable
    """

    type: str
    "Type of global"

    name: str
    "Name of the variable"

    value: str
    "Value of the variable:"

    def __init__(self,  name: str, type: str, values: list[str]) -> None:
        # we are currently assuming all values are of type 'type' since C only allows homogenous arrays
        self.name: str = name
        self.type: str = type
        self.values: list[str] = values
        super().__init__(Label(name))
    def __str__(self) -> str:
        result = f"{self.name}:\n"
        for value in self.values:
            result += f'\t.{self.type} {value}\n'
        return result

class VariableAlias(Variable):
    """
    Alias to a MIPS variable
    """

    var: Variable
    "Variable being aliased"

    @property
    def offset(self) -> int:
        """Offset hook, returns offset of the aliased variable instead of its own"""
        return self.var.offset
    
    def __init__(self, label: Label, ref: Variable) -> None:
        self.label = label
        self.var = ref


class Variables:
    """
    List of MIPS variables
    """

    vars: dict[str, BaseVariable]

    def __init__(self) -> None:
        self.vars: BaseVariable = {}
        self.globs: Global = {}

    def __contains__(self, var: BaseVariable | str) -> bool:
        result = self.vars.get(var if isinstance(var, str) else var.label.label) is not None
        if not result:
            return self.globs.get(var if isinstance(var, str) else var.label.label, None) is not None
        return result

    def __getitem__(self, var: BaseVariable | str) -> Variable | None:
        result = self.vars.get(var if isinstance(var, str) else var.label.label)
        if result is None:
            return self.globs.get(var if isinstance(var, str) else var.label.label, None)
        return result

    def add_glob(self, var: Global):
        assert var not in self.globs
        self.globs[var.label.label] = var

    def add_var(self, var: BaseVariable):
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
