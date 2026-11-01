"""The leak check: draft formulas equal by value to a forbidden formula and to no permitted one."""

import re
from functools import lru_cache
from itertools import combinations

import sympy as sp
from sympy.core.function import AppliedUndef

from core.shared.math.latex_cas.equivalence import _compare, _Fingerprint, _fingerprint
from core.shared.math.latex_cas.extraction import formulas, prose_formulas
from core.shared.math.latex_cas.normalise import _normalise
from core.shared.math.latex_cas.parser import _parse_side
from core.shared.math.latex_cas.sides import _sides, _top_level_split

type _Candidate = tuple[str, sp.Basic, _Fingerprint]  # (side text, parsed value, fingerprint)


def is_trivial(e: object) -> bool:
    """Never a leak by itself: single symbols, small integers (|n| <= 2) and their negatives, and notation that
    names a quantity instead of giving it (anything with an undefined function: f(0,0), D_uf(0,0), |f(x,y)|)."""
    if e is None:
        return True
    if isinstance(e, sp.Basic) and e.has(AppliedUndef):
        return True
    if isinstance(e, sp.Mul) and len(e.args) == 2 and e.args[0] == -1:
        e = e.args[1]
    if isinstance(e, sp.Abs):  # |x|, |R_3|
        e = e.args[0]
    if isinstance(e, sp.Symbol) or e in (sp.oo, -sp.oo):  # "x \to \pm\infty": a limit point, not a value
        return True
    if isinstance(e, sp.Integer):
        return abs(int(e)) <= 2
    if isinstance(e, sp.Tuple):  # a tuple with an infinite end is an interval, (0,+\infty): not checked
        return any(x in (sp.oo, -sp.oo) for x in e) or all(is_trivial(x) for x in e)
    return _is_set_notation(e)


def _is_set_notation(e: object) -> bool:
    """A bare product / power of symbols involving a capital letter: A^c, yA, OZ, D\\varphi, A^TA. In these
    sheets capitals name sets, matrices, axes and operators, so such a product is notation, not a value."""
    if not isinstance(e, (sp.Mul, sp.Pow)) or any(a.is_Number for a in e.atoms(sp.Number) if abs(a) != 1):
        return False
    if e.atoms(sp.Function) or not all(isinstance(a, sp.Symbol) for a in e.atoms() if not a.is_Number):
        return False
    return any(s.name[:1].isupper() and s.name[:1].isascii() for s in e.free_symbols)


def _checkable(e: sp.Basic | None) -> bool:
    return e is not None and isinstance(e, (sp.Expr, sp.Tuple, sp.MatrixBase)) and not is_trivial(e)


@lru_cache(maxsize=4096)
def _candidates(text: str, prose: bool = False, values_only: bool = False) -> tuple[_Candidate, ...]:
    """Non-trivial parsed sides of every formula in a text: (side text, expr, fingerprint). With `prose`, the
    equations written in the prose without delimiters too."""
    segs = formulas(text) + (prose_formulas(text) if prose else [])
    out = []
    for seg in segs:
        for side in _sides(seg, values_only):
            e = _parse_side(side)
            if not _checkable(e):
                continue
            fp = _fingerprint(e)
            if fp is not None:
                out.append((side, e, fp))
    return tuple(out)


def checkable(text: str, values_only: bool = True) -> list[str]:
    """Sides of a text's formulas that the checker can compare (parsed, non-trivial). With `values_only`
    (how forbidden texts are read), the first side of each equation chain is left out."""
    return [side for side, _, _ in _candidates(text or "", False, values_only)]


MAX_SUBEXPRESSIONS = 300


def _subexpressions(e: sp.Basic) -> list[sp.Basic]:
    """Every subtree of e, plus partial sums / products of small Add / Mul nodes (x+y inside 1+x+y)."""
    out = []
    for node in sp.preorder_traversal(e):
        if not isinstance(node, sp.Expr) or node is e:
            continue
        out.append(node)
        if isinstance(node, (sp.Add, sp.Mul)) and 3 <= len(node.args) <= 6:
            for k in range(2, len(node.args)):
                out += [node.func(*c) for c in combinations(node.args, k)]
    if isinstance(e, (sp.Add, sp.Mul)) and 3 <= len(e.args) <= 6:
        for k in range(2, len(e.args)):
            out += [e.func(*c) for c in combinations(e.args, k)]
    return out


def _fragments(side: str) -> list[str]:
    """Bracketed pieces of an unparseable side: "(...)" with its parentheses, "{...}" without its braces.
    "\\lim_{(x,y)\\to(0,0)}\\frac{x^4y^4}{\\sqrt{x^2+y^2}}" still permits x^4y^4 and \\sqrt{x^2+y^2}."""
    out, stack = [], []
    for i, c in enumerate(side):
        if c in "({" and not (c == "{" and i and side[i - 1] == "\\"):
            stack.append((c, i))
        elif c in ")}" and stack:
            o, j = stack.pop()
            if (o, c) == ("(", ")"):
                out.append(side[j : i + 1])
            elif (o, c) == ("{", "}"):
                out.append(side[j + 1 : i])
    return out


@lru_cache(maxsize=2048)
def _permitted(text: str) -> tuple[_Candidate, ...]:
    """Permitted pool of a text: its formulas, their subexpressions (design 6.3 (b)), and the bracketed
    fragments of formulas that do not parse as a whole (limits, notation such as DG^{-1}(4,4,-1))."""
    segs = (formulas(text) or ([text.strip()] if text and text.strip() else [])) + prose_formulas(text)
    roots: list[tuple[str, sp.Basic]] = []
    for seg in segs:
        for side in _sides(seg):
            e = _parse_side(side)
            if e is not None:
                roots.append((side, e))
                continue
            for frag in _fragments(side):
                for piece in _top_level_split(frag):
                    pe = _parse_side(piece)
                    if pe is not None:
                        roots.append((piece, pe))
    out: list[_Candidate] = []
    seen: set[sp.Basic] = set()

    def add(label: str, e: sp.Basic) -> None:
        if e in seen or not _checkable(e) or len(out) >= MAX_SUBEXPRESSIONS:
            return
        seen.add(e)
        fp = _fingerprint(e)
        if fp is not None:
            out.append((label, e, fp))

    for side, e in roots:
        add(side, e)
    for side, e in roots:
        if isinstance(e, (sp.Expr, sp.Tuple)):
            for sub in _subexpressions(e):
                add(f"{side} > {sub}", sub)
    return tuple(out)


_CELL = re.compile(r"&|\\\\|\\quad(?![A-Za-z])")
_ENV = re.compile(r"\\(?:begin|end)\{[A-Za-z]*\*?\}")


def literal_tokens(text: str) -> set[str]:
    """The whole pieces of a text's formulas, normalised: each formula, its sides, the cells of its environments
    (cases, aligned, matrices), and the relation-separated pieces of each bracket or |...| group. A text without
    $...$ counts as one formula. "x-2y" is not a piece of "x-2y-z = 0"; "(x-2)^2+y^2" is one of
    "F(\\{(x,y) \\mid (x-2)^2+y^2 \\le 1\\})"."""
    segs = (formulas(text) or ([text.strip()] if text and text.strip() else [])) + prose_formulas(text)
    out: set[str] = set()
    for seg in segs:
        norm = _normalise(seg)
        out.add(norm)
        pieces = [*_top_level_split(norm), *_CELL.split(_ENV.sub(" ", norm))]
        groups = [g for f in _fragments(norm) for g in ([f, f[1:-1]] if f.startswith("(") else [f])]
        groups += [m.group(0) for m in re.finditer(r"\|[^|]+\|", norm)]
        for group in groups:
            pieces.append(group)
            pieces += _top_level_split(group)
        for piece in pieces:
            out.update(p.strip() for p in [piece, *_CELL.split(piece)] if p.strip())
    return out


def _negated(fp: _Fingerprint | None) -> _Fingerprint | None:
    if fp is None or fp[0] in ("tuple", "matrix"):
        return None
    if fp[0] == "const":
        return ("const", None, None if fp[2] is None else -fp[2])
    return ("expr", None, None if fp[2] is None else tuple(None if v is None else -v for v in fp[2]))


def _matches_permitted(e: sp.Basic, fp: _Fingerprint, perm: list[_Candidate]) -> bool:
    """Equal to a permitted formula or subexpression, up to sign (x-y is fine when y-x is permitted)."""
    for _, pe, pfp in perm:
        if e == pe or _compare(e, pe, fp, pfp):
            return True
        nfp = _negated(pfp)
        if nfp is not None and isinstance(pe, sp.Expr) and _compare(e, -pe, fp, nfp):
            return True
    return False


def explain(draft: str, forbidden: list[str], allowed: list[str]) -> list[tuple[str, str]]:
    """Like `leaked`, but each hit comes with the forbidden formula it matches: [(draft side, forbidden side)].

    The draft's equations written without $...$ are checked too. An unexpected error propagates: "no leak" and
    "not checked" must stay distinguishable, so the caller can fail closed."""
    draft_c = _candidates(draft or "", True)
    if not draft_c:
        return []
    forb = [c for t in forbidden for c in _candidates(t or "", False, True)]
    if not forb:
        return []
    perm = [c for t in allowed for c in _permitted(t or "")]
    hits: list[tuple[str, str]] = []
    done: set[str] = set()
    for side, e, fp in draft_c:
        if side in done:
            continue
        done.add(side)
        match = next((fs for fs, fe, ffp in forb if e == fe or _compare(e, fe, fp, ffp)), None)
        if match is None or _matches_permitted(e, fp, perm):
            continue
        hits.append((side, match))
    return hits


def leaked(draft: str, forbidden: list[str], allowed: list[str]) -> list[str]:
    """Draft formulas (or sides of them) equivalent to a forbidden formula and to no permitted one.

    `forbidden` / `allowed` are raw texts (step details, result value, allowed content, student messages);
    their formulas are extracted. A permitted formula also permits its subexpressions, and a permitted text
    without any $...$ is read as one formula (a student message typed without delimiters).
    """
    return [side for side, _ in explain(draft, forbidden, allowed)]
