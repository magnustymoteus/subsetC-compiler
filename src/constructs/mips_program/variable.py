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
