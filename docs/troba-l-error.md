# Troba l'error

Code: `backend/core/mistakes/`. Routes: `#/errades` → `#/errades/problemes` (worked solutions) or
`#/errades/teoria` (results of the notes).

## Purpose

The student reads a mathematical text with deliberate errors and has to find them and say why they are wrong. Two
activities share the same machinery:

- **Resolucions de problemes**: a worked solution of an exercise of the collection, written from its solution sheet
  and the theory it cites, with errors planted in it.
- **Teoremes i demostracions**: a theorem, proposition, lemma or corollary of the notes that has a proof (59 items),
  rewritten with errors. At least one error is in the statement (a dropped or weakened hypothesis, a stronger
  conclusion, a swapped quantifier, the converse…) and, with two or more errors, at least one is in the proof.

Difficulty sets the number of errors: `facil` 1, `normal` 2, `dificil` 3.

## Student flow

1. Pick a source and a difficulty. Sources with a ready document are marked; "Una altra" asks for a different one.
2. The whole document is shown as numbered paragraphs (for a result of the notes, the statement first, then the
   proof), with the number of errors it contains. For a result of the notes, only its label is shown: its original
   statement is the answer key.
3. The student highlights a span inside one paragraph (a formula is selected whole) and writes why it is wrong, as
   many times as they want, then submits once.
4. The correction shows the score, which errors were found, the verdict and feedback on each highlight, and for every
   error its quote, explanation and correction. A missed error first shows only its paragraph, with an optional hint
   and a button to reveal it. In the theory activity the original item of the notes is shown at the end.

## Pipeline

| Stage | Kind | Input | Output |
|---|---|---|---|
| Generation | LLM, JSON schema | Reference (sheet and its theory, or the original item), difficulty, rejection reasons of the previous attempt | Fragments, `n_enunciat` (theory), N errors each with fragment, exact quote, type, explanation, correction, hint |
| Validation | Code (`domain/services/generation_checks.py`) | Draft | Problems, or the document with each quote's character offsets |
| Verification | LLM, JSON schema, independent | Reference and the fragments, **without** the declared errors | Every problem it finds, with fragment, quote and severity (`error`, `consequencia`, `imprecisio`) |
| Comparison | Code (`compare_verification`) | Declared errors and findings | Discrepancies |
| Grading | LLM, JSON schema | Reference, the document with its declared errors, the located highlights | Per highlight: which error it means, explanation grade, feedback |
| Scoring | Code (`domain/services/grading.py`) | Located highlights and the grader's report | Score and per-highlight points |

`MistakeExerciseGenerator` runs generation → validation → verification → comparison, and on any problem regenerates
with the reasons, three attempts at most, under `TUTOR_MISTAKES_GENERATION_DEADLINE_S` (default 300 s). Every attempt,
with its validation problems, verifier findings and discrepancies, is stored with the document. The static reference
is sent as the request's `context`, so providers cache it across attempts and gradings.

## Gates

Validation (code) rejects a draft unless:

- it has 4 to 14 non-empty fragments (the prompt asks for 5 to 10), with balanced `$…$`, no `$$`, and no LaTeX
  command outside the known vocabulary, in the fragments or in any error field;
- it declares exactly N errors, at most one per fragment, each with a type valid for the activity and a non-empty
  explanation, correction and hint;
- every quote appears literally in its fragment;
- for a result of the notes: 1 to 3 statement fragments leaving at least 3 for the proof, at least one error in the
  statement, and at least one in the proof when N ≥ 2.

Error types: `calcul`, `logica`, `hipotesi`, `teorema_mal_aplicat`, `conclusio`, `desigualtat` for solutions;
`hipotesi`, `conclusio`, `quantificador`, `implicacio`, `desigualtat`, `pas_injustificat`, `cas_oblidat`, `calcul`,
`definicio` for results of the notes.

Verification (code on the blind reviewer's findings) requires that:

- every declared error is matched by a finding of severity `error` or `consequencia` in the same fragment whose quote
  overlaps the declared one (a different problem in the same fragment does not confirm it);
- no finding of severity `error` is left unmatched: that would be an unintended error. `imprecisio` findings are
  tolerated.

## Grading and scoring

Code decides where each highlight lands. The candidates are the errors in the same paragraph. A highlight that
overlaps an error's quote finds that error even if the model's verdict says otherwise. It is **exact** when it is not
much longer than the shortest selection covering the quote (at most 3 times as long plus 10 characters), and
**approximate** otherwise. A highlight that overlaps no error counts only if the grader names an error of the same
paragraph; otherwise it is a false positive.

The LLM grades only the student's explanation: `correcta` 1.0, `parcial` 0.6, `incorrecta` 0.35, `absent` 0.3 (finding
the error is worth something on its own, and a wrong reason never scores below no reason). Approximate highlights get
×0.8. Each error keeps its best highlight. Score = 100 × (sum of the best points / N − 0.1 × false positives), floored
at 0. Highlights that land on no paragraph are dropped, and with none left no model is called.

A session is graded once. Its grading is stored, and later submissions get the stored result: the correction reveals
every error. A grading holds a claim on the session (240 s deadline); a concurrent submission gets 409 until it is
stored.

## Ready pool and generation policy

Verified documents live in the database (`mistake_exercises`) and open without calling a model. The files under
`backend/generats/errades/<source>/<difficulty>/` seed it on every start (only ids the database lacks are imported).

`POST /api/errades/sessions` picks a random ready document for the source and difficulty, avoiding `excepte` (the one
just seen) when there are others. Only a caller allowed to generate (`TUTOR_GENERACIO=professor`, the default, means
only professors) gets a new document generated, when none is ready or when it asks with `nova: true`. For anyone
else `nova` only picks another ready document, and a source and difficulty with none ready is a 409 that suggests
another difficulty. Concurrent requests for the same source and difficulty share one generation.

## Pre-generation and offline authoring

- Live: `uv run python scripts/pregenerate_errades.py t3-10:normal t2-4c:facil T3.21:dificil` (ids starting with `T`
  are results of the notes) writes verified documents to `backend/generats/errades/`.
- Offline, with the same gates: `scripts/errades_offline.py`.
  - `brief <font> <id> <dificultat> <out.md>` writes the writer's instructions: the generation prompt, the reference,
    the request and the JSON schema of a batch document.
  - `validate <batch.json>` runs the code validation.
  - `blind <batch.json>` writes `<batch>.blind.md` for an independent reviewer: the verifier's instructions and the
    documents **without** their declared errors, next to their reference.
  - `import <batch.json>` reads the reviewer's `<batch>.ver.json`, applies `compare_verification`, and saves only the
    documents that pass, with the hash of their reference.
  - `check-cache` re-validates every document in `backend/generats/errades/` against the current sheets and notes and
    re-applies the verification gate to its stored review, reporting documents whose reference changed since import.

## Data and endpoints

| Endpoint | Body | Returns |
|---|---|---|
| `GET /api/errades/teoria` | — | Results of the notes by topic, with ready documents per difficulty |
| `GET /api/errades/disponibles` | — | `{source id: {difficulty: n}}` of ready documents |
| `POST /api/errades/sessions` | `{exercici_id` or `teoria_id, dificultat, nova, excepte}` | `session_id`, the document (fragments, `n_enunciat`, `n_errors`, never the errors), the exercise or the item's label, `generada_ara` |
| `POST /api/errades/sessions/{id}/correccio` | `{anotacions: [{id, fragment, inici, fi, comentari}]}`, at most 40 | Score, found, total, false positives, per-highlight results, the declared errors; for theory, the original item |

Both POST endpoints are rate-limited as model calls. Tables: `mistake_exercises`, `mistake_sessions`,
`mistake_gradings`. Stages: `mistakes_generation`, `mistakes_verification`, `mistakes_grading`.

## Limits

- Validity rests on one independent model pass: an error both models miss, or an ambiguous one the verifier accepts,
  can survive. Offline batches add a reviewer of the author's choice under the same blind rule.
- The grader judges explanations in free text; only placement and arithmetic are deterministic.
- Live generation takes minutes and costs money, which is why students are served from the ready pool.
