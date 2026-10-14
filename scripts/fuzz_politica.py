"""Fuzz the policy state machine over every sheet, with no LLM: random diagnosis sequences, invariant checks.

    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe scripts/fuzz_politica.py [--seeds 30] [--torns 20]
                                                                             [--exercicis t2-4c,t3-5]

Invariants (any violation is printed with the exercise, seed and turn):
  I1 no identical plan (action, target, level) more than 3 turns in a row (except after closing)
  I2 a student who keeps trying and stays stuck gets the step shown within 8 turns on that step
  I3 after `tancar` every turn is `despres_de_tancar`
  I4 the level reached on a step never decreases
  I5 a conceptual question never raises the level
  I6 the authored fallback of every plan passes the deterministic guard (it is sent without the LLM guard)
  I7 when a step is shown, its own detail passes the deterministic guard
"""

import argparse
import random
from collections import Counter

from core.course.domain.entities.course import Course
from core.course.domain.entities.exercise import Exercise
from core.course.infra.yaml_course_source import YamlCourseSource
from core.tutoring.domain.fallback import fallback_message
from core.tutoring.domain.guard import deterministic_check
from core.tutoring.domain.policy import allowed_content, allowed_theory, decide
from core.tutoring.domain.values.diagnosis import Diagnosis, StepState, StepStatus
from core.tutoring.domain.values.session_state import SessionState
from settings import BACKEND_DIR

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


def random_diagnosis(ex: Exercise, rng: random.Random, done: set[str], profile: str) -> tuple[Diagnosis, set[str]]:
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
    states: dict[str, StepState] = {
        s: ("completat" if s in done else rng.choice(["no_iniciat", "en_curs", "no_iniciat"])) for s in ex.step_ids
    }
    if profile == "random" and rng.random() < 0.08 and done:
        states[rng.choice(sorted(done))] = "erroni"
    mistakes = [rng.choice(ex.mistake_ids)] if (profile == "random" and rng.random() < 0.2) else []
    result = rng.choice(["cap"] * 6 + ["correcte", "incorrecte"]) if profile == "random" else "cap"
    diagnosis = Diagnosis.model_validate(
        {
            "evidence": "",
            "student_summary": "",
            "step_states": [StepStatus(step_id=s, state=states[s]) for s in ex.step_ids],
            "current_step": ex.step_ids[0],
            "detected_mistakes": mistakes,
            "other_mistake": "",
            "proposed_result": result,
            "result_justified": rng.random() < 0.3,
            "disorientation": disorientation,
            "intent": intent,
            "question_theory": [],
        }
    )
    return diagnosis, done


def check(course: Course, ex: Exercise, seed: int, turns: int, profile: str) -> list[str]:
    rng = random.Random(seed)
    state = SessionState()
    done: set[str] = set()
    out: list[str] = []
    plans: list[tuple[str, str | None, int]] = []
    since_target: Counter[str] = Counter()
    for n in range(1, turns + 1):
        diagnosis, done = random_diagnosis(ex, rng, done, profile)
        prev = state
        plan, state = decide(ex, diagnosis, state, STUDENT_TEXTS)
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--torns", type=int, default=20)
    ap.add_argument("--exercicis", default="")
    args = ap.parse_args()
    course = YamlCourseSource(BACKEND_DIR / "exercicis", BACKEND_DIR / "teoria").load()
    ids = args.exercicis.split(",") if args.exercicis else list(course.exercises)
    violations: list[str] = []
    for ex_id in ids:
        ex = course.exercise(ex_id)
        for profile in PROFILES:
            for seed in range(args.seeds if profile == "random" else 2):
                violations += check(course, ex, seed, args.torns, profile)
    kinds = Counter(v.split()[0] for v in violations)
    print(f"{len(ids)} exercises, violations: {dict(kinds) or 'none'}")
    seen: set[tuple[str, str]] = set()
    for v in violations:
        key = (v.split()[0], v.split()[1])
        if key not in seen:
            seen.add(key)
            print(" ", v[:300])


if __name__ == "__main__":
    main()
