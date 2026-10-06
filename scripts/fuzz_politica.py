"""Fuzz the policy state machine over every sheet, with no LLM: random diagnosis sequences, invariant checks.

    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe scripts/fuzz_politica.py [--seeds 30] [--torns 20]

Invariants (any violation is printed with the exercise, seed and turn):
  I1 no identical plan (action, target, level) more than 3 turns in a row (except after closing)
  I2 a student who keeps trying and stays stuck gets the step shown within 8 turns on that step
  I3 after `tancar` every turn is `despres_de_tancar`
  I4 the level reached on a step never decreases
  I5 a conceptual question never raises the level
  I6 the authored fallback of every plan passes the deterministic guard (it is sent without the LLM guard)
  I7 when a step is shown, its own detail passes the deterministic guard
"""

from __future__ import annotations

import argparse
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from tutor.fitxes import load_llistes  # noqa: E402
from tutor.guardia import deterministic_check  # noqa: E402
from tutor.pipeline import fallback_message  # noqa: E402
from tutor.politica import EstatSessio, allowed_content, allowed_theory, decide  # noqa: E402
from tutor.schemas import Diagnosi  # noqa: E402
from tutor.teoria import load_teoria  # noqa: E402

INTENTS = ["mostra_treball", "demana_pista", "demana_solucio", "pregunta_conceptual", "proposa_resultat",
           "fora_de_tema", "frustracio"]
DESOR = ["en_cami", "dubte_puntual", "encallat", "perdut"]


def random_diag(ex, rng, done: set[str], profile: str) -> tuple[Diagnosi, set[str]]:
    if profile == "stuck_trying":
        intent, des = "mostra_treball", "encallat"
    elif profile == "beggar":
        intent, des = "demana_solucio", "encallat"
    else:
        intent, des = rng.choice(INTENTS), rng.choice(DESOR)
    done = set(done)
    if profile == "random" and rng.random() < 0.25:
        pending = [s for s in ex.step_ids if s not in done]
        if pending:
            done.add(pending[0])
    estat = {s: ("completat" if s in done else rng.choice(["no_iniciat", "en_curs", "no_iniciat"])) for s in ex.step_ids}
    if profile == "random" and rng.random() < 0.08 and done:
        estat[rng.choice(sorted(done))] = "erroni"
    errors = [rng.choice(ex.error_ids)] if (profile == "random" and rng.random() < 0.2) else []
    resultat = rng.choice(["cap"] * 6 + ["correcte", "incorrecte"]) if profile == "random" else "cap"
    d = Diagnosi(
        evidencia="", resum_alumne="",
        estat_passos=[{"pas": s, "estat": estat[s]} for s in ex.step_ids],
        pas_actual=ex.step_ids[0], errors_detectats=errors, error_altre="",
        resultat_proposat=resultat, resultat_justificat=rng.random() < 0.3,
        nivell_desorientacio=des, intencio=intent, teoria_pregunta=[],
    )
    return d, done


def check(ex, teoria, seed: int, torns: int, profile: str) -> list[str]:
    rng = random.Random(seed)
    st = EstatSessio()
    done: set[str] = set()
    out: list[str] = []
    plans = []
    since_target: dict[str, int] = Counter()
    for n in range(1, torns + 1):
        d, done = random_diag(ex, rng, done, profile)
        prev = st
        pla, st = decide(ex, d, st, ["(missatge de l'alumne)"])
        plans.append((pla.accio, pla.pas_objectiu, pla.nivell_pista))
        tag = f"{ex.id} {profile} seed={seed} t={n} {pla.accio}/{pla.pas_objectiu}/{pla.nivell_pista}"
        # I1
        if len(plans) >= 4 and len(set(plans[-4:])) == 1 and pla.accio != "despres_de_tancar":
            out.append(f"I1 same plan 4x: {tag}")
        # I3
        if prev.tancat and pla.accio != "despres_de_tancar":
            out.append(f"I3 reopened after closing: {tag}")
        # I4
        for s, lvl in prev.nivell_per_pas.items():
            if st.nivell_per_pas.get(s, 0) < lvl:
                out.append(f"I4 level decreased on {s}: {tag}")
        # I5
        if pla.accio == "explicar_concepte" and pla.pas_objectiu and st.nivell_per_pas.get(pla.pas_objectiu, 0) > prev.nivell_per_pas.get(pla.pas_objectiu, 0):
            out.append(f"I5 concept question raised the level: {tag}")
        # I6 fallback safety (the question requirement is irrelevant here)
        contingut = allowed_content(ex, pla, st.completats, st.mostrats)
        th = allowed_theory(ex, pla, st.completats, teoria)
        fb = fallback_message(ex, pla, th)
        permeses = [contingut, ex.enunciat_md(), *[t.enunciat for t in th]]
        probs = [p for p in deterministic_check(fb, pla, permeses) if "pregunta" not in p and "massa llarg" not in p]
        if probs:
            out.append(f"I6 fallback fails guard {probs[:2]}: {tag}")
        # I7
        if pla.accio == "mostrar_pas":
            probs = [p for p in deterministic_check(ex.pas(pla.pas_objectiu).detall + " Ho veus?", pla, permeses)
                     if "massa llarg" not in p]
            if probs:
                out.append(f"I7 shown step fails guard {probs[:2]}: {tag}")
        # I2
        if profile == "stuck_trying" and pla.pas_objectiu:
            since_target[pla.pas_objectiu] += 1
            if since_target[pla.pas_objectiu] > 8 and pla.pas_objectiu not in st.mostrats:
                out.append(f"I2 stuck student never shown the step: {tag}")
                break
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--torns", type=int, default=20)
    ap.add_argument("--exercicis", default="")
    args = ap.parse_args()
    teoria = load_teoria()
    _, exercicis = load_llistes(teoria=teoria)
    ids = args.exercicis.split(",") if args.exercicis else list(exercicis)
    viol: list[str] = []
    for ex_id in ids:
        ex = exercicis[ex_id]
        for profile in ("random", "stuck_trying", "beggar"):
            for seed in range(args.seeds if profile == "random" else 2):
                viol += check(ex, teoria, seed, args.torns, profile)
    kinds = Counter(v.split()[0] for v in viol)
    print(f"{len(ids)} exercises, violations: {dict(kinds) or 'none'}")
    seen = set()
    for v in viol:
        key = (v.split()[0], v.split()[1])
        if key not in seen:
            seen.add(key)
            print(" ", v[:300])


if __name__ == "__main__":
    main()
