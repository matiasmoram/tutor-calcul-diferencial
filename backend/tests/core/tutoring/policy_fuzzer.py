"""Random diagnosis sequences for the policy (no LLM), as scripts/fuzz_politica.py generates them.

Invariants checked by `check` (any violation is reported with the exercise, seed and turn):
  I1 no identical plan (action, target, level) more than 3 turns in a row (except after closing, and answers to
     consecutive concept questions: each one answers a new question and none moves the ladder)
  I2 a student who keeps trying and stays stuck gets the step shown within 8 turns on that step
  I3 after `tancar` every turn is `despres_de_tancar`
  I4 the level reached on a step never decreases
  I5 a conceptual question never raises the level
  I6 the authored fallback of every plan passes the deterministic guard (it is sent without the LLM guard)
  I7 when a step is shown, its own detail passes the deterministic guard
"""

import random
from collections import Counter

from core.course.domain.entities.course import Course
from core.course.domain.entities.exercise import Exercise
from core.shared.llm.client import JsonObject
from core.tutoring.domain.fallback import fallback_message
from core.tutoring.domain.guard import deterministic_check
from core.tutoring.domain.policy import allowed_content, allowed_theory, decide
from core.tutoring.domain.values.diagnosis import Diagnosis
from core.tutoring.domain.values.session_state import SessionState

INTENTS = [
    "mostra_treball",
    "demana_pista",
    "demana_solucio",
    "pregunta_conceptual",
    "proposa_resultat",
    "fora_de_tema",
    "frustracio",
]
DISORIENTATIONS = ["en_cami", "dubte_puntual", "encallat", "perdut"]
PROFILES = ("random", "stuck_trying", "beggar")
STUDENT_TEXTS = ["(missatge de l'alumne)"]


def random_diagnosis(ex: Exercise, rng: random.Random, done: set[str], profile: str) -> tuple[JsonObject, set[str]]:
    """A diagnosis with the model's (Catalan) keys. Same random stream as the legacy fuzzer."""
    if profile == "stuck_trying":
        intent, disorientation = "mostra_treball", "encallat"
    elif profile == "beggar":
        intent, disorientation = "demana_solucio", "encallat"
    else:
        intent, disorientation = rng.choice(INTENTS), rng.choice(DISORIENTATIONS)
    done = set(done)
    if profile == "random" and rng.random() < 0.25:
        pending = [s for s in ex.step_ids if s not in done]
        if pending:
            done.add(pending[0])
    states = {
        s: ("completat" if s in done else rng.choice(["no_iniciat", "en_curs", "no_iniciat"])) for s in ex.step_ids
    }
    if profile == "random" and rng.random() < 0.08 and done:
        states[rng.choice(sorted(done))] = "erroni"
    mistakes = [rng.choice(ex.mistake_ids)] if (profile == "random" and rng.random() < 0.2) else []
    result = rng.choice(["cap"] * 6 + ["correcte", "incorrecte"]) if profile == "random" else "cap"
    data: JsonObject = {
        "evidencia": "",
        "resum_alumne": "",
        "estat_passos": [{"pas": s, "estat": states[s]} for s in ex.step_ids],
        "pas_actual": ex.step_ids[0],
        "errors_detectats": mistakes,
        "error_altre": "",
        "resultat_proposat": result,
        "resultat_justificat": rng.random() < 0.3,
        "nivell_desorientacio": disorientation,
        "intencio": intent,
        "teoria_pregunta": [],
    }
    return data, done


def diagnosis_sequence(ex: Exercise, seed: int, turns: int, profile: str) -> list[JsonObject]:
    rng = random.Random(seed)
    done: set[str] = set()
    out: list[JsonObject] = []
    for _ in range(turns):
        data, done = random_diagnosis(ex, rng, done, profile)
        out.append(data)
    return out


def check(course: Course, ex: Exercise, seed: int, turns: int, profile: str) -> list[str]:
    state = SessionState()
    out: list[str] = []
    plans: list[tuple[str, str | None, int]] = []
    since_target: Counter[str] = Counter()
    for n, data in enumerate(diagnosis_sequence(ex, seed, turns, profile), 1):
        prev = state
        plan, state = decide(ex, Diagnosis.model_validate(data), state, STUDENT_TEXTS)
        plans.append((plan.action, plan.target_step, plan.hint_level))
        tag = f"{ex.id} {profile} seed={seed} t={n} {plan.action}/{plan.target_step}/{plan.hint_level}"
        if (
            len(plans) >= 4
            and len(set(plans[-4:])) == 1
            and plan.action not in ("despres_de_tancar", "explicar_concepte")
        ):
            out.append(f"I1 same plan 4x: {tag}")
        if prev.closed and plan.action != "despres_de_tancar":
            out.append(f"I3 reopened after closing: {tag}")
        for s, lvl in prev.level_per_step.items():
            if state.level_per_step.get(s, 0) < lvl:
                out.append(f"I4 level decreased on {s}: {tag}")
        if (
            plan.action == "explicar_concepte"
            and plan.target_step
            and state.level_per_step.get(plan.target_step, 0) > prev.level_per_step.get(plan.target_step, 0)
        ):
            out.append(f"I5 concept question raised the level: {tag}")
        content = allowed_content(ex, plan, state.completed, state.shown)
        theory = allowed_theory(course, ex, plan, state.completed)
        permitted = [content, ex.statement_md(), *[t.statement for t in theory]]
        fallback = fallback_message(ex, plan, theory)
        problems = [
            p
            for p in deterministic_check(fallback, plan, permitted)
            if "pregunta" not in p and "massa llarg" not in p  # the question requirement is irrelevant here
        ]
        if problems:
            out.append(f"I6 fallback fails guard {problems[:2]}: {tag}")
        if plan.action == "mostrar_pas" and plan.target_step:
            shown = ex.step(plan.target_step).detail + " Ho veus?"
            problems = [p for p in deterministic_check(shown, plan, permitted) if "massa llarg" not in p]
            if problems:
                out.append(f"I7 shown step fails guard {problems[:2]}: {tag}")
        if profile == "stuck_trying" and plan.target_step:
            since_target[plan.target_step] += 1
            if since_target[plan.target_step] > 8 and plan.target_step not in state.shown:
                out.append(f"I2 stuck student never shown the step: {tag}")
                break
    return out
