# Tutor socràtic · Càlcul Diferencial (prototip)

Demo of a Socratic tutor for every problem of the Càlcul Diferencial collection (Temes 1–6, FME-UPC). The tutor knows the course notes and cites them ("pel Teorema 12 del Tema 3"). The student picks an exercise, explains what they did, and the tutor guides them without giving away the solution. The "Panell del professor" shows every internal decision the system makes.

## Run

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env   # then put your ANTHROPIC_API_KEY in .env
.\run.ps1                # http://127.0.0.1:8000
```

Tests (no API calls, scripted fake LLM): `.\.venv\Scripts\python.exe -m pytest tests -q`

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

## Files

| Path | What |
|---|---|
| `backend/exercicis/temaN.yaml` | Solution sheets, one list per tema: steps (objective / idea / detail / theory), common errors with Socratic questions, leak regexes |
| `backend/teoria/temaN.yaml` | Course notes transcribed to Markdown + LaTeX, one item per numbered Definició/Teorema/… (`T3.12`) |
| `backend/tutor/teoria.py` | Loads the notes; theory references (`T3.12`, `T3.12+dem` = with proof) |
| `backend/tutor/schemas.py` | Structured-output schemas per stage |
| `backend/tutor/politica.py` | Deterministic policy + what content the reply stage may see |
| `backend/tutor/guardia.py` | Deterministic output checks |
| `backend/tutor/prompts.py` | Catalan system prompts |
| `backend/tutor/pipeline.py` | The turn loop (diagnosis → policy → reply → guard) |
| `frontend/` | Static UI (KaTeX), chat + professor panel |

## "Troba l'error" mode (`#/errades`)

Two activities on the same machinery (`backend/tutor/errades.py`); `#/errades` lets the student choose:

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

- Live: `python scripts/pregenerate_errades.py t3-10:normal T3.21:dificil ...` (ids starting with `T` are theory).
- Offline (written by an agent or by hand, same gates): `scripts/errades_offline.py validate|blind|import <batch.json>`.
  `blind` writes the documents without their declared errors for an independent reviewer, `import` compares that review
  in code (`compare_verification`) and caches only what passes; `check-cache` re-validates the whole cache. Specs:
  `work/SPEC_errades.md` (authoring) and `work/SPEC_errades_review.md` (blind review).

## "Cert o fals" mode (`#/afirmacions`)

A quiz of statements about one tema (or centred on one result of the notes, e.g. `T2.12`): the student decides
true / false and justifies it, a proof or a counterexample ("iterated limits agree ⇒ double limit exists" is false:
$xy/(x^2+y^2)$). 6 / 8 / 10 statements for fàcil / normal / difícil. `backend/tutor/afirmacions.py`:

1. **Generation (LLM, structured):** batches of up to 5 statements, each with verdict, trap type, model proof or
   counterexample, key ideas (grading rubric), a Socratic hint, cited theory (closed enum) and sympy checks of the
   counterexample's computations. At least half are false, at least two true.
2. **Validation (code + CAS):** LaTeX, duplicates, a hint that doesn't name the verdict; every sympy check is
   evaluated (`backend/tutor/comprovacions.py`, whitelisted parser, worker processes under a deadline). A failing
   check rejects the statement.
3. **Verification (2 LLMs in parallel):** a blind solver that only sees the statements decides each verdict; an
   audit sees the solutions and checks proofs, counterexamples, theory and hints. Code keeps a statement only if the
   blind verdict matches with confidence and the audit accepts it. Rejected statements are replaced with the
   reasons (not the whole quiz), up to 3 extra rounds.
4. **Grading (LLM + CAS + code):** the verdict is graded by code. The LLM judges the justification against the
   rubric (another valid counterexample counts) and transcribes the student's own computations as sympy checks;
   a failing one lowers the grade. Score: 30% verdict + 70% justification, ×0.85 if the hint was used.

Quizzes are cached in `backend/generats/afirmacions/<font>/<difficulty>/`. Pre-generate with
`python scripts/pregenerate_afirmacions.py tema-2:normal T2.12:facil ...`. Stages `afirmacions_generacio`,
`afirmacions_verificacio`, `afirmacions_auditoria`, `afirmacions_correccio` (override with `TUTOR_MODEL_<STAGE>`).

## Photo of the notebook

Students can attach a photo (button, paste, or drag and drop) instead of typing. The browser shrinks it to 1800 px JPEG, and `POST /api/sessions/{id}/transcripcio` runs a vision stage (`tutor/transcripcio.py`, structured output: transcription, legibility, content type, doubts). The transcriber is told to copy **literally**, without fixing mistakes, so the diagnosis still sees them. The transcription is placed in the text box for the student to review and correct, then sent as a normal message tagged `origen: "foto"` (shown in the professor panel).

## Navigation

`#/` landing (choose a mode) → `#/exercicis` (tutor) → `#/exercicis/<list>/<exercise>`; `#/errades` (find the error) → `#/errades/teoria[/<item>]` or `#/errades/problemes` → `#/errades/<list>/<exercise>`. Old `#/problemes` and `#/llista/...` links still work. Hash routes, so the browser back button works.

## Adding an exercise or a list

Each YAML file in `backend/exercicis/` is one list (one tema): a `llista:` header (`id: tema-N`, `etiqueta`, `titol`, `tema`, `tipus`, `format`) plus `problemes`, each with its shared statement (`preambul`) and one sheet per sub-part (`exercicis`, ids like `t2-4c`). Sheets are authored in chunks under `work/fitxes/` and merged with `python scripts/merge_fitxes.py`; `python scripts/check_fitxes.py [chunk.yaml --tema N]` validates them. See `work/PLA.md` and `work/SPEC_wave2.md`.

## Course theory

`backend/teoria/temaN.yaml` holds the notes split into numbered items (the notes use one shared counter per tema, so `T3.12` is unambiguous). Sheets cite items, never whole PDFs: a turn carries 2–6 items (~1k tokens on average) instead of a whole tema (~15–20k).

- `teoria` (exercise level): definitions the statement relies on; shown to the student under the statement from the first turn.
- `passos[].teoria`: results a step uses. Naming a theorem names the strategy, so the reply stage only sees a step's theory from hint level 2 (the same gate as the step's idea).
- `teoria_reservada`: items that solve this very exercise (a worked example in the notes). Items whose `problemes` field cites the problem are reserved automatically. Only the diagnosis and the guard see them.
- Citations are links: the reply cites items as «<Tipus> <n> del Tema <m>» and the chat turns every such citation into a link that opens the original PDF at that item's page in a new tab (`/pdf/...#page=N`; the app serves `sources/`). The `#/teoria` page lists every tema with its PDF and an index of all numbered items, each linking to its page; the problem collection PDF is linked there too.
- On a conceptual question the diagnosis picks up to 2 items from the sheet or the tema's index; the reply explains them and cites them. The reply returns `referencies` (closed enum of the items it was shown); the UI renders them as expandable cards, and the guard rejects wrong citations (`cita_teoria_incorrecta`).

## Prompt caching and token budget

The static part of the diagnosis and guard prompts (sheet + theory + tema index) is passed as `context=` and goes first: an explicit `cache_control` block for Anthropic, an identical prefix for OpenAI/Gemini automatic caching. `CallMeta.cached_tokens` and the professor panel show cache hits. `PYTHONPATH=work/pylib python scripts/token_budget.py` builds the real prompts over a simulated session and counts tokens (tiktoken).

Sheet tests check that (1) each step's leak regexes catch that step's own worked detail, (2) no level-1/2 hint text (objective, idea) contains its own banned content, and (3) no hint text reveals the final result.

## Models

`LLM_PROVIDER` in `.env` selects `anthropic`, `gemini` or `openai`; both go through the same structured-output contract.

- Gemini (default per stage): diagnosis `gemini-3.5-flash`, reply `gemini-3.5-flash-lite`, guard `gemini-3-flash-preview`. Different models per stage because free-tier quotas are per model. The free tier allows about 5 requests/min and 20 requests/day per model; each turn uses 3+ requests. Enable billing for a real demo.
- OpenAI: diagnosis `gpt-5.5`, reply and guard `gpt-5.4-mini`. Tested live: about 5–8 s per turn.
- Anthropic: `claude-opus-5-5` for all stages.

Override any stage with `TUTOR_MODEL_<STAGE>` (see `.env.example`). `scripts/live_demo.py` runs a scripted 4-turn conversation against the real API and prints the trace.


## Visual lab (`#/visual`)

Interactive figures of the theory, frontend only (`frontend/visual.js` core, `visual-labs-a.js` temes 1–3,
`visual-labs-b.js` temes 4–6). Students type their own function or pick an example from the notes; every lab
cites its items (links to the PDF) and has a "Teoria relacionada" button with the statements.

| Lab | Tema | What it shows |
|---|---|---|
| `normes` | 1 | Unit balls of the p-norms, equivalence constants |
| `punt-fix` | 2 | Cobweb of $x_{n+1}=g(x_n)$, contraction constant, $k^n$ rate |
| `grafica` | 2 | Surface + level sets $C_k(f)$ in 3D and as a contour map |
| `limits` | 2 | Limits along $y=mx$ / $y=mx^2$, plus $\sup_{\|x\|=r}\|f-L\|$ to tell candidate from proof |
| `gradient` | 3 | Directional derivative as a slice, tangent plane, $
abla f$ ⟂ level curve, $D_uf$ vs angle |
| `diferenciabilitat` | 3 | Zoom to the tangent plane, remainder $E(r)$; classic counterexamples |
| `inversa` | 4 | Grid deformation by $F$, sign of $\det JF$, fold curve, $DF(a)$ vs $F$ on a small square |
| `implicita` | 4 | Curve $F=0$, local graph $y=g(x)$, $g'=-F_x/F_y$, vertical tangents and singular points |
| `taylor` | 5 | Taylor polynomial of order 1–3 over $f$, error slope $ho^{r+1}$ |
| `extrems` | 5 | Critical points (Newton), Hessian, Sylvester, eigenvalues, quadratic approximation |
| `lagrange` | 6 | Point moving on $g=0$ with $
abla f$, $
abla g$; candidates of $
abla f=\lambda
abla g$ and singular points |
| `varietats` | 6 | Surfaces $\Phi=0$ in $\mathbb{R}^3$, tangent plane, normal, tangent projection of $
abla f$, level surface tangency |

Libraries (lazy-loaded from cdnjs only when a lab opens): **Plotly.js 3** (WebGL surfaces, contours, isosurfaces)
and **math.js 14** (parsing + symbolic derivatives; numeric central differences as fallback). math.js installs a
global `math`, which would shadow app.js's KaTeX `math()`: `loadVisLibs()` takes its instance and restores it.
Colors come from the CSS tokens (light/dark); surfaces use a single-hue sequential scale, signed values
($\det JF$) a diverging one. Numerical verdicts (differentiable, limit exists, …) are labelled as numerical.

## Hardening (2026-10)

- **Policy = explicit state machine** (`backend/tutor/politica.py`): one escalation rule for every action, session facts
  (closed, steps shown, errors seen, repetitions, result confirmed, student attempts), no yes/no oracle for bare guesses,
  terminal closing, anti-gaming (help requests without an attempt climb at half speed; the full step only after an attempt;
  `demanar_intent` asks for a concrete micro-attempt), empathetic tone for frustration, MathDial teacher-move tags.
  Invariants are tested in `tests/test_politica.py`.
- **Guard**: regexes (spelling) + **sympy math-provenance check** (`backend/tutor/cas.py`): a reply formula equivalent to
  forbidden content (result, unopened steps) is rejected whatever its notation, unless it comes from allowed content,
  the statement, the theory shown or the student's own words. `python scripts/check_cas.py` self-tests it on all sheets.
- **Reply in plain text** (no JSON): LaTeX survives; references are extracted from the citations it writes.
- **Roles**: set `TUTOR_CLAU_PROFESSOR` and open the app once with `?prof=<key>`; without the key students get only the
  chat (no solution, no trace). With no key configured the app runs in open demo mode.
- **Conversation log** in `backend/registres/*.jsonl` and a professor review page at `#/professor` (flags: fallbacks,
  rejected drafts, loops, steps shown, frustration).
- **Simulated students**: `python scripts/simulate.py --mostra 40 --workers 4` (misconception personas from each sheet,
  lost / guesser / answer-beggar / silent / injector / persuader / extractor archetypes; completion, loops, fallback,
  level-aware leak judge, cost). Model study: `scripts/model_study.py` (recommended: gpt-5.4-mini for all stages).
