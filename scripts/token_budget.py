"""Estimate prompt/completion tokens per tutor turn and per session, for every exercise.

Builds the REAL prompts of each stage (same builders the tutoring adapters use) over a simulated session:
the student advances one step every two turns, asks for a hint on the others, and asks one
conceptual question. Tokens are counted with tiktoken o200k_base (OpenAI's tokenizer; Gemini and
Claude tokenizers give counts within ~10-20%).

    PYTHONPATH=work/pylib .venv/Scripts/python.exe scripts/token_budget.py [--turns 6] [--rewrites 0.3]

Reasoning tokens are not in the prompt and depend on the model/effort: they are reported as an
assumption (--reasoning), not measured. No model is called.
"""

from __future__ import annotations

import argparse
import json
import statistics

import tiktoken

from core.course.domain.entities.course import Course
from core.course.domain.entities.exercise import Exercise
from core.course.infra.yaml_course_source import YamlCourseSource
from core.tutoring.domain.policy import allowed_content, allowed_theory, decide
from core.tutoring.domain.theory_access import concept_question_ids
from core.tutoring.domain.values.chat_message import ChatMessage
from core.tutoring.domain.values.diagnosis import Diagnosis
from core.tutoring.domain.values.session_state import SessionState
from core.tutoring.infra import prompts
from core.tutoring.infra.llm_schemas import diagnosis_schema, guard_schema
from settings import BACKEND_DIR

ENC = tiktoken.get_encoding("o200k_base")
STUDENT = "He provat de fer això: $f(x,y)$ sobre la recta $y=kx$ dona $\\frac{k}{1+k^2}$, però no sé si això demostra res. Què hauria de fer ara?"
TUTOR = "Bona idea provar rectes. Què et diu exactament un camí: que el límit existeix, o només un candidat? Com podries controlar tots els camins alhora?"
DIAG_OUT = 260  # typical diagnosis JSON (5 steps, evidence, summary)
REPLY_OUT = 90  # 2-4 sentences + references
GUARD_OUT = 45


def tok(text: str) -> int:
    return len(ENC.encode(text))


def simulate(ex: Exercise, course: Course, turns: int) -> list[dict[str, int]]:
    st = SessionState()
    hist: list[ChatMessage] = []
    ids = concept_question_ids(course, ex)
    sch_d = tok(json.dumps(diagnosis_schema(ex, ids), ensure_ascii=False))
    diag_ctx = tok(prompts.DIAGNOSIS_SYSTEM) + tok(prompts.diagnosis_context(course, ex))
    guard_ctx = tok(prompts.GUARD_SYSTEM) + tok(prompts.guard_context(course, ex))
    out = []
    for t in range(turns):
        hist.append(ChatMessage.from_student(STUDENT))
        done = ex.step_ids[: min(len(ex.step_ids) - 1, t // 2)]
        concept = t == 1
        d = Diagnosis.model_validate(
            {
                "evidencia": "",
                "resum_alumne": "",
                "estat_passos": [{"pas": s, "estat": "completat" if s in done else "no_iniciat"} for s in ex.step_ids],
                "pas_actual": ex.step_ids[len(done)],
                "errors_detectats": [],
                "error_altre": "",
                "resultat_proposat": "cap",
                "resultat_justificat": False,
                "nivell_desorientacio": "encallat",
                "intencio": "pregunta_conceptual" if concept else "demana_pista",
                "teoria_pregunta": ids[:1] if concept else [],
            }
        )
        plan, st = decide(ex, d, st)
        content = allowed_content(ex, plan, st.completed, st.shown)
        th = allowed_theory(course, ex, plan, st.completed)
        th_ids = [i.id for i in th]
        diag_in = diag_ctx + tok(prompts.diagnosis_user(st, hist)) + sch_d
        # The reply is plain text: no output schema in its prompt.
        reply_in = tok(prompts.REPLY_SYSTEM) + tok(prompts.reply_user(ex, hist, plan, content, None, th))
        guard_in = (
            guard_ctx
            + tok(prompts.guard_user(plan, content, hist, TUTOR, th, th_ids))
            + tok(json.dumps(guard_schema(), ensure_ascii=False))
        )
        out.append(
            {
                "diag_in": diag_in,
                "diag_cache": diag_ctx,
                "reply_in": reply_in,
                "guard_in": guard_in,
                "guard_cache": guard_ctx,
            }
        )
        hist.append(ChatMessage.from_tutor(TUTOR))
    return out


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * len(xs)))]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--turns", type=int, default=6)
    ap.add_argument("--rewrites", type=float, default=0.3, help="average rejected drafts per turn")
    ap.add_argument("--reasoning", type=int, default=600, help="assumed reasoning tokens per diagnosis call")
    args = ap.parse_args()

    course = YamlCourseSource(BACKEND_DIR / "exercicis", BACKEND_DIR / "teoria").load()
    exercicis = course.exercises
    per_turn, per_session, cache_share, theory_tokens = [], [], [], []
    stage: dict[str, list[int]] = {"diag_in": [], "reply_in": [], "guard_in": []}
    for ex in exercicis.values():
        turns = simulate(ex, course, args.turns)
        theory_tokens.append(tok(prompts.exercise_theory(course, ex)))
        sess_in = sess_out = 0
        for t in turns:
            r = 1 + args.rewrites  # each rewrite = one more reply + one more guard call
            tin = t["diag_in"] + r * (t["reply_in"] + t["guard_in"])
            tout = DIAG_OUT + args.reasoning + r * (REPLY_OUT + GUARD_OUT)
            per_turn.append((tin, tout))
            cache_share.append((t["diag_cache"] + r * t["guard_cache"]) / tin)
            for k in stage:
                stage[k].append(t[k])
            sess_in += tin
            sess_out += tout
        per_session.append((sess_in, sess_out))

    n = len(exercicis)
    print(
        f"{n} exercises, {args.turns} turns/session, {args.rewrites} rewrites/turn, "
        f"{args.reasoning} reasoning tok/diagnosis (assumed)\n"
    )
    print(
        f"theory per exercise (stages that see it all): mean {statistics.mean(theory_tokens):.0f}, "
        f"p90 {pct(theory_tokens, 0.9)}, max {max(theory_tokens)} tokens"
    )
    for k, v in stage.items():
        print(f"{k:9s} mean {statistics.mean(v):6.0f}  p90 {pct(v, 0.9):6d}  max {max(v):6d}")
    ti = [a for a, _ in per_turn]
    to = [b for _, b in per_turn]
    print(
        f"\nper turn   input mean {statistics.mean(ti):6.0f} (p90 {pct(ti, 0.9):.0f})   output mean {statistics.mean(to):.0f}"
    )
    print(f"           cacheable prefix share of input: {statistics.mean(cache_share):.0%}")
    si = [a for a, _ in per_session]
    so = [b for _, b in per_session]
    print(
        f"per session input mean {statistics.mean(si):6.0f} (p90 {pct(si, 0.9):.0f})   output mean {statistics.mean(so):.0f}"
    )


if __name__ == "__main__":
    main()
