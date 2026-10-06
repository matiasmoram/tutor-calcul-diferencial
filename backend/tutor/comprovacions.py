"""Machine checks of concrete mathematical claims (limits, non-existence of limits, identities) with sympy.

The 'Cert o fals' mode uses them twice: on the generator's counterexamples (a failing check rejects the
statement) and on the concrete claims a student makes in an answer (a failing check lowers the grade).

A check is a small dict written by an LLM in sympy syntax:
    {"tipus": "limit",    "expressio": "(x*(m*x))/(x**2+(m*x)**2)", "variable": "x", "punt": "0", "costat": "ambdos", "valor": "m/(1+m**2)"}
    {"tipus": "no_limit", "expressio": "sin(1/y)", "variable": "y", "punt": "0", "costat": "ambdos", "valor": ""}
    {"tipus": "igualtat", "expressio": "diff(x**2*y, x)", "variable": "", "punt": "", "costat": "ambdos", "valor": "2*x*y"}

The strings come from a model that may have read student text, so they are never eval'ed as Python: only a
whitelist of characters and names reaches sympy's parser, with empty builtins. sympy can hang on hard limits, so
`avalua` runs the checks in worker processes under a deadline; a check that times out is "indeterminat".
"""

from __future__ import annotations

import multiprocessing as mp
import random
import re
import time

import sympy as sp
from sympy.parsing.sympy_parser import convert_xor, parse_expr, standard_transformations

Estat = str  # "ok" | "falla" | "indeterminat"
TIPUS = ("limit", "no_limit", "igualtat")
COSTATS = ("ambdos", "dreta", "esquerra")
MAX_LONGITUD = 300

_VARS = "x y z t m n k a b c r s u v w h p q"
SYMBOLS = {name: sp.Symbol(name, real=True) for name in _VARS.split()}
FUNCIONS = {
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "exp": sp.exp, "log": sp.log, "sqrt": sp.sqrt, "Abs": sp.Abs,
    "atan": sp.atan, "asin": sp.asin, "acos": sp.acos, "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh,
    "sign": sp.sign, "Max": sp.Max, "Min": sp.Min, "floor": sp.floor, "diff": sp.diff, "limit": sp.limit,
    "pi": sp.pi, "E": sp.E, "oo": sp.oo,
}
NOMS_PERMESOS = frozenset(SYMBOLS) | frozenset(FUNCIONS)
_CARACTERS = re.compile(r"^[0-9A-Za-z_+\-*/^().,\s]*$")
_PARSER_GLOBALS = {"__builtins__": {}, "Integer": sp.Integer, "Float": sp.Float, "Rational": sp.Rational, "Symbol": sp.Symbol}


class ExpressioInvalida(ValueError):
    pass


def parse(text: str) -> sp.Expr:
    """sympy expression from an untrusted string: whitelisted characters and names only."""
    text = (text or "").strip()
    if not text:
        raise ExpressioInvalida("expressió buida")
    if len(text) > MAX_LONGITUD:
        raise ExpressioInvalida("expressió massa llarga")
    if not _CARACTERS.match(text) or "__" in text:
        raise ExpressioInvalida(f"caràcters no permesos a «{text}»")
    for name in re.findall(r"[A-Za-z_][A-Za-z_0-9]*", text):
        if name not in NOMS_PERMESOS:
            raise ExpressioInvalida(f"nom no permès «{name}» (permesos: {', '.join(sorted(NOMS_PERMESOS))})")
    try:
        return parse_expr(
            text,
            local_dict=dict(SYMBOLS) | FUNCIONS,
            global_dict=dict(_PARSER_GLOBALS),
            transformations=standard_transformations + (convert_xor,),
            evaluate=True,
        )
    except Exception as e:  # sympy raises many types on malformed input
        raise ExpressioInvalida(f"no s'ha pogut interpretar «{text}» ({type(e).__name__})") from e


def _iguals(a, b) -> bool | None:
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


def _dir(costat: str) -> str:
    return {"dreta": "+", "esquerra": "-"}.get(costat, "+-")


def avalua_una(c: dict) -> dict:
    """Evaluates one check in this process. Never raises: problems become 'indeterminat' with a reason."""
    tipus = c.get("tipus")
    try:
        if tipus not in TIPUS:
            raise ExpressioInvalida(f"tipus desconegut «{tipus}»")
        expr = parse(c.get("expressio", ""))
        if tipus == "igualtat":
            valor = parse(c.get("valor", ""))
            r = _iguals(expr, valor)
            if r is None:
                return {"estat": "indeterminat", "calculat": "", "detall": "sympy no ho pot decidir"}
            return {"estat": "ok" if r else "falla", "calculat": str(sp.simplify(expr)), "detall": ""}

        var = c.get("variable", "").strip()
        if var not in SYMBOLS:
            raise ExpressioInvalida(f"variable no vàlida «{var}»")
        punt = parse(c.get("punt", ""))
        direction = _dir(c.get("costat", "ambdos"))
        try:
            lim = sp.limit(expr, SYMBOLS[var], punt, direction)
            existeix = not isinstance(lim, sp.AccumBounds) and not lim.has(sp.AccumBounds, sp.nan) and lim is not sp.zoo
        except ValueError:
            # sympy: "The limit does not exist since left hand limit = a and right hand limit = b"
            lim, existeix = None, False
        except (NotImplementedError, TypeError) as e:
            return {"estat": "indeterminat", "calculat": "", "detall": f"sympy no pot calcular el límit ({type(e).__name__})"}

        if tipus == "no_limit":
            if existeix and lim.is_finite is not False and not lim.has(sp.Limit):
                return {"estat": "falla", "calculat": str(lim), "detall": f"el límit existeix i val {lim}"}
            if lim is not None and lim.has(sp.Limit):
                return {"estat": "indeterminat", "calculat": "", "detall": "sympy no avalua el límit"}
            return {"estat": "ok", "calculat": "no existeix" if lim is None or not existeix else str(lim), "detall": ""}

        # tipus == "limit"
        if lim is None or not existeix:
            return {"estat": "falla", "calculat": "no existeix", "detall": "el límit no existeix"}
        if lim.has(sp.Limit):
            return {"estat": "indeterminat", "calculat": "", "detall": "sympy no avalua el límit"}
        valor = parse(c.get("valor", ""))
        r = _iguals(sp.simplify(lim), valor)
        if r is None:
            return {"estat": "indeterminat", "calculat": str(lim), "detall": "sympy no pot comparar el valor"}
        return {"estat": "ok" if r else "falla", "calculat": str(sp.simplify(lim)), "detall": ""}
    except ExpressioInvalida as e:
        return {"estat": "indeterminat", "calculat": "", "detall": str(e)}
    except Exception as e:  # a sympy bug must not take the request down
        return {"estat": "indeterminat", "calculat": "", "detall": f"error de sympy ({type(e).__name__})"}


def avalua(comprovacions: list[dict], timeout_s: float = 25.0, en_proces: bool = False) -> list[dict]:
    """Evaluates every check, in parallel worker processes under one shared deadline.
    `en_proces=True` runs them inline (tests; no hang protection)."""
    if not comprovacions:
        return []
    if en_proces:
        return [avalua_una(c) for c in comprovacions]
    ctx = mp.get_context("spawn")
    pool = ctx.Pool(processes=min(4, len(comprovacions)))
    try:
        pending = [pool.apply_async(avalua_una, (c,)) for c in comprovacions]
        deadline = time.monotonic() + timeout_s
        out = []
        for p in pending:
            try:
                out.append(p.get(timeout=max(0.05, deadline - time.monotonic())))
            except mp.TimeoutError:
                out.append({"estat": "indeterminat", "calculat": "", "detall": "temps esgotat (sympy)"})
        return out
    finally:
        pool.terminate()  # kills workers stuck in a hard limit


SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["descripcio", "tipus", "expressio", "variable", "punt", "costat", "valor"],
    "properties": {
        "descripcio": {"type": "string", "description": "Què es comprova, en català (p. ex. 'límit sobre la recta y=mx')."},
        "tipus": {"type": "string", "enum": list(TIPUS)},
        "expressio": {"type": "string", "description": "Sintaxi sympy, una sola variable lliure per als límits (substitueix el camí)."},
        "variable": {"type": "string", "description": "Variable del límit; '' per a igualtat."},
        "punt": {"type": "string", "description": "Punt del límit (p. ex. '0', 'oo'); '' per a igualtat."},
        "costat": {"type": "string", "enum": list(COSTATS)},
        "valor": {"type": "string", "description": "Valor esperat (límit o costat dret de la igualtat); '' per a no_limit."},
    },
}

SINTAXI = """Sintaxi de les comprovacions (sympy, cap altra cosa):
- Operadors: + - * / ** (o ^), parèntesis. Multiplicació SEMPRE explícita: 2*x, x*y.
- Variables: x y z t m n k a b c r s u v w h p q (reals). Funcions: sin cos tan exp log sqrt Abs atan asin acos sinh cosh tanh sign Max Min floor diff limit; constants pi E oo.
- "limit": `expressio` ha de dependre d'UNA variable que tendeix al punt (els paràmetres com m poden quedar lliures); per a un camí, substitueix-lo: f(x,y)=x*y/(x**2+y**2) sobre y=m*x és "x*(m*x)/(x**2+(m*x)**2)", variable "x", punt "0", valor "m/(1+m**2)".
- "no_limit": el límit (d'una variable) no existeix: expressio "sin(1/y)", variable "y", punt "0", valor "".
- "igualtat": expressio i valor són iguals com a funcions: expressio "diff(x**2*y, x)", valor "2*x*y" (variable "", punt "").
- No escriguis funcions definides a trossos: comprova cada tros sobre la regió on s'aplica."""
