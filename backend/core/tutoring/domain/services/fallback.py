from collections.abc import Mapping, Sequence

from core.course.domain.entities.exercise import Exercise
from core.course.domain.entities.theory_item import KIND_NAMES, TheoryItem
from core.tutoring.domain.values.plan import Action, Plan

FIXED_MESSAGES: Mapping[Action, str] = {
    "tancar": "Molt bé, has arribat al resultat amb una justificació correcta!",
    "despres_de_tancar": "Aquest exercici ja està resolt. Si vols, pots triar-ne un altre de la llista.",
    "redirigir": "Tornem a l'exercici: on t'havies quedat?",
    "demanar_conclusio": "Ja tens totes les peces. Com formularies la conclusió final?",
    "demanar_raonament": "Com hi has arribat? Explica'm el raonament que et porta a aquest resultat.",
    "demanar_intent": "Prova de fer tu el primer càlcul d'aquest pas, encara que no estiguis segur, i ensenya'm què et surt.",
}


# Grammatical gender of each item kind, for the Catalan article ("la Definició 3", "el Teorema 12").
_FEMININE: frozenset[str] = frozenset({"definicio", "proposicio", "observacio", "nota"})


def _named(it: TheoryItem) -> str:
    """How a reply names an item so the web links it: "el Teorema 12 del Tema 3"."""
    if it.number is None:
        return f"els apunts del Tema {it.topic} (§{it.section})" if it.section else f"els apunts del Tema {it.topic}"
    article = "la" if it.kind in _FEMININE else "el"
    return f"{article} {KIND_NAMES[it.kind]} {it.number} del Tema {it.topic}"


def fallback_message(ex: Exercise, plan: Plan, theory: Sequence[TheoryItem] = ()) -> str:
    """Safe message built only from authored content, used when every draft is rejected.

    It delivers what the plan promised at its level (objective at 1, idea at 2-3, full step at 4), so the hint
    ladder never records a level the student did not receive. Authored step texts never match a regex the plan
    vetoes (see policy._forbidden_patterns and scripts/check_fitxes.py)."""
    if plan.action == "mostrar_conclusio":
        return f"Amb tots els passos resolts, la conclusió és: {ex.result.value.strip()} Ho veus clar?"
    if plan.action in FIXED_MESSAGES:
        return FIXED_MESSAGES[plan.action]
    if plan.action == "explicar_concepte":
        # The item that answers the question; only without one, the first allowed item (usually background). A
        # concept answer never delivers step content: it does not move the hint ladder.
        by_id: dict[str, TheoryItem] = {str(it.id): it for it in theory}
        it = next((by_id[i] for i in plan.extra_theory if i in by_id), theory[0] if theory else None)
        if it is None:
            return "Quin concepte concret no et quadra? Explica'm amb les teves paraules com l'entens ara."
        where = "" if it.number is None else " als apunts"
        return f"Mira {_named(it)}{where}. Com creus que s'aplica a aquest exercici?"
    if plan.suggested_question:
        return plan.suggested_question
    if plan.target_step:
        step = ex.step(plan.target_step)
        if plan.hint_level >= 4:
            return f"Aquest pas es fa així: {step.detail.strip()} Com continuaries a partir d'aquí?"
        if plan.hint_level >= 2:
            return f"Una idea per avançar: {step.idea.strip()} Com ho aplicaries?"
        return f"Ara l'objectiu és aquest: {step.objective.strip()} Com ho començaries?"
    return "Explica'm amb les teves paraules què has fet fins ara i on t'has encallat."
