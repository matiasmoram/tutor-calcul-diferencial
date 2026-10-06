# Spec — "Troba l'error" documents written offline

Project root: `C:/Users/matia/Documents/ProjecteDiferencial`. Python: `.venv/Scripts/python.exe` (prefix commands with
`PYTHONIOENCODING=utf-8`). The live LLM generator is unavailable, so you write the documents it would write. They go
through the same gates: code validation now, and later an independent blind review whose findings are compared in code
(every declared error must be found, and nothing else may be wrong). A document with an accidental extra error, or a
declared error that is not really an error, is REJECTED. Precision matters more than speed.

Read first: `backend/tutor/errades.py` — the prompts `GENERACIO_SYSTEM` (problems) and `GENERACIO_TEORIA_SYSTEM`
(theory) are your instructions; follow them exactly. All text in Catalan.

## Output

One JSON file (a list), the path given in your task. Each document:

```json
{"font": "teoria", "id": "T3.21", "dificultat": "normal", "n_enunciat": 2,
 "fragments": ["...", "..."],
 "errors": [{"fragment": 1, "cita": "...", "tipus": "hipotesi", "explicacio": "...", "correccio": "...", "pista": "..."}]}
```
Problems: `"font": "problema"`, `"id": "t3-5"`, no `n_enunciat`.

- `dificultat`: facil = 1 error, normal = 2, dificil = 3. One error per fragment.
- Error `tipus`: theory ∈ hipotesi, conclusio, quantificador, implicacio, desigualtat, pas_injustificat, cas_oblidat,
  calcul, definicio. Problems ∈ calcul, logica, hipotesi, teorema_mal_aplicat, conclusio, desigualtat.
- `cita` must be copied character-for-character from its fragment (shortest span holding the error, 2–25 words).
- Math: inline `$...$` only, never `$$`. Balanced `$`. In JSON, backslashes are doubled (`"$\\mathbb{R}^n$"`).
  Write the file with Python (`json.dump(..., ensure_ascii=False, indent=1)`) to avoid escaping mistakes.

## Theory documents (source: `backend/teoria/temaN.yaml`)

- Rewrite the item's statement and proof faithfully: same notation, hypotheses and proof structure. You may condense
  routine computations, but no important logical step may disappear (a reviewer compares against the notes, and a
  missing step can read as an error). Long proofs: 6–10 proof fragments, 1–3 sentences each.
- `n_enunciat` = 1–3 statement fragments, then ≥3 proof fragments; total 5–14 fragments.
- ≥1 error in the statement; with ≥2 errors, ≥1 in the proof. A wrong statement must be really FALSE (give a simple
  counterexample in `explicacio` when there is one) or not proved by the given proof — never an equivalent rewording.
- The proof keeps proving the CORRECT statement. If a proof step uses a hypothesis your wrong statement dropped, that
  step is a consequence, not a new error — but prefer statement errors whose consequences don't make other proof steps
  look wrong (e.g. strengthen the conclusion, change a quantifier, open↔closed, strict↔non-strict).
- Variety: across your batch, use different error kinds; don't always drop "de classe $\mathcal{C}^1$".
- Difficulty: facil = visible to someone who knows the statement; normal = needs the role of each hypothesis;
  dificil = subtle (a quantifier, an inclusion, a plausible-looking proof step).

## Problem documents (source: `backend/exercicis/temaN.yaml`)

- The sheet's `passos[].detall` and `resultat` are the correct solution; write a student-style resolution following it,
  5–10 fragments, with the errors placed on purpose (inspired by `errors_comuns`, not copied).
- Everything not declared must be correct and rigorous. Consequences of an error that propagate are NOT new errors,
  but keep propagation short (it makes the blind review ambiguous): prefer errors whose effect is local, or let the
  final conclusion follow consistently from the wrong step.
- Pick exercises with real reasoning (≥3 steps in the sheet); spread them over different problems of the tema.

## Self-check before finishing

1. `PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe scripts/errades_offline.py validate <your file>` → 0 problems.
2. Reread each document as a strict examiner who does NOT know where the errors are: is anything else wrong or
   ambiguous? Fix it. Verify computations with sympy when in doubt (`PYTHONPATH=work/pylib`).
3. Edit only your output file. Final report: number of documents, one line per document (id, difficulty, error
   kinds), and anything you are unsure about.
