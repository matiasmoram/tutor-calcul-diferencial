from collections.abc import Mapping, Sequence

from core.course.domain.entities.exercise import Exercise
from core.course.domain.entities.theory_item import TheoryItem
from core.tutoring.domain.values.plan import Action, Plan

FIXED_MESSAGES: Mapping[Action, str] = {
    "tancar": "Molt bé, has arribat al resultat amb una justificació correcta!",
    "despres_de_tancar": "Aquest exercici ja està resolt. Si vols, pots triar-ne un altre de la llista.",
    "redirigir": "Tornem a l'exercici: on t'havies quedat?",
    "demanar_conclusio": "Ja tens totes les peces. Com formularies la conclusió final?",
    "demanar_raonament": "Com hi has arribat? Explica'm el raonament que et porta a aquest resultat.",
    "demanar_intent": "Prova de fer tu el primer càlcul d'aquest pas, encara que no estiguis segur, i ensenya'm què et surt.",
}


def fallback_message(ex: Exercise, plan: Plan, theory: Sequence[TheoryItem] = ()) -> str:
    """Safe message built only from authored content, used when every draft is rejected.

    It delivers what the plan promised at its level (objective at 1, idea at 2-3, full step at 4), so the hint
    ladder never records a level the student did not receive. Authored step texts never match a regex the plan
    vetoes (see policy._forbidden_patterns and scripts/check_fitxes.py)."""
    if plan.action == "mostrar_conclusio":
        return f"Amb tots els passos resolts, la conclusió és: {ex.result.value.strip()} Ho veus clar?"
    if plan.action in FIXED_MESSAGES:
        return FIXED_MESSAGES[plan.action]
    if plan.action == "explicar_concepte" and theory:
        it = theory[0]
        return (
            f"Mira la {it.label.split(' (')[0]} del Tema {it.topic} als apunts. "
            "Com creus que s'aplica a aquest exercici?"
        )
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
