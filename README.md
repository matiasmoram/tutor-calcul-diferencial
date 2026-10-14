# Tutor socràtic · Càlcul Diferencial (prototip)

Demo of a Socratic tutor for every problem of the Càlcul Diferencial collection (Temes 1–6, FME-UPC). The tutor knows the course notes and cites them ("pel Teorema 12 del Tema 3"). The student picks an exercise, explains what they did, and the tutor guides them without giving away the solution. The "Panell del professor" shows every internal decision the system makes.

## Run

```powershell
uv sync                  # Python 3.13 + dependencies into .venv (https://docs.astral.sh/uv/)
copy .env.example .env   # then put your API key in .env
uv run uvicorn apps.tutor_api.server:app --reload --port 8000   # http://127.0.0.1:8000  (or: make run)
```

Checks (no API calls, scripted fake LLM, a throwaway SQLite database per test): `make check`, or `uv run pytest -q`,
`uv run ruff check backend scripts`, `uv run pyright`. Deploy: `DEPLOY.md`.

## How one turn works

```
student message
   │
   ▼
1. DIAGNOSI (LLM, structured output)     sees: full solution sheet + conversation
   JSON schema with closed enums built from the sheet: step states, current step,
   detected common errors, proposed result (correct/incorrect), disorientation
   level (en_cami / dubte_puntual / encallat / perdut), intent, literal evidence.
   │
   ▼
2. POLÍTICA (plain Python, deterministic)
   Decides the action (pista, qüestionar_error, validar_i_avançar, mostrar_pas, …),
   the target step and the hint level 1–4. Hint levels escalate per step and are
   capped; the full step (level 4) is shown only after level 3 AND an explicit request.
   Completed steps are tracked across turns in session state.
   │
   ▼
3. RESPOSTA (LLM, structured output)     sees: ONLY the content the plan allows
   Level 1 = step objective, 2 = + strategy idea, 3–4 = + worked detail.
   Later steps and the final result are never in its prompt, so it cannot leak them.
   │
   ▼
4. GUARDIÀ
   a) deterministic: leak regexes from the sheet, required closing question, length
   b) LLM judge with the full solution: leaks, exceeding hint level, doing the
      student's work, false maths, language
   Rejected → rewrite with the reasons (max 3 drafts) → else a safe authored fallback.
   Fail-closed: if the judge errors, the draft is rejected.
```

## Architecture

DDD + Clean Architecture, Python backend in the house style of the Prosper backends. Rules: `backend/AGENTS.md`;
history of the migration: `work/ARQUITECTURA.md`.

| Path | What |
|---|---|
| `backend/core/course/` | Course content: topics, theory items (`T3.12`, `T3.12+dem` = with proof), problem sheets, exercises with their hidden solution sheets |
| `backend/core/tutoring/` | The tutor: diagnosis → deterministic policy (`domain/policy.py`) → reply → guard (`domain/guard.py`), photo transcription, sessions |
| `backend/core/mistakes/` | "Troba l'error" |
| `backend/core/quizzes/` | "Cert o fals" |
| `backend/core/counterexamples/` | "Construeix el contraexemple" (sympy only, no model) |
| `backend/contraexemples/reptes.yaml` | Counterexample challenges, each with an authored example and its certificates |
| `backend/core/shared/` | Ids and exceptions, the LLM port + provider clients + call log, async SQLModel storage, CAS / sympy checks |
| `backend/apps/tutor_api/` | FastAPI app (composition root): endpoints, response schemas, dependency providers |
| `backend/exercicis/temaN.yaml` | Solution sheets, one list per tema: steps (objective / idea / detail / theory), common errors with Socratic questions, leak regexes |
| `backend/teoria/temaN.yaml` | Course notes transcribed to Markdown + LaTeX, one item per numbered Definició/Teorema/… |
| `backend/generats/` | Pre-generated "troba l'error" documents and quizzes (seed of the database) |
| `scripts/` | Authoring checks, pregeneration, simulation, model study, database utilities |
| `frontend/` | Static UI (KaTeX), chat + professor panel |

Every context is `domain/` (pure) → `application/` (one use case per file) → `infra/` (LLM adapters, SQLModel
repositories). Everything persistent lives in the database (`DATABASE_URL`; local SQLite by default), including the
log of every model call (`llm_calls`).

## "Troba l'error" mode (`#/errades`)

Two activities on the same machinery (`backend/core/mistakes`); `#/errades` lets the student choose:

- **Teoremes i demostracions** (`#/errades/teoria/<item>`): a theorem / proposition / lemma / corollary of the notes
  (every numbered result that has a proof, 59 items) rewritten with errors. At least one error is in the **statement**
  (a dropped or weakened hypothesis, a stronger conclusion, a swapped quantifier, the converse, open↔closed...) and,
  with 2+ errors, at least one in the **proof** (a step that doesn't follow, a missing case...). The original item of the
  notes is the reference for generation, verification and grading; the student sees it only after the correction.
- **Resolucions de problemes** (`#/errades/problemes` → `#/errades/<tema>/<exercise>`): a "bad resolution" of an
  exercise of the collection, built from its current solution sheet and the theory it cites.

The student highlights spans on the document, comments each one and submits once:

1. **Generation (LLM, structured):** 5–14 fragments (theory: `n_enunciat` statement fragments, then the proof) and
   exactly N errors (1/2/3 by difficulty), each with an exact quote, type, explanation, fix and a Socratic hint.
2. **Validation (code):** error count, one error per fragment, every quote found literally in its fragment (character
   offsets stored), balanced `$`, no `$$`, error types of the activity; theory: statement/proof split, ≥1 error in the
   statement, ≥1 in the proof when N ≥ 2.
3. **Verification (LLM, independent):** a second pass that never sees the declared errors lists every problem it finds
   (`error` / `consequencia` / `imprecisio`). Code requires that every declared error is found and that nothing else is
   wrong; otherwise the generator retries with the reasons (max 3 attempts).
4. **Grading (LLM + code):** code decides where each highlight lands (character overlap → exact / approximate, only
   errors in the same fragment are candidates); the LLM only judges the student's explanation (correct / partial / wrong /
   missing) and writes feedback. The score is computed in code. One correction per document (a resubmission returns the
   same result: the correction reveals every error).

The static reference (sheet or original item) is sent as `context=`, so providers cache it across attempts and gradings.

**Ready pool.** Verified documents are cached in `backend/generats/errades/<exercise or item>/<difficulty>/` and open
instantly; lists show which ones are ready (`GET /api/errades/disponibles`, `GET /api/errades/teoria`). "Una altra"
picks a different cached document, or generates a new one when there is no other.

- Live: `uv run python scripts/pregenerate_errades.py t3-10:normal T3.21:dificil ...` (ids starting with `T` are theory).
- Offline (written by an agent or by hand, same gates): `scripts/errades_offline.py validate|blind|import <batch.json>`.
  `blind` writes the documents without their declared errors for an independent reviewer, `import` compares that review
  in code (`compare_verification`) and caches only what passes; `check-cache` re-validates the whole cache. Specs:
  `work/SPEC_errades.md` (authoring) and `work/SPEC_errades_review.md` (blind review).

## "Cert o fals" mode (`#/afirmacions`)

A quiz of statements about one tema (or centred on one result of the notes, e.g. `T2.12`): the student decides
true / false and justifies it, a proof or a counterexample ("iterated limits agree ⇒ double limit exists" is false:
$xy/(x^2+y^2)$). 6 / 8 / 10 statements for fàcil / normal / difícil. `backend/core/quizzes`:

1. **Generation (LLM, structured):** batches of up to 5 statements, each with verdict, trap type, model proof or
   counterexample, key ideas (grading rubric), a Socratic hint, cited theory (closed enum) and sympy checks of the
   counterexample's computations. At least half are false, at least two true.
2. **Validation (code + CAS):** LaTeX, duplicates, a hint that doesn't name the verdict; every sympy check is
   evaluated (`backend/core/shared/math/sympy_checks.py`, whitelisted parser, worker processes under a deadline). A failing
   check rejects the statement.
3. **Verification (2 LLMs in parallel):** a blind solver that only sees the statements decides each verdict; an
   audit sees the solutions and checks proofs, counterexamples, theory and hints. Code keeps a statement only if the
   blind verdict matches with confidence and the audit accepts it. Rejected statements are replaced with the
   reasons (not the whole quiz), up to 3 extra rounds.
4. **Grading (2 LLMs + CAS + code):** the verdict is graded by code. A grader judges the justification and quotes
   the student's words as evidence for each key idea of the rubric (another valid counterexample counts); code
   credits only quotes really in the answer, one idea per quote, and caps "correcta" at "parcial" below half the
   ideas. In parallel, a transcriber that never sees the solutions writes the student's computations as sympy
   checks; code keeps those whose quote is in the answer and whose value the quote states (so a grader cannot
   silently "fix" a wrong value), and a failing one lowers the grade. Score: 30% verdict + 70% justification,
   ×0.85 if the hint was used.

Quizzes are cached in `backend/generats/afirmacions/<font>/<difficulty>/`. Pre-generate with
`uv run python scripts/pregenerate_afirmacions.py tema-2:normal T2.12:facil ...`. Stages `quiz_generation`,
`quiz_verification`, `quiz_audit`, `quiz_grading`, `quiz_extraction` (override with `TUTOR_MODEL_<STAGE>`).

## "Construeix el contraexemple" mode (`#/contraexemples`)

The student builds the pathological function. A challenge asks for $f$ with properties at the origin that look
incompatible (partials but not continuous; every line agrees but there is no limit; differentiable but not $C^1$;
crossed second derivatives that differ…). The student writes $f(x,y)$ off the origin, $f(0,0)$, and a **certificate**
for each property that needs one. No model is called: every verdict is computed (`backend/core/counterexamples`).

- **Only one-variable limits are trusted.** sympy's two-variable limits are unsound: with the angle left free, the
  polar limit of $x^2y/(x^4+y^2)$ is 0, but the limit does not exist. Partial and directional derivatives are limits of
  difference quotients in $h$, iterated limits are two one-variable limits, and a path $(x(t),y(t))$ reduces $f$ to $t$.
- **Negative properties need paths** ("the limit does not exist": two paths with different limits, or one without a
  limit). "Not differentiable" is often decided with no certificate: a missing partial, or a directional derivative
  that is not $\nabla f\cdot v$.
- **Positive properties need a radial bound** $G(r)$ ("continuous": $|f-f(0,0)|\le G(r)$; "differentiable": the same
  for the remainder). $G\to0$ is checked exactly. The inequality is sampled on a polar grid, with angles that hug the
  axes so that a parabola like $y=x^2$ is caught; the verdict is therefore **plausible**, not proved.
- Statuses: `ok` (exact), `plausible` (sampled), `falla` (the property is shown false for this f, or f is not a
  real function off the origin), `indeterminat` (shown as "No demostrat": sympy cannot decide, or the certificate is
  missing or proves nothing). Only `ok` and `plausible` pass.
- **Tied to the notes** (`backend/teoria`). Each challenge cites the items it is about (`teoria`, shown under the
  statement). `teoria_propietats` maps each property to its definition, and a failed property shows it as "Repassa".
  `teoria_reservada` lists items that already contain such a counterexample (e.g. Observació 17 del Tema 3); they are
  shown only with the author's example. Hints and explanations cite the notes, and the citations become links to the
  PDF page. The server refuses to start if a cited item does not exist (`SpecCatalog.check_theory`).
- Hardened against a simulated student trying to game the checker (two rounds). Inputs are parsed without evaluation;
  nested exponentials and huge powers are rejected. sympy's "no limit" counts only after retrying on rewritten forms
  and seeing a spread that does not shrink. Equality is exact, with no tolerance. f must be real off the origin, which
  is checked with a 4096-angle sweep and with sign changes of the denominator. Positive properties are also checked
  exactly along rays and along every path in the submission.
- Each property runs in its own worker of the server's `SympyCheckPool` (`map`), under the pool's deadline.
- Challenges: `backend/contraexemples/reptes.yaml`. Each has an authored example with its certificates; the tests run
  every example through the checker. A student sees the example only after passing; professors always see it.
- Endpoints: `GET /api/contraexemples`, `GET /api/contraexemples/{id}`, `POST /api/contraexemples/{id}/comprova`.

## Photo of the notebook

Students can attach a photo (button, paste, or drag and drop) instead of typing. The browser shrinks it to 1800 px JPEG, and `POST /api/sessions/{id}/transcripcio` runs a vision stage (stage `transcription` in `backend/core/tutoring`, structured output: transcription, legibility, content type, doubts). The transcriber is told to copy **literally**, without fixing mistakes, so the diagnosis still sees them. The transcription is placed in the text box for the student to review and correct, then sent as a normal message tagged `origen: "foto"` (shown in the professor panel).

## Navigation

`#/` landing (choose a mode) → `#/exercicis` (tutor) → `#/exercicis/<list>/<exercise>`; `#/errades` (find the error) → `#/errades/teoria[/<item>]` or `#/errades/problemes` → `#/errades/<list>/<exercise>`. Old `#/problemes` and `#/llista/...` links still work. Hash routes, so the browser back button works.

## Adding an exercise or a list

Each YAML file in `backend/exercicis/` is one list (one tema): a `llista:` header (`id: tema-N`, `etiqueta`, `titol`, `tema`, `tipus`, `format`) plus `problemes`, each with its shared statement (`preambul`) and one sheet per sub-part (`exercicis`, ids like `t2-4c`). Sheets are authored in chunks under `work/fitxes/` and merged with `uv run python scripts/merge_fitxes.py`; `uv run python scripts/check_fitxes.py [chunk.yaml --tema N]` validates them. See `work/PLA.md` and `work/SPEC_wave2.md`.

## Course theory

`backend/teoria/temaN.yaml` holds the notes split into numbered items (the notes use one shared counter per tema, so `T3.12` is unambiguous). Sheets cite items, never whole PDFs: a turn carries 2–6 items (~1k tokens on average) instead of a whole tema (~15–20k).

- `teoria` (exercise level): definitions the statement relies on; shown to the student under the statement from the first turn.
- `passos[].teoria`: results a step uses. Naming a theorem names the strategy, so the reply stage only sees a step's theory from hint level 2 (the same gate as the step's idea).
- `teoria_reservada`: items that solve this very exercise (a worked example in the notes). Items whose `problemes` field cites the problem are reserved automatically. Only the diagnosis and the guard see them.
- Citations are links: the reply cites items as «<Tipus> <n> del Tema <m>» and the chat turns every such citation into a link that opens the original PDF at that item's page in a new tab (`/pdf/...#page=N`; the app serves `sources/`). The `#/teoria` page lists every tema with its PDF and an index of all numbered items, each linking to its page; the problem collection PDF is linked there too.
- On a conceptual question the diagnosis picks up to 2 items from the sheet or the tema's index; the reply explains them and cites them. The reply returns `referencies` (closed enum of the items it was shown); the UI renders them as expandable cards, and the guard rejects wrong citations (`cita_teoria_incorrecta`).

## Prompt caching and token budget

The static part of the diagnosis and guard prompts (sheet + theory + tema index) is passed as `context=` and goes first: an explicit `cache_control` block for Anthropic, an identical prefix for OpenAI/Gemini automatic caching. `CallMeta.cached_tokens` and the professor panel show cache hits. `PYTHONPATH=work/pylib uv run python scripts/token_budget.py` builds the real prompts over a simulated session and counts tokens (tiktoken).

Sheet tests check that (1) each step's leak regexes catch that step's own worked detail, (2) no level-1/2 hint text (objective, idea) contains its own banned content, and (3) no hint text reveals the final result.

## Models

`LLM_PROVIDER` in `.env` selects `anthropic`, `gemini` or `openai`; both go through the same structured-output contract.

- Gemini (default per stage): diagnosis `gemini-3.5-flash`, reply `gemini-3.5-flash-lite`, guard `gemini-3-flash-preview`. Different models per stage because free-tier quotas are per model. The free tier allows about 5 requests/min and 20 requests/day per model; each turn uses 3+ requests. Enable billing for a real demo.
- OpenAI: diagnosis `gpt-5.5`, reply and guard `gpt-5.4-mini`. Tested live: about 5–8 s per turn.
  Production overrides (measured 2026-10, see `render.yaml` / DEPLOY.md): `gpt-5.6-luna` for diagnosis, reply, guard
  (effort `none`), transcription and both gradings, at ~1/5 the cost of `gpt-5.4-mini` (per 1M tokens in/out: luna
  0.20/1.20, mini 0.75/4.5, gpt-5.5 5/30). Generation/verification keep the defaults: `gpt-5.4-mini` there truncated
  quiz generation at `max_tokens` and emitted NUL bytes in the JSON. Do not set a global `TUTOR_MODEL` in production.
  Measured with luna: a tutor turn ~$0.0037; generating a "Troba l'error" document ~$0.003–0.009 (3/4 succeeded) and a
  "Cert o fals" quiz ~$0.034–0.047 in 2–4 min (3/4, one truncated), mathematically correct 24/24 but with LaTeX
  corruption that the generation gates now reject. Live generation is professor-only by default (`TUTOR_GENERACIO`).
- Anthropic: `claude-opus-5-5` for all stages.

Override any stage with `TUTOR_MODEL_<STAGE>` / `TUTOR_EFFORT_<STAGE>` (stages `diagnosis`, `reply`, `guard`, `transcription`, `mistakes_*`, `quiz_*`; see `.env.example`). `scripts/live_demo.py` runs a scripted 4-turn conversation against the real API and prints the trace.


## Visualitzador (`#/visual`)

Three tools for the exercises, frontend only (`frontend/visual.js` core, `visual-eines.js` tools,
`visual-latex.js` statement reader):

| Tool | Route | For |
|---|---|---|
| Explorador f(x,y) | `#/visual/explorador` | Surface + contour map; click a point for f, ∇f, tangent plane, Hessian; critical points (classified); constraints/regions (`x^2+y^2 <= 1`, one per line, `<` = open boundary) with candidates for absolute extrema: interior points, Lagrange points on each boundary, corners, singular points; max/min, or sup/inf not attained on open boundaries; compactness check |
| Anàlisi en un punt | `#/visual/punt` | Limit along y−b = m(x−a)^k as a function of m, sup of \|f−L\| on circles, directional derivatives by the definition vs ∇f·u, tangent-plane remainder E(r); value f(a) settable for piecewise functions |
| Canvis de variables | `#/visual/canvis` | Grid deformation by F, sign of det JF, fold curve, F vs DF(a) on a small square |

**From an exercise:** the statement gets a "📈 Visualitza" button when `extractVisual()` can read a function
from its LaTeX (f(x,y)=…, `\lim_{(x,y)\to(a,b)}`, `cases` with the special point, maps F=(F1,F2), regions
`\{(x,y)\mid …\}`, bare constraints). It opens the right tool in a new tab with the functions filled in; 121 of
the 333 statements are readable (the rest are proofs or have no concrete function). Results that would give the
exercise away (critical points, candidates, conclusions) stay behind a click.

Libraries, lazy-loaded from cdnjs: **Plotly.js 3** and **math.js 14** (parsing, symbolic derivatives; numeric
central differences as fallback). math.js installs a global `math`, which would shadow app.js's KaTeX `math()`:
`loadVisLibs()` takes its instance and restores it. Verdicts are numerical and say so.

## Hardening (2026-10)

- **Policy = explicit state machine** (`backend/core/tutoring/domain/policy.py`): one escalation rule for every action, session facts
  (closed, steps shown, errors seen, repetitions, result confirmed, student attempts), no yes/no oracle for bare guesses,
  terminal closing, anti-gaming (help requests without an attempt climb at half speed; the full step only after an attempt;
  `demanar_intent` asks for a concrete micro-attempt), empathetic tone for frustration, MathDial teacher-move tags.
  Invariants are tested in `tests/test_politica.py`.
- **Guard**: regexes (spelling) + **sympy math-provenance check** (`backend/core/shared/math/latex_cas.py`): a reply formula equivalent to
  forbidden content (result, unopened steps) is rejected whatever its notation, unless it comes from allowed content,
  the statement, the theory shown or the student's own words. `uv run python scripts/check_cas.py` self-tests it on all sheets.
- **Reply in plain text** (no JSON): LaTeX survives; references are extracted from the citations it writes.
- **Roles**: set `TUTOR_CLAU_PROFESSOR` and open the app once with `?prof=<key>`; without the key students get only the
  chat (no solution, no trace). With no key configured the app runs in open demo mode.
- **Conversation log** in `backend/registres/*.jsonl` and a professor review page at `#/professor` (flags: fallbacks,
  rejected drafts, loops, steps shown, frustration).
- **Simulated students**: `uv run python scripts/simulate.py --mostra 40 --workers 4` (misconception personas from each sheet,
  lost / guesser / answer-beggar / silent / injector / persuader / extractor archetypes; completion, loops, fallback,
  level-aware leak judge, cost). Model study: `scripts/model_study.py` (see Models above).
