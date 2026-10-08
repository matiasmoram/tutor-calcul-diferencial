"""Deterministic pedagogical policy: an explicit state machine over the session.

Takes the structured diagnosis of the LAST student message and the accumulated session state, and decides WHAT
the tutor may do this turn. The LLM that writes the reply never chooses the action or the hint level. It only
phrases the plan, and it only sees the content the plan allows.

Invariants (each has a test):
- Progress: a student who neither completes nor advances a step after a hint gets a higher level next time;
  every step-targeted action uses the same escalation rule.
- No oracle: a bare guess (no reasoning shown) is neither confirmed nor denied.
- Closing is terminal: after `tancar` the session stays closed.
- Non-hint actions (concept questions, redirections) never move the hint ladder.
- A regex never vetoes content the plan allows (completed or shown steps, the target's detail from level 3,
  the student's own words).
- Anti-gaming (help abuse, as in Cognitive Tutors): bare requests for help without any attempt climb the ladder
  at half speed, and the full step is only shown after the student has tried something.
"""

import re
from collections.abc import Mapping, Sequence
from typing import NamedTuple

from core.course.domain.entities.course import Course
from core.course.domain.entities.exercise import Exercise
from core.course.domain.entities.theory_item import TheoryItem
from core.course.domain.values.theory_ref import TheoryRef
from core.shared.domain.ids import TheoryItemId
from core.tutoring.domain.values.diagnosis import OTHER_MISTAKE, Diagnosis, Disorientation, Intent, StepState
from core.tutoring.domain.values.plan import TEACHER_MOVES, Action, Plan
from core.tutoring.domain.values.session_state import SessionState

MAX_HINT_LEVEL = 3  # 4 = show the full step
BASE_LEVEL: Mapping[Disorientation, int] = {"en_cami": 1, "dubte_puntual": 1, "encallat": 2, "perdut": 2}
STUCK_TURNS_AT_TOP_TO_SHOW = 2  # stuck turns at level 3 after which the step is shown without an explicit request
REPEATS_WHILE_WORKING = 2  # an on-track student mid-step gets this many turns at a level before it rises
STUCK_INTENTS: tuple[Intent, ...] = ("demana_pista", "demana_solucio", "frustracio")
WORK_INTENTS: tuple[Intent, ...] = ("mostra_treball", "proposa_resultat")  # intents that count as an attempt

# Actions that deliver content of the target step: they move the hint ladder and count for escalation.
HINT_ACTIONS: frozenset[Action] = frozenset(
    {"pista", "mostrar_pas", "questionar_error", "questionar_resultat", "demanar_justificacio", "validar_i_avancar"}
)
CLOSING_ACTIONS: tuple[Action, ...] = ("tancar", "mostrar_conclusio")
STATE_RANK: Mapping[StepState, int] = {"no_iniciat": 0, "erroni": 0, "en_curs": 1, "completat": 2}


class Decision(NamedTuple):
    plan: Plan
    state: SessionState


def _merge_completed(ex: Exercise, previous: Sequence[str], diagnosis: Diagnosis) -> list[str]:
    now = diagnosis.step_state_map()
    return [s for s in ex.step_ids if (s in previous and now.get(s) != "erroni") or now.get(s) == "completat"]


def _level(current: int, disorientation: Disorientation, escalate: bool) -> int:
    """The single escalation rule shared by every step-targeted action."""
    level = current + 1 if (current > 0 and escalate) else current
    return min(MAX_HINT_LEVEL, max(BASE_LEVEL[disorientation], level, 1))


def _allowed_texts(
    ex: Exercise,
    target: str | None,
    level: int,
    completed: Sequence[str],
    shown: Sequence[str],
    student_texts: Sequence[str],
    allow_result: bool,
) -> list[str]:
    texts = [ex.step(s).detail for s in dict.fromkeys([*completed, *shown])]
    if target is not None and level >= 3:
        texts.append(ex.step(target).detail)
    if allow_result:
        texts.append(ex.result.value)
    return [*texts, *student_texts]


def _forbidden_patterns(
    ex: Exercise,
    target: str | None,
    level: int,
    allow_result: bool,
    completed: Sequence[str],
    shown: Sequence[str],
    student_texts: Sequence[str],
) -> list[str]:
    """Leak regexes for this turn, minus any that would veto content the plan allows."""
    patterns: list[str] = [] if allow_result else list(ex.result.leak_patterns)
    if target is not None:
        idx = ex.step_ids.index(target)
        for later in ex.steps[idx + 1 :]:
            patterns += later.leak_patterns
        if level < 3:
            patterns += ex.step(target).leak_patterns
    allowed = _allowed_texts(ex, target, level, completed, shown, student_texts, allow_result)
    return [p for p in dict.fromkeys(patterns) if not any(re.search(p, t, re.IGNORECASE) for t in allowed)]


def _forbidden_texts(
    ex: Exercise, target: str | None, level: int, allow_result: bool, completed: Sequence[str], shown: Sequence[str]
) -> list[str]:
    """Same gate as the regexes, as texts: their formulas are compared by value, not by spelling."""
    opened = set(completed) | set(shown)
    texts = [] if allow_result else [ex.result.value]
    if target is not None:
        idx = ex.step_ids.index(target)
        texts += [s.detail for s in ex.steps[idx + 1 :] if s.id not in opened]
        if level < 3:
            texts.append(ex.step(target).detail)
    return texts


def _concept_items(ex: Exercise, diagnosis: Diagnosis, target: str | None, current: int) -> list[str]:
    """Concept answers may not name a later step's theory early (that names the strategy)."""
    if target is None:
        return list(diagnosis.question_theory)
    idx = ex.step_ids.index(target)
    gated = {r.item_id for s in ex.steps[idx + (1 if current >= 2 else 0) :] for r in s.theory}
    background = {r.item_id for r in ex.theory}
    return [t for t in diagnosis.question_theory if t not in gated or t in background]


def _concept_plan(ex: Exercise, diagnosis: Diagnosis, target: str, current: int) -> Plan:
    extra = _concept_items(ex, diagnosis, target, current)
    return Plan(
        action="explicar_concepte",
        reason="Pregunta conceptual." + (f" Teoria: {', '.join(extra)}." if extra else ""),
        target_step=target,
        hint_level=current,
        extra_theory=extra,
    )


def decide(ex: Exercise, diagnosis: Diagnosis, state: SessionState, student_texts: Sequence[str] = ()) -> Decision:
    d = diagnosis
    known_mistakes = [m for m in d.detected_mistakes if m in ex.mistake_ids]
    has_mistake = bool(known_mistakes) or (OTHER_MISTAKE in d.detected_mistakes and bool(d.other_mistake.strip()))
    justified = d.result_justified and not has_mistake

    completed = _merge_completed(ex, state.completed, d)
    new_steps = [s for s in completed if s not in state.completed]
    resolved = list(dict.fromkeys(completed + state.shown))  # a shown step no longer blocks the next one
    target = next((s for s in ex.step_ids if s not in resolved), None)
    states_now: dict[str, StepState] = d.step_state_map()
    states_now.update(dict.fromkeys(completed, "completat"))
    current = state.level_per_step.get(target, 0) if target else 0
    repeats = state.repetitions.get(target, 0) if target else 0

    stuck = d.intent in STUCK_INTENTS or d.disorientation in ("encallat", "perdut")
    progress = bool(target) and STATE_RANK.get(states_now.get(target or "", "no_iniciat"), 0) > STATE_RANK.get(
        state.step_states.get(target or "", "no_iniciat"), 0
    )
    after_hint_here = state.last_step == target and state.last_action in HINT_ACTIONS
    working = d.disorientation == "en_cami" and states_now.get(target or "") == "en_curs"
    # A student visibly working through a long step gets some room before the level rises.
    no_progress = (
        after_hint_here and not new_steps and not progress and (not working or repeats >= REPEATS_WHILE_WORKING)
    )
    attempt = d.intent in WORK_INTENTS or bool(new_steps) or progress
    # Help abuse: without an attempt this turn, the level only climbs after repeating it once at the same level.
    earned = attempt or repeats >= 2 or current == 0
    stuck = stuck and earned
    no_progress = no_progress and earned
    level = _level(current, d.disorientation, stuck or no_progress) if target else 0
    has_reasoning = bool(completed) or any(states_now.get(s) in ("en_curs", "completat") for s in ex.step_ids)
    # A result only drives the turn when this message is about it: a request for help, a question or
    # frustration is answered as such even if the diagnosis also reports a result.
    proposes = d.proposed_result != "cap" and d.intent in ("proposa_resultat", "mostra_treball")
    already_said = state.result_confirmed

    plan: Plan
    if state.closed:
        plan = Plan(
            action="despres_de_tancar",
            reason="L'exercici ja està tancat.",
            target_step=None,
            hint_level=0,
            may_state_result=True,
            requires_question=False,
        )

    elif d.intent == "fora_de_tema":
        plan = Plan(action="redirigir", reason="Missatge fora de tema.", target_step=target, hint_level=0)

    elif d.proposed_result == "correcte" and not has_mistake and (justified or target is None):
        plan = Plan(
            action="tancar",
            reason="Resultat correcte i justificat.",
            target_step=None,
            hint_level=0,
            may_state_result=True,
            requires_question=False,
        )

    elif d.intent == "pregunta_conceptual" and target is not None:
        # A question is answered first; a mistake in the same message comes back when the student shows work.
        plan = _concept_plan(ex, d, target, current)

    elif has_mistake:
        mistake_id = known_mistakes[0] if known_mistakes else OTHER_MISTAKE
        repeated = state.mistakes_seen.get(mistake_id, 0) > 0
        mistake = ex.mistake(mistake_id) if known_mistakes else None
        lvl = _level(current, d.disorientation, True) if (target and repeated) else (current if target else 0)
        plan = Plan(
            action="questionar_error",
            reason=f"Error detectat: {mistake_id}" + (" (repetit: es puja el nivell)." if repeated else "."),
            target_step=target,
            hint_level=lvl,
            target_mistake=mistake_id,
            mistake_text=mistake.description if mistake else d.other_mistake,
            # A repeated mistake gets new content (the step at a higher level), not the same question again.
            suggested_question=mistake.question if (mistake and not repeated) else None,
        )

    elif proposes and not has_reasoning and state.last_action != "demanar_raonament":
        # Asked once; a second bare guess gets a hint on the step instead (handled by the branches below).
        plan = Plan(
            action="demanar_raonament",
            reason="Proposa un resultat sense raonament: no es confirma ni es desmenteix.",
            target_step=target,
            hint_level=max(current, 1) if target else 0,
        )

    elif proposes and has_reasoning and d.proposed_result == "incorrecte":
        plan = Plan(
            action="questionar_resultat",
            reason="Resultat incorrecte després d'haver treballat.",
            target_step=target,
            hint_level=level,
        )

    elif proposes and has_reasoning and d.proposed_result == "correcte":
        plan = Plan(
            action="demanar_justificacio",
            reason="Resultat correcte amb raonament parcial.",
            target_step=target,
            hint_level=level,
            result_stated_by_student=True,
        )

    elif target is None:
        if d.intent == "pregunta_conceptual":
            plan = Plan(
                action="explicar_concepte",
                reason="Pregunta conceptual amb tots els passos fets.",
                target_step=None,
                hint_level=0,
                extra_theory=list(d.question_theory),
            )
        elif stuck or state.last_action == "demanar_conclusio":
            # Asked once already (or stuck): the conclusion follows from resolved steps, so the tutor states it.
            plan = Plan(
                action="mostrar_conclusio",
                reason="Tots els passos resolts; l'alumne no arriba a la conclusió.",
                target_step=None,
                hint_level=0,
                may_state_result=True,
            )
        else:
            plan = Plan(
                action="demanar_conclusio",
                reason="Tots els passos fets; falta la conclusió.",
                target_step=None,
                hint_level=0,
            )

    elif d.intent == "pregunta_conceptual":
        plan = _concept_plan(ex, d, target, current)

    elif (
        current >= MAX_HINT_LEVEL
        and not attempt
        and state.student_attempts == 0
        and repeats >= 1
        and state.last_action != "demanar_intent"
    ):
        # Help abuse at the top of the ladder: instead of repeating the same hint, ask for a tiny concrete attempt.
        plan = Plan(
            action="demanar_intent",
            reason="Demana ajuda al nivell màxim sense cap intent: es demana un intent concret.",
            target_step=target,
            hint_level=current,
        )

    elif (
        current >= MAX_HINT_LEVEL
        and (state.student_attempts > 0 or attempt)
        and (d.intent == "demana_solucio" or (stuck and repeats >= STUCK_TURNS_AT_TOP_TO_SHOW))
    ):
        plan = Plan(
            action="mostrar_pas",
            reason=f"Pistes esgotades al pas (nivell {current}).",
            target_step=target,
            hint_level=4,
            max_sentences=6,
        )

    elif new_steps and d.disorientation in ("en_cami", "dubte_puntual") and d.intent not in STUCK_INTENTS:
        plan = Plan(
            action="validar_i_avancar",
            reason=f"Ha completat: {', '.join(new_steps)}.",
            target_step=target,
            hint_level=max(current, 1),
        )

    else:
        reason = f"Desorientació '{d.disorientation}', intenció '{d.intent}', nivell previ {current}"
        reason += ", sense progrés des de l'última pista." if no_progress else "."
        plan = Plan(action="pista", reason=reason, target_step=target, hint_level=level)

    tone = "empatic" if (d.intent == "frustracio" or d.disorientation == "perdut") else plan.tone
    move = "Telling" if (plan.action == "pista" and plan.hint_level >= 3) else TEACHER_MOVES[plan.action]

    # ---- state transition ----
    closes = plan.action in CLOSING_ACTIONS
    closed = state.closed or closes
    if closes:
        completed = list(ex.step_ids)
    shown = [*state.shown, *([target] if plan.action == "mostrar_pas" and target and target not in state.shown else [])]
    confirmed = already_said or plan.action in ("tancar", "demanar_justificacio")

    allow_result = plan.may_state_result or confirmed
    plan = plan.model_copy(
        update={
            "tone": tone,
            "move": move,
            "forbidden_patterns": _forbidden_patterns(
                ex, plan.target_step, plan.hint_level, allow_result, completed, shown, student_texts
            ),
            "forbidden_texts": _forbidden_texts(ex, plan.target_step, plan.hint_level, allow_result, completed, shown),
        }
    )

    level_per_step = dict(state.level_per_step)
    repetitions = dict(state.repetitions)
    hint_step = plan.target_step if plan.action in HINT_ACTIONS else None
    if hint_step is not None:
        previous = level_per_step.get(hint_step, 0)
        same = state.last_step == hint_step and plan.hint_level == previous
        repetitions[hint_step] = repetitions.get(hint_step, 0) + 1 if same else 1
        level_per_step[hint_step] = max(previous, plan.hint_level)
    mistakes_seen = dict(state.mistakes_seen)
    if plan.target_mistake:
        mistakes_seen[plan.target_mistake] = mistakes_seen.get(plan.target_mistake, 0) + 1

    new_state = SessionState(
        completed=completed,
        level_per_step=level_per_step,
        turns=state.turns + 1,
        closed=closed,
        last_step=hint_step if hint_step is not None else state.last_step,
        last_action=plan.action,
        step_states=states_now,
        shown=shown,
        mistakes_seen=mistakes_seen,
        repetitions=repetitions,
        result_confirmed=confirmed,
        student_attempts=state.student_attempts + (1 if attempt else 0),
    )
    return Decision(plan, new_state)


def allowed_content(ex: Exercise, plan: Plan, completed: Sequence[str], shown: Sequence[str] = ()) -> str:
    """The ONLY solution content the reply stage gets to see."""
    parts: list[str] = []
    done = [ex.step(s) for s in dict.fromkeys([*completed, *shown])]
    if done:
        parts.append("Passos que l'alumne JA té resolts (pots referir-t'hi):")
        parts += [f"  - {s.title}: {s.detail}" for s in done]
    if plan.target_step:
        s = ex.step(plan.target_step)
        parts.append(f"PAS OBJECTIU: {s.title}")
        if plan.hint_level >= 1:
            parts.append(f"  objectiu: {s.objective}")
        if plan.hint_level >= 2:
            parts.append(f"  idea: {s.idea}")
        if plan.hint_level >= 3:
            parts.append(f"  detall: {s.detail}")
    if plan.mistake_text:
        parts.append(f"ERROR DE L'ALUMNE (no l'anomenis directament): {plan.mistake_text}")
    if plan.suggested_question:
        parts.append(f"Pregunta socràtica suggerida (pots adaptar-la): {plan.suggested_question}")
    if plan.may_state_result:
        parts.append(f"RESULTAT: {ex.result.value}")
    return "\n".join(parts) if parts else "(cap contingut de la solució)"


def allowed_theory(course: Course, ex: Exercise, plan: Plan, completed: Sequence[str]) -> list[TheoryItem]:
    """Theory items the reply stage may see and cite this turn.

    Naming a theorem names the strategy, so a step's theory follows the same gate as its idea (hint level >= 2).
    Items that solve this very exercise are never included."""
    refs: list[TheoryRef] = list(ex.theory)
    if plan.action in ("tancar", "despres_de_tancar"):
        refs += [r for s in ex.steps for r in s.theory]
    else:
        refs += [r for s in completed for r in ex.step(s).theory]
        if plan.target_step and plan.hint_level >= 2:
            refs += ex.step(plan.target_step).theory
    refs += [TheoryRef(t) for t in plan.extra_theory]
    reserved = course.reserved_ids(ex)
    ids: list[TheoryItemId] = [
        i for i in dict.fromkeys(r.item_id for r in refs) if i in course.theory and i not in reserved
    ]
    return [course.theory[i] for i in ids]
