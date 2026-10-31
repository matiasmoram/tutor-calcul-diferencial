"""Code gates of the per-parts pipeline (Catalan messages: they go back to the model as rejection reasons).

A  RESOLUTION  the correct resolution: the parts follow the sheet's steps in order (theory: the statement, then 2 to
               5 proof stages), 1 to 4 fragments each, every fragment renders; a blind check finds nothing wrong
               and the resolution reaches the result.
B  CORRUPTION  one part's error as small edits of its correct text, applied by code: the first edit is the error,
               the later ones its local consequences; the quote is located on the edited text.
C  PART CHECK  a blind check of the corrupted part, with the earlier parts as correct context, finds exactly that
               error and nothing else wrong; its consequences come after it."""

import re

from pydantic import BaseModel

from core.mistakes.domain.entities.mistake_exercise import DeclaredMistake
from core.mistakes.domain.entities.parted_mistake_exercise import STATEMENT_TITLE
from core.mistakes.domain.exceptions import MistakePartsUnavailableException
from core.mistakes.domain.services.generation_checks import (
    fragment_problems,
    located_before,
    same_problem,
    unknown_message,
)
from core.mistakes.domain.services.locate import locate, overlap
from core.mistakes.domain.values.llm_outputs import (
    SEVERITY_CONSEQUENCE,
    SEVERITY_ERROR,
    CorruptionDraft,
    PartReport,
    ResolutionDraft,
    ResolutionReport,
)
from core.mistakes.domain.values.mistake_kind import PROBLEM_MISTAKE_KINDS, THEORY_MISTAKE_KINDS
from core.mistakes.domain.values.mistake_source import MistakeSource, ProblemSource, TheorySource
from core.mistakes.domain.values.resolution import Resolution, ResolutionPart
from core.shared.math.latex_vocabulary import unknown_commands

MIN_PARTS = 2
MAX_FRAGMENTS_PER_PART = 4
MAX_PARTS_PER_STEP = 2
MAX_STATEMENT_FRAGMENTS = 3
MIN_PROOF_PARTS, MAX_PROOF_PARTS = 2, 5
MAX_EDITS = 3
MAX_EDITED_CHARS = 240
MAX_EDITED_SHARE = 0.5  # of the part's characters
# Words that would point the student at the error.
_MARKERS = re.compile(r"\(error\)|compte|potser|crec que", re.IGNORECASE)


def require_parts(source: MistakeSource) -> None:
    """Raises MistakePartsUnavailableException for a source that cannot make 2 parts: a problem whose sheet has a
    single step (theory always has the statement and at least 2 proof stages)."""
    if isinstance(source, ProblemSource) and len(source.exercise.steps) < MIN_PARTS:
        raise MistakePartsUnavailableException(source.id)


class ResolutionCheck(BaseModel):
    resolution: Resolution
    problems: list[str]  # empty: valid

    @property
    def valid(self) -> bool:
        return not self.problems


def _fragment_count_problem(fragments: list[str], what: str, most: int) -> list[str]:
    if 1 <= len(fragments) <= most:
        return []
    return [f"{what} ha de tenir entre 1 i {most} fragments (en té {len(fragments)})"]


def check_resolution(draft: ResolutionDraft, source: MistakeSource) -> ResolutionCheck:
    """Stage A, by code. Parts are named as the writer numbered them."""
    problems: list[str] = []
    parts: list[ResolutionPart] = []
    if isinstance(source, TheorySource):
        statement = [f.strip() for f in draft.statement]
        problems += _fragment_count_problem(statement, "l'enunciat", MAX_STATEMENT_FRAGMENTS)
        problems += fragment_problems(statement, " de l'enunciat")
        parts.append(ResolutionPart(title=STATEMENT_TITLE, step="", fragments=statement))
        if not MIN_PROOF_PARTS <= len(draft.parts) <= MAX_PROOF_PARTS:
            problems.append(
                f"la demostració ha de tenir entre {MIN_PROOF_PARTS} i {MAX_PROOF_PARTS} parts (en té {len(draft.parts)})"
            )
        for i, d in enumerate(draft.parts, 1):
            fragments = [f.strip() for f in d.fragments]
            if not d.title.strip():
                problems.append(f"la part {i} de la demostració no té títol")
            problems += _fragment_count_problem(fragments, f"la part {i} de la demostració", MAX_FRAGMENTS_PER_PART)
            problems += fragment_problems(fragments, f" de la part {i} de la demostració")
            parts.append(ResolutionPart(title=d.title.strip(), step="", fragments=fragments))
        return ResolutionCheck(
            resolution=Resolution(parts=parts, statement_fragments=len(statement)), problems=problems
        )

    steps = [d.step for d in draft.parts]
    expected = source.exercise.step_ids
    collapsed = [s for k, s in enumerate(steps) if k == 0 or s != steps[k - 1]]
    if collapsed != expected:
        problems.append(
            f"les parts han de seguir els passos de la solució en ordre, una o dues parts per pas: "
            f"{', '.join(expected)} (has fet servir: {', '.join(steps) or 'cap'})"
        )
    for step in dict.fromkeys(steps):
        if steps.count(step) > MAX_PARTS_PER_STEP:
            problems.append(f"el pas {step} té {steps.count(step)} parts; com a màxim {MAX_PARTS_PER_STEP}")
    if len(draft.parts) < MIN_PARTS:
        problems.append(f"calen com a mínim {MIN_PARTS} parts (n'hi ha {len(draft.parts)})")
    titles = {s.id: s.title for s in source.exercise.steps}
    for i, d in enumerate(draft.parts, 1):
        fragments = [f.strip() for f in d.fragments]
        problems += _fragment_count_problem(fragments, f"la part {i}", MAX_FRAGMENTS_PER_PART)
        problems += fragment_problems(fragments, f" de la part {i}")
        parts.append(ResolutionPart(title=titles.get(d.step, d.step), step=d.step, fragments=fragments))
    return ResolutionCheck(resolution=Resolution(parts=parts, statement_fragments=0), problems=problems)


def _where(resolution: Resolution, fragment: object) -> str:
    """A document-wide fragment number as the writer knows it: part and fragment inside the part."""
    if isinstance(fragment, int) and not isinstance(fragment, bool):
        first = 1
        for i, p in enumerate(resolution.parts, 1):
            if first <= fragment < first + len(p.fragments):
                return f"la part {i}, fragment {fragment - first + 1}"
            first += len(p.fragments)
    return f"el fragment {fragment}"


def resolution_verification_problems(resolution: Resolution, report: ResolutionReport, theory: bool) -> list[str]:
    """Stage A's blind check passes with no error, no consequence, and the result reached."""
    issues = [
        f"hi ha un error a {_where(resolution, p.fragment)}: «{p.quote}» — {p.explanation}"
        for p in report.findings
        if p.severity in (SEVERITY_ERROR, SEVERITY_CONSEQUENCE)
    ]
    if report.reaches_result is not True:
        issues.append(
            "la demostració no demostra l'enunciat complet"
            if theory
            else "la resolució no arriba al resultat correcte de la solució de referència"
        )
    return issues


class CorruptionCheck(BaseModel):
    unfit: bool  # the model found no believable error in the part: another part is chosen
    flawed_fragments: list[str]
    mistake: DeclaredMistake | None
    problems: list[str]  # empty: valid

    @property
    def valid(self) -> bool:
        return not self.problems


class _Edit(BaseModel):
    number: int  # 1-based, in the order sent
    fragment: int  # 1-based, inside the part
    start: int  # of `original` in the correct fragment
    original: str
    new: str

    @property
    def end(self) -> int:
        return self.start + len(self.original)


def _edits(clean: list[str], draft: CorruptionDraft) -> tuple[list[_Edit], list[str]]:
    edits: list[_Edit] = []
    problems: list[str] = []
    if not 1 <= len(draft.edits) <= MAX_EDITS:
        problems.append(f"calen entre 1 i {MAX_EDITS} canvis (n'hi ha {len(draft.edits)})")
    for k, e in enumerate(draft.edits, 1):
        fi = e.fragment
        if not isinstance(fi, int) or isinstance(fi, bool) or not 1 <= fi <= len(clean):
            problems.append(f"el canvi {k} apunta a un fragment inexistent ({fi})")
            continue
        if e.new == e.original:
            problems.append(f"el canvi {k} no canvia res («nou» és igual que «original»)")
        count = clean[fi - 1].count(e.original) if e.original else 0
        if count != 1:
            problems.append(
                f"l'«original» del canvi {k} ha d'aparèixer exactament una vegada, copiat literalment, al fragment "
                f"{fi} (hi apareix {count} vegades): «{e.original}»"
            )
            continue
        edits.append(
            _Edit(number=k, fragment=fi, start=clean[fi - 1].index(e.original), original=e.original, new=e.new)
        )
    for a in edits:
        for b in edits:
            if a.number < b.number and a.fragment == b.fragment and overlap(a.start, a.end, b.start, b.end):
                problems.append(f"els canvis {a.number} i {b.number} se solapen")
    if (
        edits
        and edits[0].number == 1
        and any((e.fragment, e.start) < (edits[0].fragment, edits[0].start) for e in edits)
    ):
        problems.append(
            "el primer canvi és l'error i ha de ser el primer de la part; els altres en són conseqüències posteriors"
        )
    edited = sum(max(len(e.original), len(e.new)) for e in draft.edits)
    size = sum(len(f) for f in clean)
    if edited > MAX_EDITED_CHARS or edited > MAX_EDITED_SHARE * size:
        problems.append(
            f"els canvis són massa grans ({edited} caràcters; com a màxim {MAX_EDITED_CHARS} i la meitat de la part): "
            "fes un canvi petit i local"
        )
    return edits, problems


def _apply(clean: list[str], edits: list[_Edit]) -> list[str]:
    flawed = list(clean)
    for e in sorted(edits, key=lambda e: (e.fragment, e.start), reverse=True):
        text = flawed[e.fragment - 1]
        flawed[e.fragment - 1] = text[: e.start] + e.new + text[e.end :]
    return flawed


def check_corruption(
    clean: list[str], draft: CorruptionDraft, first_fragment: int, mistake_id: str, theory: bool
) -> CorruptionCheck:
    """Stage B, by code. `clean`: the part's correct fragments; `first_fragment`: the document-wide number of its
    first one, which numbers the declared error like every fragment of the document."""
    if draft.fit is False:
        return CorruptionCheck(
            unfit=True, flawed_fragments=clean, mistake=None, problems=["la part no és apta per a un error"]
        )
    edits, problems = _edits(clean, draft)
    if problems:
        return CorruptionCheck(unfit=False, flawed_fragments=clean, mistake=None, problems=problems)

    flawed = _apply(clean, edits)
    problems += fragment_problems(flawed)
    for e in edits:
        if _MARKERS.search(e.new):
            problems.append(f"el canvi {e.number} assenyala l'error («{e.new}»): el text ha de sonar convençut")
    valid_kinds = THEORY_MISTAKE_KINDS if theory else PROBLEM_MISTAKE_KINDS
    if draft.kind not in valid_kinds:
        problems.append(f"el tipus no és vàlid ({draft.kind}); tipus vàlids: {', '.join(valid_kinds)}")
    for field, value in (
        ("cita", draft.quote),
        ("explicacio", draft.explanation),
        ("correccio", draft.correction),
        ("pista", draft.hint),
    ):
        if not value.strip():
            problems.append(f"falta el camp '{field}'")
        if unknown := unknown_commands(value):
            problems.append(f"el camp '{field}' {unknown_message(unknown)}")

    error = edits[0]
    text = flawed[error.fragment - 1]
    new_start, new_end = error.start, error.start + len(error.new)
    span = locate(text, draft.quote)
    # An empty `nou` (a deletion) leaves a point: the quote must reach it.
    on_new = span is not None and (
        overlap(span[0], span[1], new_start, new_end) if new_end > new_start else span[0] <= new_start <= span[1]
    )
    if not on_new:
        problems.append(
            f"la cita ha de ser el text erroni del primer canvi, copiat literalment del fragment {error.fragment} ja "
            f"canviat: «{draft.quote}»"
        )
    mistake = None
    if span is not None and on_new and not problems:
        mistake = DeclaredMistake(
            id=mistake_id,
            fragment=first_fragment + error.fragment - 1,
            quote=text[span[0] : span[1]],
            start=span[0],
            end=span[1],
            kind=draft.kind or "",
            explanation=draft.explanation,
            correction=draft.correction,
            hint=draft.hint,
        )
    return CorruptionCheck(unfit=False, flawed_fragments=flawed, mistake=mistake, problems=problems)


def part_verification_problems(
    mistake: DeclaredMistake, first_fragment: int, flawed: list[str], report: PartReport
) -> list[str]:
    """Stage C passes with exactly one error, the declared one, every consequence after it and no alert about the
    earlier parts. The verifier numbers the part's fragments from 1; imprecisions are ignored."""
    local = mistake.model_copy(update={"fragment": mistake.fragment - first_fragment + 1})
    errors = [p for p in report.findings if p.severity == SEVERITY_ERROR]
    found = [p for p in errors if same_problem(local, p, flawed)]
    issues: list[str] = []
    if not found:
        issues.append(
            f"l'error declarat al fragment {local.fragment} («{local.quote}») no l'ha detectat el verificador: "
            "potser no és un error real o és ambigu"
        )
    elif len(found) > 1:
        issues.append("el verificador hi veu més d'un error a la cita: l'error ha de ser un de sol i local")
    for p in errors:
        if p not in found:
            issues.append(f"hi ha un error NO intencionat al fragment {p.fragment}: «{p.quote}» — {p.explanation}")
    for p in report.findings:
        if p.severity == SEVERITY_CONSEQUENCE and located_before(p, local, flawed):
            issues.append(
                f"la conseqüència del fragment {p.fragment} («{p.quote}») és anterior a l'error: "
                "les conseqüències han de venir després de l'error"
            )
    if alert := report.context_alert.strip():
        issues.append(f"el verificador creu que les parts anteriors tenen un error: {alert}")
    return issues
