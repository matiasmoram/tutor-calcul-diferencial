# Cert o fals

Code: `backend/core/quizzes/`. Route: `#/afirmacions`.

## Purpose

A quiz of statements that look true and may not be ("if the iterated limits agree, the double limit exists" is false:
$xy/(x^2+y^2)$). For each one the student decides true or false and justifies it, with a proof or a counterexample.
The point is the justification: the verdict alone is worth 30% of a statement.

## Student flow

1. Pick a source and a difficulty. A source is a whole tema (`tema-2`) or one numbered result or definition of the
   notes (`T2.12`), around which most statements then turn. Difficulty sets the size: `facil` 6, `normal` 8,
   `dificil` 10 statements.
2. Each statement is shown with a short concept label. The student marks `cert` or `fals` and writes a justification.
3. A hint per statement is available on request. It is recorded at once and multiplies that statement's points by
   0.85.
4. The student submits once. The correction shows, per statement, the right verdict, the grade of the justification
   with feedback, the model solution or counterexample, the key ideas the answer contained, the cited items of the
   notes and the sympy checks, both the quiz's own and those run on the student's computations.

## Generation pipeline

`QuizGenerator` (`application/quiz_generator.py`) builds a quiz in rounds:

| Step | Kind | What happens |
|---|---|---|
| Write | LLM, JSON schema | A batch of up to 5 statements, asked for a number of false ones within the bounds the quiz still allows. It sees the notes of the source, the statements already kept, and the rejected ones with their reasons |
| Validate | Code (`domain/services/validation.py`) | Structure, LaTeX, neutral hints, existing citations, duplicates |
| sympy | Code, worker processes | Every check of every statement evaluated; a check that comes out false rejects its statement |
| Verify | 2 LLM calls in parallel | A **blind solver** sees only the statements and decides each verdict with a confidence and whether it is well posed. An **auditor** sees the declared solutions and checks proof or counterexample, cited theory and hint |
| Judge | Code (`domain/services/judging.py`) | Keeps a statement only if the solver reached the same verdict with confidence, found it well posed, and the audit accepted solution, theory and hint |

Rejected statements are replaced, not the whole quiz: the next round asks only for what is missing. Statements that
passed validation and sympy but were not verified yet wait as backups for later rounds, so only as many statements as
the quiz still needs are verified (each verification costs two calls). At most ceil(n/5) + 3 rounds run, all under
`TUTOR_QUIZ_GENERATION_DEADLINE_S` (default 420 s). A truncated output halves the batch and
retries the round; any other unusable output loses that round only. Every round, with its rejections and reasons, is
stored with the quiz.

### What a statement carries

`enunciat`, `veredicte` (`cert` or `fals`), `trampa` (the trap: converse, dropped hypothesis, stronger conclusion,
quantifiers, partial information taken as enough, generalisation, or one of two kinds of true statement), `concepte`,
`contraexemple`, `resolucio`, `idees_clau` (1 to 4, the grading rubric), `pista`, `teoria` (items of the notes, a
closed enum of the numbered items of this tema and earlier ones) and `comprovacions`.

A `comprovacio` is a machine check of a concrete claim in sympy syntax: `limit` (expression, variable, point, side,
value), `no_limit` or `igualtat` (`backend/core/shared/math/sympy_checks.py`). The strings are never evaluated as
Python. Only a whitelist of characters and names reaches sympy's parser, and each check runs in a worker process under
a deadline; a check that times out is `indeterminat`, which does not reject.

## Gates

A statement is rejected if:

- the verdict is not `cert` or `fals`, or a required field is empty, or a false statement has no counterexample;
- it has fewer than 1 or more than 4 key ideas, or more than 4 checks;
- any text has unbalanced `$…$`, uses `$$`, or uses a LaTeX command outside the known vocabulary;
- the hint or the concept label gives the verdict away (they may not say true, false or counterexample);
- it cites an item outside the allowed set, or repeats a statement already in the quiz (accents, case and punctuation
  ignored);
- one of its sympy checks fails;
- the blind solver disagrees, is not confident, or finds it ill-posed, or the audit rejects its solution, theory or
  hint.

The quiz itself must be balanced: at least half the statements false and at least two true.

## Grading and scoring

`AnswersGrader` (`application/answers_grader.py`) runs two model calls in parallel, then sympy, then code:

- The **grader** sees the solutions and judges each justification (`correcta`, `parcial`, `incorrecta`), quoting the
  student's words as evidence for each key idea of the rubric. Another valid counterexample counts.
- The **transcriber** never sees the solutions. It rewrites the concrete computations in the student's answer as sympy
  checks, each with the quote it comes from. If it fails, grading goes on without student checks: they can only lower a
  grade.

Code then decides (`domain/services/scoring.py`):

- The verdict is compared in code. A wrong verdict scores 0, and a justification of the wrong verdict cannot be
  `correcta` or `parcial`.
- A key idea counts only if its quote is really in the answer (spacing, `$`, braces and backslashes ignored), and one
  quote credits one idea. `correcta` with fewer than half the key ideas becomes `parcial`, and `parcial` with none
  becomes `incorrecta`.
- A student check is kept only if its quote is in the answer and states the value being checked, so the transcriber
  cannot silently correct a wrong value. At most 3 per statement run in sympy. A failing one lowers the grade one
  level and adds a note.
- Points per statement: 0.3 for the right verdict plus 0.7 × (1 for `correcta`, 0.5 for `parcial`, 0 otherwise), × 0.85
  if the hint was used. The grade is the mean, from 0 to 100.

A quiz session is graded once. The result reveals every verdict and solution, so later submissions get the stored
result. Grading holds a claim on the session under a 240 s deadline, and a hint request during it is refused.

## Ready pool and generation policy

Quizzes live in the database (`quizzes`), seeded on every start from `backend/generats/afirmacions/<source>/<difficulty>/`.
`POST /api/afirmacions/sessions` serves a stored quiz, avoiding `excepte` when there are others. A new one is
generated only for a caller allowed to (`TUTOR_GENERACIO`, professors only by default), when none is stored or when
it asks with `nova: true`. For anyone else a source and difficulty with nothing stored is a 409. Concurrent requests
for the same source and difficulty share one generation.

## Pre-generation and offline authoring

- Live: `uv run python scripts/pregenerate_afirmacions.py tema-2:normal T2.12:facil` writes verified quizzes to
  `backend/generats/afirmacions/`.
- Offline, with the same gates and code decisions as `QuizGenerator`: `scripts/afirmacions_offline.py`. A batch is one
  quiz's candidate statements in the writer's output format, plus `font`, `dificultat` and `autor`. A batch should
  hold a few more statements than the quiz needs, since rejected ones are dropped.
  - `brief <font> <dificultat> <out.md>` writes the writer's instructions: the generation prompt, the notes of the
    source, the request and the JSON schema.
  - `validate <batch.json>` runs the code validation and every sympy check, and writes nothing.
  - `blind <batch.json>` writes `<batch>.solver.md` (the statements only, for a blind solver) and `<batch>.audit.md`
    (with the declared solutions, for an auditor): two independent reviewers, as in the live pipeline.
  - `import <batch.json>` reads `<batch>.solver.json` and `<batch>.audit.json`, judges every statement with the same
    code as the live pipeline, keeps a balanced quiz of the difficulty's size and saves it under
    `backend/generats/afirmacions/`, recording who wrote and who reviewed it. The next start seeds it into the
    database.

## Data and endpoints

| Endpoint | Body | Returns |
|---|---|---|
| `GET /api/afirmacions/fonts` | — | Temes and focusable items, with stored quizzes per difficulty, and the quiz sizes |
| `POST /api/afirmacions/sessions` | `{font, dificultat, nova, excepte}` | `session_id`, the quiz (statements and concept labels only), `generat_ara`, the focus item |
| `POST /api/afirmacions/sessions/{id}/pista/{statement_id}` | — | The hint |
| `POST /api/afirmacions/sessions/{id}/correccio` | `{respostes: [{id, veredicte, justificacio}]}` | Grade, per-statement results and solutions, cited items of the notes |

Tables: `quizzes`, `quiz_sessions`, `quiz_gradings`. Stages: `quiz_generation`, `quiz_verification` (blind solver),
`quiz_audit`, `quiz_grading`, `quiz_extraction` (transcriber).

## Limits

- A statement is accepted on the agreement of two model passes plus sympy on the concrete computations; a subtle
  error in a proof that both passes miss can survive.
- sympy checks cover limits and identities. They do not prove universally quantified claims, and an undecided check
  does not reject.
- The justification grade is a model's judgement, bounded by code (quoted evidence, rubric coverage, sympy) but not
  replaced by it.
