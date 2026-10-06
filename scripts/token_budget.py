"""Estimate prompt/completion tokens per tutor turn and per session, for every exercise.

Builds the REAL prompts of each stage (same builders the pipeline uses) over a simulated session:
the student advances one step every two turns, asks for a hint on the others, and asks one
conceptual question. Tokens are counted with tiktoken o200k_base (OpenAI's tokenizer; Gemini and
Claude tokenizers give counts within ~10-20%).

    PYTHONPATH=work/pylib .venv/Scripts/python.exe scripts/token_budget.py [--turns 6] [--rewrites 0.3]

Reasoning tokens are not in the prompt and depend on the model/effort: they are reported as an
assumption (--reasoning), not measured.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

import tiktoken

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from tutor import prompts  # noqa: E402
from tutor.fitxes import load_llistes  # noqa: E402
from tutor.politica import EstatSessio, allowed_content, allowed_theory, decide  # noqa: E402
from tutor.schemas import Diagnosi, diagnosi_schema, guardia_schema  # noqa: E402
from tutor.teoria import load_teoria  # noqa: E402

ENC = tiktoken.get_encoding("o200k_base")
STUDENT = "He provat de fer això: $f(x,y)$ sobre la recta $y=kx$ dona $\\frac{k}{1+k^2}$, però no sé si això demostra res. Què hauria de fer ara?"
TUTOR = "Bona idea provar rectes. Què et diu exactament un camí: que el límit existeix, o només un candidat? Com podries controlar tots els camins alhora?"
DIAG_OUT = 260   # typical diagnosis JSON (5 steps, evidence, summary)
REPLY_OUT = 90   # 2-4 sentences + references
GUARD_OUT = 45


def tok(text: str) -> int:
    return len(ENC.encode(text))


def simulate(ex, teoria, turns: int) -> list[dict]:
    st = EstatSessio()
    hist: list[dict] = []
    ids = prompts.diagnosi_teoria_ids(ex, teoria)
    sch_d = tok(json.dumps(diagnosi_schema(ex, ids), ensure_ascii=False))
    diag_ctx = tok(prompts.DIAGNOSI_SYSTEM) + tok(prompts.diagnosi_context(ex, teoria))
    guard_ctx = tok(prompts.GUARDIA_SYSTEM) + tok(prompts.guardia_context(ex, teoria))
    out = []
    for t in range(turns):
        hist.append({"rol": "alumne", "text": STUDENT})
        done = ex.step_ids[: min(len(ex.step_ids) - 1, t // 2)]
        concept = t == 1
        d = Diagnosi(
            evidencia="", resum_alumne="",
            estat_passos=[{"pas": s, "estat": "completat" if s in done else "no_iniciat"} for s in ex.step_ids],
            pas_actual=ex.step_ids[len(done)], errors_detectats=[], error_altre="", resultat_proposat="cap",
            resultat_justificat=False, nivell_desorientacio="encallat",
            intencio="pregunta_conceptual" if concept else "demana_pista",
            teoria_pregunta=ids[:1] if concept else [],
        )
        pla, st = decide(ex, d, st)
        contingut = allowed_content(ex, pla, st.completats)
        th = allowed_theory(ex, pla, st.completats, teoria)
        th_ids = [i.id for i in th]
        diag_in = diag_ctx + tok(prompts.diagnosi_user(ex, st, hist)) + sch_d
        # The reply is plain text: no output schema in its prompt.
        reply_in = tok(prompts.RESPOSTA_SYSTEM) + tok(prompts.resposta_user(ex, hist, pla, contingut, None, th))
        guard_in = (guard_ctx + tok(prompts.guardia_user(pla, contingut, hist, TUTOR, th, th_ids))
                    + tok(json.dumps(guardia_schema(), ensure_ascii=False)))
        out.append({
            "diag_in": diag_in, "diag_cache": diag_ctx,
            "reply_in": reply_in,
            "guard_in": guard_in, "guard_cache": guard_ctx,
        })
        hist.append({"rol": "tutor", "text": TUTOR})
    return out


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * len(xs)))]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--turns", type=int, default=6)
    ap.add_argument("--rewrites", type=float, default=0.3, help="average rejected drafts per turn")
    ap.add_argument("--reasoning", type=int, default=600, help="assumed reasoning tokens per diagnosis call")
    args = ap.parse_args()

    teoria = load_teoria()
    _, exercicis = load_llistes(teoria=teoria)
    per_turn, per_session, cache_share, theory_tokens = [], [], [], []
    stage = {"diag_in": [], "reply_in": [], "guard_in": []}
    for ex in exercicis.values():
        turns = simulate(ex, teoria, args.turns)
        theory_tokens.append(tok(prompts.teoria_exercici(ex, teoria)))
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
    print(f"{n} exercises, {args.turns} turns/session, {args.rewrites} rewrites/turn, "
          f"{args.reasoning} reasoning tok/diagnosis (assumed)\n")
    print(f"theory per exercise (stages that see it all): mean {statistics.mean(theory_tokens):.0f}, "
          f"p90 {pct(theory_tokens, .9)}, max {max(theory_tokens)} tokens")
    for k, v in stage.items():
        print(f"{k:9s} mean {statistics.mean(v):6.0f}  p90 {pct(v, .9):6d}  max {max(v):6d}")
    ti = [a for a, _ in per_turn]
    to = [b for _, b in per_turn]
    print(f"\nper turn   input mean {statistics.mean(ti):6.0f} (p90 {pct(ti, .9):.0f})   output mean {statistics.mean(to):.0f}")
    print(f"           cacheable prefix share of input: {statistics.mean(cache_share):.0%}")
    si = [a for a, _ in per_session]
    so = [b for _, b in per_session]
    print(f"per session input mean {statistics.mean(si):6.0f} (p90 {pct(si, .9):.0f})   output mean {statistics.mean(so):.0f}")


if __name__ == "__main__":
    main()
