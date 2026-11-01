"""Machine checks of concrete mathematical claims (limits, non-existence of limits, identities) with sympy.

The quiz mode uses them twice: on the generator's counterexamples (a failing check rejects the statement) and on
the concrete claims a student makes in an answer (a failing check lowers the grade).

A check is written by an LLM in sympy syntax. Its JSON keys and enum values are Catalan because they are part of
the prompt contract and of the stored quizzes:
    {"tipus": "limit",    "expressio": "(x*(m*x))/(x**2+(m*x)**2)", "variable": "x", "punt": "0", "costat": "ambdos", "valor": "m/(1+m**2)"}
    {"tipus": "no_limit", "expressio": "sin(1/y)", "variable": "y", "punt": "0", "costat": "ambdos", "valor": ""}
    {"tipus": "igualtat", "expressio": "diff(x**2*y, x)", "variable": "", "punt": "", "costat": "ambdos", "valor": "2*x*y"}

The strings come from a model that may have read student text, so they are never eval'ed as Python: only a
whitelist of characters and names reaches sympy's parser, with empty builtins. sympy can hang on hard limits, so
checks run in worker processes under a deadline (`core.shared.math.infra.sympy_pool.SympyCheckPool`); a check that
times out is "indeterminat".
"""

import random
import re
from collections.abc import Mapping
from typing import Literal

import sympy as sp
from pydantic import BaseModel, ConfigDict, Field
from sympy.parsing.sympy_parser import convert_xor, parse_expr, standard_transformations

from core.shared.domain.contract import catalan_alias

CheckKind = Literal["limit", "no_limit", "igualtat"]
Side = Literal["ambdos", "dreta", "esquerra"]
CheckStatus = Literal["ok", "falla", "indeterminat"]

CHECK_KINDS: tuple[CheckKind, ...] = ("limit", "no_limit", "igualtat")
SIDES: tuple[Side, ...] = ("ambdos", "dreta", "esquerra")
MAX_LENGTH = 300

_VARS = "x y z t m n k a b c r s u v w h p q"
SYMBOLS: Mapping[str, sp.Symbol] = {name: sp.Symbol(name, real=True) for name in _VARS.split()}


def _cbrt(a: sp.Expr, evaluate: bool = True) -> sp.Expr:
    """The real cube root (sympy's a**(1/3) is the complex principal root for a < 0). `evaluate` is passed by the
    parser's evaluate=False mode."""
    return sp.Mul(
        sp.sign(a, evaluate=evaluate),
        sp.Pow(sp.Abs(a, evaluate=evaluate), sp.Rational(1, 3), evaluate=evaluate),
        evaluate=evaluate,
    )


FUNCTIONS: Mapping[str, object] = {
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "exp": sp.exp, "log": sp.log, "sqrt": sp.sqrt, "Abs": sp.Abs,
    "atan": sp.atan, "asin": sp.asin, "acos": sp.acos, "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh,
    "sign": sp.sign, "Max": sp.Max, "Min": sp.Min, "floor": sp.floor, "diff": sp.diff, "limit": sp.limit,
    "cbrt": _cbrt,
    "pi": sp.pi, "E": sp.E, "oo": sp.oo,
}  # fmt: skip
ALLOWED_NAMES = frozenset(SYMBOLS) | frozenset(FUNCTIONS)
_CHARACTERS = re.compile(r"^[0-9A-Za-z_+\-*/^().,\s]*$")
_PARSER_GLOBALS: Mapping[str, object] = {
    "__builtins__": {}, "Integer": sp.Integer, "Float": sp.Float, "Rational": sp.Rational, "Symbol": sp.Symbol,
    "Add": sp.Add, "Mul": sp.Mul, "Pow": sp.Pow,  # used by the evaluate=False transformation
}  # fmt: skip


class InvalidExpression(ValueError):
    pass


class MathCheck(BaseModel):
    """Validated from the model's Catalan keys; serialized back to them (`serialize_by_alias`)."""

    model_config = ConfigDict(serialize_by_alias=True)

    description: str = Field(
        default="", validation_alias=catalan_alias("descripcio", "description"), serialization_alias="descripcio"
    )
    kind: str = Field(
        validation_alias=catalan_alias("tipus", "kind"), serialization_alias="tipus"
    )  # unknown kind -> "indeterminat"
    expression: str = Field(
        default="", validation_alias=catalan_alias("expressio", "expression"), serialization_alias="expressio"
    )
    variable: str = ""
    point: str = Field(default="", validation_alias=catalan_alias("punt", "point"), serialization_alias="punt")
    side: str = Field(default="ambdos", validation_alias=catalan_alias("costat", "side"), serialization_alias="costat")
    value: str = Field(default="", validation_alias=catalan_alias("valor", "value"), serialization_alias="valor")


class CheckResult(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    status: CheckStatus = Field(validation_alias=catalan_alias("estat", "status"), serialization_alias="estat")
    computed: str = Field(
        default="", validation_alias=catalan_alias("calculat", "computed"), serialization_alias="calculat"
    )
    detail: str = Field(default="", validation_alias=catalan_alias("detall", "detail"), serialization_alias="detall")


def parse(text: str, evaluate: bool = True) -> sp.Expr:
    """sympy expression from an untrusted string: whitelisted characters and names only. `evaluate=False` only builds
    the tree (cheap and bounded: safe outside a worker); `True` also computes it (`9**9**9**9`, `limit(...)`)."""
    text = (text or "").strip()
    if not text:
        raise InvalidExpression("expressió buida")
    if len(text) > MAX_LENGTH:
        raise InvalidExpression("expressió massa llarga")
    if not _CHARACTERS.match(text) or "__" in text:
        raise InvalidExpression(f"caràcters no permesos a «{text}»")
    for name in re.findall(r"[A-Za-z_][A-Za-z_0-9]*", text):
        if name not in ALLOWED_NAMES:
            raise InvalidExpression(f"nom no permès «{name}» (permesos: {', '.join(sorted(ALLOWED_NAMES))})")
    try:
        return parse_expr(
            text,
            local_dict=dict(SYMBOLS) | dict(FUNCTIONS),
            global_dict=dict(_PARSER_GLOBALS),
            transformations=(*standard_transformations, convert_xor),
            evaluate=evaluate,
        )
    except Exception as e:  # sympy raises many types on malformed input
        raise InvalidExpression(f"no s'ha pogut interpretar «{text}» ({type(e).__name__})") from e


def equal(a: sp.Expr, b: sp.Expr) -> bool | None:
    """True/False when decidable; None when sympy cannot tell."""
    if a == b:
        return True
    if a.has(sp.oo, -sp.oo, sp.zoo) or b.has(sp.oo, -sp.oo, sp.zoo):
        return False
    try:
        d = sp.simplify(a - b)
    except Exception:
        d = None
    if d == 0:
        return True
    # Numeric fallback at random points: simplify misses many identities (abs, roots, trig).
    free = sorted((a - b).free_symbols, key=str)
    rng = random.Random(0)
    try:
        for _ in range(6):
            point = {s: sp.Rational(rng.randint(-29, 29) or 7, rng.randint(3, 11)) for s in free}
            va, vb = complex(a.subs(point).evalf()), complex(b.subs(point).evalf())
            if abs(va - vb) > 1e-9 * max(1.0, abs(va), abs(vb)):
                return False
        return True
    except (TypeError, ValueError, ZeroDivisionError):
        return None if d is None else False


def _direction(side: str) -> str:
    return {"dreta": "+", "esquerra": "-"}.get(side, "+-")


def _undecided(detail: str, computed: str = "") -> CheckResult:
    return CheckResult(status="indeterminat", computed=computed, detail=detail)


def evaluate_one(check: MathCheck) -> CheckResult:
    """Evaluates one check in this process. Never raises: problems become 'indeterminat' with a reason."""
    try:
        if check.kind not in CHECK_KINDS:
            raise InvalidExpression(f"tipus desconegut «{check.kind}»")
        expr = parse(check.expression)
        if check.kind == "igualtat":
            r = equal(expr, parse(check.value))
            if r is None:
                return _undecided("sympy no ho pot decidir")
            return CheckResult(status="ok" if r else "falla", computed=str(sp.simplify(expr)))

        var = check.variable.strip()
        if var not in SYMBOLS:
            raise InvalidExpression(f"variable no vàlida «{var}»")
        point = parse(check.point)
        try:
            lim = sp.limit(expr, SYMBOLS[var], point, _direction(check.side))
            exists = not isinstance(lim, sp.AccumBounds) and not lim.has(sp.AccumBounds, sp.nan) and lim is not sp.zoo
        except ValueError:
            # sympy: "The limit does not exist since left hand limit = a and right hand limit = b"
            lim, exists = None, False
        except (NotImplementedError, TypeError) as e:
            return _undecided(f"sympy no pot calcular el límit ({type(e).__name__})")

        if check.kind == "no_limit":
            if exists and lim is not None and lim.is_finite is not False and not lim.has(sp.Limit):
                return CheckResult(status="falla", computed=str(lim), detail=f"el límit existeix i val {lim}")
            if lim is not None and lim.has(sp.Limit):
                return _undecided("sympy no avalua el límit")
            return CheckResult(status="ok", computed="no existeix" if lim is None or not exists else str(lim))

        if lim is None or not exists:
            return CheckResult(status="falla", computed="no existeix", detail="el límit no existeix")
        if lim.has(sp.Limit):
            return _undecided("sympy no avalua el límit")
        r = equal(sp.simplify(lim), parse(check.value))
        if r is None:
            return _undecided("sympy no pot comparar el valor", computed=str(lim))
        return CheckResult(status="ok" if r else "falla", computed=str(sp.simplify(lim)))
    except InvalidExpression as e:
        return _undecided(str(e))
    except Exception as e:  # a sympy bug must not take the request down
        return _undecided(f"error de sympy ({type(e).__name__})")


CHECK_SCHEMA: Mapping[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["descripcio", "tipus", "expressio", "variable", "punt", "costat", "valor"],
    "properties": {
        "descripcio": {
            "type": "string",
            "description": "Què es comprova, en català (p. ex. 'límit sobre la recta y=mx').",
        },
        "tipus": {"type": "string", "enum": list(CHECK_KINDS)},
        "expressio": {
            "type": "string",
            "description": "Sintaxi sympy, una sola variable lliure per als límits (substitueix el camí).",
        },
        "variable": {"type": "string", "description": "Variable del límit; '' per a igualtat."},
        "punt": {"type": "string", "description": "Punt del límit (p. ex. '0', 'oo'); '' per a igualtat."},
        "costat": {"type": "string", "enum": list(SIDES)},
        "valor": {
            "type": "string",
            "description": "Valor esperat (límit o costat dret de la igualtat); '' per a no_limit.",
        },
    },
}

CHECK_SYNTAX = """Sintaxi de les comprovacions (sympy, cap altra cosa):
- Operadors: + - * / ** (o ^), parèntesis. Multiplicació SEMPRE explícita: 2*x, x*y.
- Variables: x y z t m n k a b c r s u v w h p q (reals). Funcions: sin cos tan exp log sqrt Abs atan asin acos sinh cosh tanh sign Max Min floor cbrt diff limit; constants pi E oo.
- "limit": `expressio` ha de dependre d'UNA variable que tendeix al punt (els paràmetres com m poden quedar lliures); per a un camí, substitueix-lo: f(x,y)=x*y/(x**2+y**2) sobre y=m*x és "x*(m*x)/(x**2+(m*x)**2)", variable "x", punt "0", valor "m/(1+m**2)".
- "no_limit": el límit (d'una variable) no existeix: expressio "sin(1/y)", variable "y", punt "0", valor "".
- "igualtat": expressio i valor són iguals com a funcions: expressio "diff(x**2*y, x)", valor "2*x*y" (variable "", punt "").
- No escriguis funcions definides a trossos: comprova cada tros sobre la regió on s'aplica."""
