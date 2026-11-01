# Troba l'error

Code: `backend/core/mistakes/`. Routes: `#/errades` → `#/errades/problemes` (worked solutions) or
`#/errades/teoria` (results of the notes).

Paths below are relative to the code directory named above, unless they start with `backend/`, `frontend/`,
`scripts/` or `supabase/`.

## Purpose

The student reads a mathematical text with deliberate errors and has to find them and say why they are wrong. Two
activities share the same machinery:

- **Resolucions de problemes**: a worked solution of an exercise of the collection, written from its solution sheet
  and the theory it cites, with errors planted in it.
- **Teoremes i demostracions**: a theorem, proposition, lemma or corollary of the notes that has a proof (59 items),
  rewritten with errors. The statement always carries an error: a dropped or weakened hypothesis, a stronger
  conclusion, a swapped quantifier, the converse…

Difficulty sets the number of errors: `facil` 1, `normal` 2, `dificil` 3.

Each document has a **layout** (`format` in the API), chosen by the student:

| Layout | Label | The student reviews | Correction |
|---|---|---|---|
| `per_parts` | Pas a pas | One flawed part at a time, with the parts before it shown correct | After each part |
| `sencer` | Document sencer | The whole text at once | Once, at the end |

- **Pas a pas** is better for learning. Every error is local and independent of the others, so a mistake never
  makes a later step wrong, and the student gets feedback before the next part. It is the default.
- **Document sencer** is closer to checking a finished exam: the errors sit anywhere in the text and the student
  decides where to look. Only the last error may affect later text (see Gates).
- A problem whose solution sheet has a single step cannot be split into parts: it is offered only as Document
  sencer. The two layouts have separate pools of ready documents.

## Student flow

1. Pick a source, a difficulty and a layout. Sources with a ready document are marked per layout; "Una altra" asks
   for a different document. If the source has none ready in the chosen layout but has in the other, the page
   offers or opens the other one.
2. **Document sencer**: the whole document is shown as numbered paragraphs (for a result of the notes, the
   statement first, then the proof), with the number of errors it contains. The student highlights a span inside
   one paragraph (a formula is selected whole) and writes why it is wrong, as many times as they want, then submits
   once. The correction shows the score, which errors were found, the verdict and feedback on each highlight, and for
   every error its quote, explanation and correction. A missed error first shows only its paragraph, with an optional
   hint and a button to reveal it.
3. **Pas a pas**: the student sees a roadmap with the title of every part and which ones they must review. The first
   flawed part is shown; they highlight and explain inside it only (the earlier parts, shown correct, are context
   and cannot be marked). They can ask for the part's hint, which lowers that part's score. Submitting grades that
   part and shows its error, correction and feedback, then the correct text of the clean parts up to the next flawed
   part, which opens. After the last flawed part comes the final result: the score of each part, the totals and the
   whole correct resolution.
4. In the theory activity, the original item of the notes is shown at the end of either layout. Until then only its
   label is shown: its original statement is the answer key.

## What a part is

A Pas a pas document is the **correct** resolution split into parts; some of them are replaced by a version with
exactly one local error.

- **Problems**: one or two parts per step of the solution sheet, in the sheet's order, titled with the step's title.
- **Theory**: part 1 is the statement ("Enunciat"), followed by 2 to 5 parts of the proof, each with a title.
- Every part has 1 to 4 fragments (the statement, 1 to 3). A document has at least 2 parts.

The parts that get an error are `k = min(errors of the difficulty, parts)`, drawn at random: 1, 2 or 3 for
`facil`, `normal`, `dificil`. For theory the statement is always one of them. The others are drawn among the proof
parts. A problem with fewer parts than the difficulty asks has fewer errors.

## Pipeline

All model stages return JSON validated against a schema, and code decides what is accepted. The static reference
(the sheet and its theory, or the original item) is sent as the request's `context`, so providers cache it across
calls.

### Document sencer (`MistakeExerciseGenerator`)

| Stage | Kind | Input | Output |
|---|---|---|---|
| Generation | LLM | Reference, difficulty, rejection reasons of the previous attempt | Fragments, `n_enunciat` (theory), N errors each with fragment, exact quote, type, explanation, correction, hint |
| Validation | Code (`domain/services/generation_checks.py`) | Draft | Problems, or the document with each quote's character offsets |
| Verification | LLM, independent | Reference and the fragments, **without** the declared errors | Every problem it finds, with fragment, quote and severity (`error`, `consequencia`, `imprecisio`) |
| Comparison | Code (`compare_verification`) | Declared errors and findings | Discrepancies |

On any problem it regenerates with the reasons, three attempts at most, under `TUTOR_MISTAKES_GENERATION_DEADLINE_S`
(default 300 s). Every attempt, with its validation problems, verifier findings and discrepancies, is stored with
the document.

### Pas a pas (`PartedMistakeExerciseGenerator`)

| Stage | Kind | What it does |
|---|---|---|
| A. Correct resolution | LLM writer, code gates (`check_resolution`), blind LLM check | Writes the whole correct resolution in parts. Up to 3 attempts, regenerating with the reasons |
| B. Corruption | LLM corrupter, code gates (`check_corruption`) | For each chosen part, one error as small edits of its correct text, applied by code |
| C. Part check | Blind LLM check, code (`part_verification_problems`) | Checks the corrupted part with the earlier parts as correct context |

Stage A gates, in code:

- the parts follow the sheet's steps in order, at most two per step (theory: 1 to 3 statement fragments, 2 to 5 proof
  parts, each titled), 1 to 4 fragments each, and every fragment renders (non-empty, balanced `$…$`, no `$$`, only
  known LaTeX commands);
- the blind check finds no `error` or `consequencia`, and says the resolution reaches the result (for theory, that it
  proves the whole statement).

Stage B: the corrupter answers `apte` (fit), up to 3 `canvis` (`fragment`, `original`, `nou`), and the error's
`cita`, `tipus`, `explicacio`, `correccio` and `pista`. Code requires that:

- every `original` appears exactly once in its fragment, verbatim, and the edits differ from their text and do not
  overlap;
- the first edit is the error and the later ones are its local consequences, placed after it;
- the edits are small: at most 240 characters and half of the part;
- `nou` carries no marker that gives the error away (`(error)`, "potser", "crec que"…);
- the edited fragments still render, the type is valid for the activity (see Gates) and the four fields are
  non-empty;
- the quote is located on the edited text, on the first edit.

The model does not write the corrupted text: code applies the edits to the correct one, so everything outside the
edits is identical. Each corrupter is told a distinct preferred `tipus`, planned by code before the chains run (for
the theory statement, one of `hipotesi`, `conclusio`, `quantificador`, `implicacio`, `desigualtat`).

Stage C: a verifier that never sees the declared error reads the earlier parts (correct) and the corrupted part. Code
requires that it:

- reports the declared error as an `error` that overlaps the quote, and only one error there;
- reports no other `error`;
- places every `consequencia` after the declared error;
- judges the earlier parts correct (`context_correct`).

The reasons of a rejection go back to stage B.

**Chains and retries.** The k parts are corrupted in parallel, each from the correct text, so their errors never
compound. A chain tries its part up to 3 times (B then C, with the reasons of the last rejection). A part that keeps
failing, or that the corrupter answers is unfit, is swapped for an unused part of the reserve (shared by the
chains). The theory statement is never swapped and cannot be answered unfit: if it fails or the reserve is empty,
the generation fails (502). The whole generation runs under the same deadline as above. Every stage's attempts are
stored with the resolution (stage A) and with each flawed part (B and C).

## Gates

Validation of a Document sencer draft rejects it unless:

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

- every declared error is matched by a finding of severity `error` in the same fragment whose quote overlaps the
  declared one (a different problem in the same fragment does not confirm it). A declared error the reviewer sees
  only as a `consequencia` inherits an earlier error and is rejected;
- no finding of severity `error` is left unmatched: that would be an unintended error. `imprecisio` findings are
  tolerated;
- **errors do not compound**: with two or more errors, no `consequencia` may sit before the last declared error.
  Only the last error in the document may change values or claims used afterwards; the others must leave everything
  after them correct (a true claim with a false justification, a calculation that is not reused).

Pas a pas needs no such rule between errors, because each part is corrupted from the correct text. Its equivalent is
stage C: the part's consequences stay inside the part, after the error.

## Grading and scoring

Code decides where each highlight lands. The candidates are the errors in the same paragraph. A highlight that
overlaps an error's quote finds that error even if the model's verdict says otherwise. It is **exact** when it is not
much longer than the shortest selection covering the quote (at most 3 times as long plus 10 characters), and
**approximate** otherwise. A highlight that overlaps no error counts only if the grader names an error of the same
paragraph; otherwise it is a false positive.

The LLM grades only the student's explanation: `correcta` 1.0, `parcial` 0.6, `incorrecta` 0.35, `absent` 0.3 (finding
the error is worth something on its own, and a wrong reason never scores below no reason). Approximate highlights get
×0.8. Each error keeps its best highlight. Highlights outside the annotatable paragraphs are dropped, and with none
left no model is called.

- **Document sencer**: score = 100 × (sum of the best points / N − 0.1 × false positives), floored at 0. Graded once;
  later submissions get the stored result, which reveals every error.
- **Pas a pas**: each flawed part is graded on its own, with the same rules and N = 1. Only the part's own
  paragraphs can be marked. If the student asked for the part's hint, its score is multiplied by 0.85 (`HINT_FACTOR`)
  and rounded. The overall score is the mean of the part scores, rounded; `trobats`, `total` and
  `falsos_positius` are summed.

Parts are graded in order, each once; a repeated submission for a graded part returns the stored result. A grading
holds a claim on the session (240 s deadline); a concurrent submission gets 409 until it is stored. A hint is
recorded under the same claim, so it cannot land under a running grading.

## Ready pool and generation policy

Verified documents live in the database (`mistake_exercises`) and open without calling a model. The files under
`backend/generats/errades/<source>/<difficulty>/<id>.json` seed it on every start (only ids the database lacks are
imported). Both layouts share the tree; a `"format": "per_parts"` key tells them apart, and a file without it is a
Document sencer.

`POST /api/errades/sessions` picks a random ready document for the source, difficulty and layout, avoiding `excepte`
(the one just seen) when there are others. Only a caller allowed to generate (`TUTOR_GENERACIO=professor`, the
default, means only professors) gets a new document generated, when none is ready or when it asks with `nova: true`.
For anyone else `nova` only picks another ready document, and a source, difficulty and layout with none ready is a
409 that suggests another difficulty. Concurrent requests for the same source, difficulty and layout share one
generation.

## Data and endpoints

The two list endpoints take `?format=sencer|per_parts` (default `sencer`) and count only that layout's documents.

| Endpoint | Body | Returns |
|---|---|---|
| `GET /api/errades/teoria` | — | Results of the notes by topic, with ready documents per difficulty |
| `GET /api/errades/disponibles` | — | `{source id: {difficulty: n}}` of ready documents |
| `POST /api/errades/sessions` | `{exercici_id` or `teoria_id, dificultat, nova, excepte, format}` | `session_id`, `font`, `solucio` (the document), the exercise (`exercici`, `llista`) or the item's label (`teoria`), `generada_ara` |
| `POST /api/errades/sessions/{id}/correccio` | `{anotacions: [{id, fragment, inici, fi, comentari}]}`, at most 40 | Document sencer only: score, found, total, false positives, per-highlight results, the declared errors; for theory, the original item |
| `POST /api/errades/sessions/{id}/parts/{part}/pista` | — | Pas a pas only: `{pista}` |
| `POST /api/errades/sessions/{id}/parts/{part}/correccio` | same as above | Pas a pas only: the part's grading, its correct text, the next part or the final result |

`format` in the session request is `sencer` (default) or `per_parts`. Both POST corrections and the session start are
rate-limited as model calls; the hint is not. The document never contains the errors.

**`solucio` of a Document sencer**: `id`, `font`, `dificultat`, `fragments`, `n_enunciat`, `n_errors`.

**`solucio` of a Pas a pas document**: `id`, `font`, `dificultat`, `format: "per_parts"`, `n_enunciat`, `n_errors`,
`parts` (`[{part, titol, revisar}]`, the roadmap) and `actual`, the first part to review:
`{part, primer_fragment, fragments, anteriors}`. `fragments` is the part's text with its error; `anteriors` is
`[{part, fragments}]` with the correct text of the clean parts before it. Fragments are numbered across the whole
document, `primer_fragment` being the number of the part's first one, and annotations use those numbers.

**Part correction** (`.../parts/{part}/correccio`): `part` must be a flawed part and the next one not yet graded. The
response has the grading JSON of Document sencer restricted to the part (`nota`, `trobats`, `total`,
`falsos_positius`, `anotacions`, `errors`, `resum`, `crida`) plus `part`, `correcte` (the part's correct fragments)
and:

- `seguent`: the next part to review, in the shape of `actual`; `null` after the last one;
- `final`, after the last one only: `{nota, trobats, total, falsos_positius, parts: [{part, nota, pista}], resolucio:
  [{part, fragments}], original?}`. `resolucio` is the whole correct resolution; `original` (theory) is the item of
  the notes.

A part with nothing marked is graded 0 with no model call.

**Errors**: 404 unknown session, part without an error, or document; 409 a grading running for the session, a part
sent out of order, a session of the other layout (each layout is graded only through its own endpoints), or nothing
ready; 422 per_parts for a problem with a single step, or an invalid source or annotation; 502 failed generation; 504
grading deadline.

## Storage

| Table | Holds |
|---|---|
| `mistake_exercises` | The document (JSON) and its `layout` (`sencer` by default) |
| `mistake_sessions` | The session, its `layout`, and the claim of a grading in progress |
| `mistake_gradings` | The one grading of a Document sencer session |
| `mistake_part_gradings` | The grading of each part of a Pas a pas session (one per `(session_id, part)`): annotations and result, with `hint_used` |
| `mistake_part_hints` | The parts whose hint was asked, one row per `(session_id, part)` |

The `layout` columns and the two part tables come from `supabase/migrations/20261031000000_mistake_parts.sql`. Model
calls are logged under the stages `mistakes_generation` (writer and corrupter), `mistakes_verification` (all blind
checks) and `mistakes_grading`.

## Pre-generation and offline authoring

Both workflows write the same files under `backend/generats/errades/`, which are committed.

- **Live**: `uv run python scripts/pregenerate_errades.py [--format sencer|per_parts] <source id>:<difficulty> …`
  (ids starting with `T` are results of the notes; difficulty defaults to `normal`; `--format` defaults to `sencer`).
  For example:
  `uv run python scripts/pregenerate_errades.py t3-10:normal t2-4c:facil T3.21:dificil` and
  `uv run python scripts/pregenerate_errades.py --format per_parts t3-10:normal T3.21:dificil`.
  It prints each document's attempts per stage, calls, tokens and cost, and continues past a failed one.
- **Offline**, with the same gates and no live call: `uv run python scripts/errades_offline.py <command> …`. The
  script's docstring has the file formats.
  - Document sencer: `brief <font> <id> <dificultat> <out.md>` writes the writer's instructions; `validate <batch.json>`
    runs the code validation; `blind <batch.json>` writes `<batch>.blind.md` for an independent reviewer, with the
    documents **without** their errors; `import <batch.json>` reads the reviewer's `<batch>.ver.json`, applies
    `compare_verification` and saves only the documents that pass, with the hash of their reference.
  - Pas a pas, in the order of the stages. The correct resolutions are in `<batch>.net.json`:
    `brief-net <font> <id> <out.md>`, then `validate-net <batch>.net.json` (stage A gates), `blind-net
    <batch>.net.json` (writes `<batch>.net.blind.md`; the reviewer answers `<batch>.net.ver.json`).
    `assign <batch>.net.json <dificultat> [--seed N]` picks the parts to corrupt like the live generator, adds the
    document to `<batch>.json` and writes a corruption brief per document. After the writer fills `corrupcions`,
    `validate <batch>.json` (stage B gates), `blind <batch>.json` (writes `<batch>.blind.<j>.md`, one reviewer per file,
    answers in `<batch>.ver.<j>.json`) and `import <batch>.json`, which saves a document only if its resolution
    passes stage A and every flawed part B and C.
  - `check-cache` (the default command) re-validates every document of both layouts in `backend/generats/errades/`
    against the current sheets and notes, re-applies the verification gates to its stored reviews, and reports
    documents whose reference changed since import. It never deletes.

## Limits

- Validity rests on one independent model pass per document (per part in Pas a pas): an error both models miss, or
  an ambiguous one the verifier accepts, can survive. Offline batches use a reviewer of the author's choice under the
  same blind rule.
- Pas a pas guarantees independent errors by construction. Document sencer does it only through the verifier, so a
  dependence the verifier misses can survive.
- The grader judges explanations in free text; only placement and arithmetic are deterministic.
- A problem with a single-step solution sheet is not available as Pas a pas.
- Live generation takes minutes and costs money, which is why students are served from the ready pool.
