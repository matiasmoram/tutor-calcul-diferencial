"""Builders for the sympy check tests: checks as the model writes them (Catalan keys)."""

from core.shared.math.sympy_checks import MathCheck


def check(kind: str, expression: str, value: str = "", variable: str = "x", point: str = "0") -> MathCheck:
    # The model writes the Catalan keys: validate from them, as production does.
    return MathCheck.model_validate(
        {"descripcio": "c", "tipus": kind, "expressio": expression, "variable": variable, "punt": point,
         "costat": "ambdos", "valor": value}
    )  # fmt: skip


ITERATED = check("limit", "x*(m*x)/(x**2+(m*x)**2)", "m/(1+m**2)")
