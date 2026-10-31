# Tutor socràtic

Code: `backend/core/tutoring/` (use cases, policy, guard) on top of `backend/core/course/` (the authored content).
Route: `#/exercicis` → `#/exercicis/<list>/<exercise>`.

## Purpose

The student works on one exercise of the problem collection and explains, in their own words or with a photo of the
notebook, what they have done. The tutor answers with a question or a hint at the right level, grounded in the course
notes, and never hands over the solution sheet. The hard rules (what may be said, when the result may be confirmed,
when a full step may be shown) are code; the model only reads the student and phrases the reply.

## Student flow

1. Pick a list (one per tema) and an exercise. The statement is shown with its background theory: the items of the
   notes the statement relies on, never the ones that solve it.
2. Write a message, or attach a photo (button, paste or drag and drop). The browser scales the photo to 1800 px, the
   transcription stage copies it literally (mistakes included), and the student reviews the text before sending it.
3. Each reply may cite items of the notes («Teorema 12 del Tema 3»). The chat turns every citation into a link to the
   item's page in the PDF, and the cited items come back as cards.
4. The conversation ends when the student reaches the result with a justification: the session then stays closed.

## Pipeline

One turn is one call of `TurnHandler.handle` (`application/turn_handler.py`).

| Stage | Kind | Sees | Produces |
|---|---|---|---|
| Diagnosis | LLM, JSON schema (`infra/llm_schemas.py`) | Full sheet, every item it cites, the tema's index, session state, conversation | `Diagnosis`: state of each step, current step, mistakes from the sheet's catalogue (or `altre` with a description), proposed result, whether it is justified, disorientation, intent, up to 2 theory items for a conceptual question, literal evidence |
| Policy | Code (`domain/services/policy.py`) | Diagnosis, session state, the student's own messages | `Plan` (action, target step, hint level, tone, forbidden patterns and formulas) and the next `SessionState` |
| Content gate | Code (`allowed_content`, `allowed_theory`) | Plan | The only solution text and theory items the reply may use |
| Reply | LLM, plain text | Plan, released content and theory, conversation, rejection reasons of the previous draft | Draft message |
| Guard, code | Code (`domain/services/guard.py`) | Draft, plan, permitted texts | List of problems |
| Guard, judge | LLM, JSON schema | Full sheet, plan, released content, draft | `GuardVerdict`: `ok` or `rebutjat` with violations |

The diagnosis and judge schemas are built per exercise, so step and mistake ids are closed enums: the model cannot
name a step the sheet does not have. The static part of their prompts (sheet, theory, index) is sent as a separate
`context` block first, which providers serve from their prompt cache.

### Policy

An explicit state machine over the session (actions in `domain/values/plan.py`): `pista`, `questionar_error`,
`questionar_resultat`, `demanar_justificacio`, `demanar_raonament`, `demanar_intent`, `demanar_conclusio`,
`validar_i_avancar`, `explicar_concepte`, `mostrar_pas`, `mostrar_conclusio`, `tancar`, `despres_de_tancar`,
`redirigir`. Each action carries a teacher-move tag (MathDial taxonomy) for the professor view. Its invariants, each
with a test (`backend/tests/core/tutoring/test_policy*.py`, plus a fuzzer in `policy_fuzzer.py`):

- **One escalation rule.** The hint level of a step starts from the student's disorientation (1 on track, 2 stuck or
  lost) and rises when a hint produced no progress. Level 3 is the top of the ladder; level 4 (`mostrar_pas`) shows
  the full step only after the student has tried something.
- **Evidence.** A step counts as completed only in a message that shows work, and only up to the current target: the
  diagnosis' word alone is not evidence.
- **No oracle.** A bare guess without reasoning is neither confirmed nor denied.
- **Result gate.** The result may be acknowledged only once the student's own text contains it (by its leak patterns
  or a sympy-equivalent formula).
- **Anti-gaming.** Requests for help without any attempt climb the ladder at half speed; `demanar_intent` asks for a
  concrete first attempt.
- **Terminal closing.** `tancar` needs reasoning in the message; after it the session stays closed.
- **No dead end.** A mistake repeated at the top of the ladder, or a request for the solution after an attempt, shows
  the step.

### Content gate

Per target step: level 1 releases the step's objective, level 2 adds the strategy idea and the theory the step cites,
level 3 adds the worked detail. Completed and already shown steps are always released. The final result is released
only when the plan allows stating it. Items listed in `teoria_reservada` (and any item of the notes whose `problemes`
field cites this problem) solve the exercise outright: only the diagnosis and the judge see them.

### Guard

Code checks run first, each one a rejection reason fed back to the writer:

- the sheet's leak regexes for the result and for the steps the plan does not open;
- sympy equivalence: a formula in the draft equivalent to forbidden content (the result, unopened steps) is rejected
  whatever its notation, unless it comes from permitted text (released content, statement, released theory, the
  student's own words) (`backend/core/shared/math/latex_cas/`);
- LaTeX commands KaTeX would not render, a missing closing question when the plan requires one, too many sentences;
- citations of items outside the released set.

Only a draft that passes all of them goes to the LLM judge, which checks leaks, exceeding the hint level, doing the
student's work, false mathematics, not following the action, not answering the student, wrong citations, language,
and obeying the student against the plan. A rejected draft is rewritten with the reasons, three drafts at most. If none passes, the student
gets an authored fallback built from the sheet (`domain/services/fallback.py`).

Failures close: a judge error or invalid output rejects the draft, and a sympy check that exceeds 20 s rejects it too.

## Atomicity and concurrency

- A turn first claims the session; a second message while one is running gets 409 before any model is called. A
  claim older than the turn deadline plus 60 s is taken over.
- The whole turn runs under a 300 s deadline (504 past it). The session is saved only when the turn completed, with
  an optimistic version check, so on any failure the stored session is unchanged and the student can resend.
- A diagnosis truncated at its token limit is asked once more; both calls are in the trace.

## Professor view

With the professor key (`?prof=<key>` once, then stored in the browser and sent as `X-Clau-Professor`):

- Starting a session also returns the sheet's outline, the result, the professor note and every theory item the
  sheet cites, marked reserved or not.
- Each turn returns the full `TurnTrace`: diagnosis, plan, released content and theory, every draft with its code
  problems and judge verdict, previous and new state, and every model call with tokens and latency. Students get only
  `{"fallback": true|false}`.
- `#/professor` lists sessions with flags (fallbacks, rejected drafts, loops, steps shown, frustration) and replays any
  session turn by turn.

## Solution sheet format

`backend/exercicis/temaN.yaml` holds one list: a `llista` header and `problemes`, each with a shared statement
(`preambul`) and one sheet per part in `exercicis` (ids like `t2-4c`). Fields of a sheet:

| Field | Use |
|---|---|
| `enunciat` | Statement shown to the student |
| `teoria` | Background items (`T2.3`; `T2.3+dem` includes the proof), shown from the first turn |
| `teoria_reservada` | Items that solve the exercise; never released to the reply |
| `resultat.valor`, `resultat.fuites` | The result and the regexes that detect it in a reply |
| `passos[]` | Steps: `id`, `titol`, `objectiu` (level 1), `idea` (level 2), `detall` (level 3), `teoria`, `fuites` |
| `errors_comuns[]` | Catalogued mistakes: `id`, `descripcio`, and a Socratic `pregunta` |
| `nota_professor` | Shown to professors only |

The notes are in `backend/teoria/temaN.yaml`, one entry per numbered item (`T3.12`: tipus, num, nom, enunciat,
demostracio, pagina…). A turn carries the few items the sheet cites, not a whole tema.

Authoring checks: `uv run python scripts/check_fitxes.py` (structure, references, leak patterns, LaTeX; also run in
CI), and `backend/tests/core/course/test_authored_content.py`, which checks on every sheet that each step's leak
regexes catch its own detail, that no level-1 or level-2 text contains banned content, and that no hint reveals the
result. `uv run python scripts/check_cas.py` self-tests the sympy leak checker over every sheet.

## Data and endpoints

| Endpoint | Body | Returns |
|---|---|---|
| `POST /api/sessions` | `{exercici_id}` | `session_id`, exercise, list, background theory (+ professor fields) |
| `POST /api/sessions/{id}/missatges` | `{text, origen: "text" or "foto"}`, at most 4000 characters | `{missatge, referencies, trace}` |
| `POST /api/sessions/{id}/transcripcio` | `{imatge: "data:image/...;base64,..."}`, body up to 10 MB | transcription, legibility, content type, doubts, call usage |
| `GET /api/professor/sessions` | — | session summaries with flags (professor only) |
| `GET /api/professor/sessions/{id}` | — | every turn with its trace (professor only) |

Tables: `tutor_sessions` (history, policy state, version, turn claim), `tutor_turns` (student text, reply, origin,
trace), `transcriptions`, and `llm_calls` for every model call.

Stages: `diagnosis`, `reply`, `guard`, `transcription`, each with its own model, effort and token cap
(`TUTOR_MODEL_<STAGE>`, `TUTOR_EFFORT_<STAGE>`).

## Evaluation

- `uv run python scripts/eval/smoke_turn.py [exercise] ["message" ...] --trace`: real turns against the configured
  provider, printing diagnosis, plan and drafts.
- `uv run python scripts/eval/simulate.py --mostra 40`: an LLM student plays personas against the real use cases:
  a student who sincerely holds one of the sheet's catalogued mistakes, plus competent, lost, guessing, answer-begging,
  silent, instruction-injecting and solution-extracting students. A separate judge flags leaks, and code decides what counts as one; the summary reports
  completion, loops, fallbacks and leaks with confidence intervals.
- `uv run python scripts/eval/model_study.py`: fixed scripted conversations under several model configurations.

## Limits

- The tutor is as good as its sheet: steps, leak patterns and catalogued mistakes are authored by hand, and a
  mistake outside the catalogue is only described by the diagnosis (`altre`).
- The sympy leak check abstains on formulas its parser cannot read; the regexes and the judge remain.
- Replies are not streamed: the student sees a reply only after the guard approved it.
