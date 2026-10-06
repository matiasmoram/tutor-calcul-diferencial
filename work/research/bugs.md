# Logic-bug audit: tutor socràtic (state machine, invariants, guard interactions)

Date: 2026-10-06. Scope: `backend/tutor/*.py`, `backend/app.py`, `frontend/app.js`, `frontend/errades.js`,
`scripts/check_fitxes.py`, `tests/test_harness.py`, plus the sheets and theory data.
No project file was edited. Throwaway reproductions are in `work/research/scratch/`:

- `policy_loops.py`: synthetic `Diagnosi` sequences through `decide()` (cases A–O below)
- `pipeline_state.py`: `Tutor.turn()` with a scripted fake LLM (fallback and exception paths)
- `data_stats.py`: sheet and theory data invariants
- `errades_grade.py`: grading edge cases in "Troba l'error"

Run them with `PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe work/research/scratch/<file>`.
The baseline test suite passes (1025 tests).

**[V]** = verified by running code. **[R]** = found by reading the code (not executed).

---

## HIGH

### H1. A correct but unjustified result locks the session into `demanar_justificacio` [V]
**Where:** `politica.py:170-176` (branch precedence), `schemas.py:413-416` (field scope), `prompts.py:17-18`.

**Repro (`policy_loops.py` case A, t2-4c):** for every turn the diagnosis says `resultat_proposat="correcte"`, with intent `proposa_resultat`, then `demana_pista`, `demana_solucio`, `frustracio`, then a completed step, then `pregunta_conceptual`. Six turns produce `demanar_justificacio` at level 1, and `nivell_per_pas` stays at 1 the whole time. In practice:
- a new completed step is never validated (no `validar_i_avancar`);
- a request for the solution never reaches `mostrar_pas`;
- a conceptual question is never answered;
- the hint level never rises.

**Root cause:** two causes stack up.
1. The diagnosis prompt limits `errors_detectats` to the last message. It does not limit `resultat_proposat` / `resultat_justificat` that way (they describe the whole conversation). Once the student has said the value, every later diagnosis keeps reporting `correcte`.
2. In `decide()`, the result branches (`questionar_resultat`, `demanar_justificacio`) come before every step-level branch. They are terminal: they never escalate, and they hide the student's intent.

This is the same bug class as the one just fixed (no escalation without "stuck"), in a branch the fix did not touch.

**Fix (root cause):**
- Make "the student already stated the correct value" a session fact. Add `EstatSessio.resultat_dit: bool`, set once.
- Scope `resultat_proposat` in the schema to the last message.
- `demanar_justificacio` should change the plan, not replace it. Set `allow_result` and add a justification instruction, but run the normal step machine underneath (pista with escalation, `validar_i_avancar`, `mostrar_pas`, `explicar_concepte`). The target is still the first pending step, which is exactly the justification that is missing.

### H2. The result works as a yes/no oracle, worse since "answers phrased as questions" were fixed [V]
**Where:** `politica.py:39,42` (INSTRUCCIONS `demanar_justificacio` "Reconeix que el valor és bo", `questionar_resultat` "Digues-li que no és correcte"), `prompts.py:18`.

**Repro (case O):** turn 1 is "És 1?", which gives `incorrecte`, then `questionar_resultat`, and the tutor says it is wrong. Turn 2 is "És 0?", which gives `correcte`, then `demanar_justificacio`, and the tutor confirms the value. On yes/no and existence problems ("existeix el límit?") one guess is enough.

**Root cause:** the policy grades a bare guess on correctness alone. Whether the student gave any reasoning (`resultat_justificat`, `evidencia`, step states) plays no part. The diagnosis change made guesses phrased as questions count as proposals, which turned this into a cheap oracle.

**Fix:** treat an unjustified proposal the same whether it is right or wrong. Use one neutral action, "how would you show it?", aimed at the first pending step. Reveal correctness only when there is reasoning to judge: `resultat_justificat`, or at least one step `en_curs`/`completat` that supports the proposal. **This is a product decision. Ask Matías.**

### H3. `questionar_error` and `questionar_resultat` never escalate, and the fallback repeats word for word [V]
**Where:** `politica.py:140-168`, `pipeline.py:44-49`.

**Repro (cases B and C):** the same catalogued error four times, with `demana_pista` / `perdut`, gives `questionar_error` at **level 0** four times. Each turn's fallback is the identical `pregunta_suggerida`. A wrong result repeated four times gives `questionar_resultat` at level 1 four times.

**Root cause:** escalation (`stuck` / `no_progress`) exists only in the final `else` (pista) branch. Every other action that targets a step copies `current` (or `max(current, 1)`). Also, `RESPOSTA_SYSTEM:41` ("no repeteixis una pista… aporta-hi un element nou") pushes the reply model past the fixed level. The guard then rejects the draft (`excedeix_nivell_pista`) and the fallback repeats.

**Fix:** compute the hint level once, before choosing the action, with one escalation rule shared by all step-targeted actions. Track repeated errors in the state (`errors_vistos: dict[id, n]`). After N repeats of the same error, attach the step's idea or detail to `questionar_error` (level ≥ 2), or switch to a pista on the step where the error occurs.

### H4. The deterministic regexes veto content the plan explicitly allows [V]
**Where:** `politica.py:95-114` (`_forbidden_regexes`).

**Repro:**
- **`mostrar_pas` is impossible in 22 (exercise, step) pairs.** In these, a *later* step's leak regex matches the target step's own `detall` (`data_stats.py`). Examples: t5-14/`signe_phi` (vetoed by `classificar`'s "màxim local estricte"), t1-7d/`frontera` (`[0,1]`), t6-3a/`existencia` (`x^2\le3`), t1-8c/d/e, t2-14c, t3-3, t5-7b, t5-15a, t6-3e. A verbatim `mostrar_pas` reply is rejected (case L). The guard therefore *always* ends at the fallback for the one action the student explicitly asked for.
- **A step completed out of order cannot be validated.** In case G (t2-4c), with `candidat` and `concloure` completed, the target is `acotar`. The `concloure` detail is in the allowed content, but restating it is vetoed by `acotar`'s regex.
- **The student's own words are vetoed too.** If a student writes the bound inside a wrong derivation, the reply cannot quote it. The LLM guard explicitly allows "repetir el que l'alumne ja ha dit"; the regex layer contradicts it.

**Root cause:** `_forbidden_regexes` already removes *result* regexes that match content the reply may show, but it does not do the same for *step* regexes (later steps, and the target below level 3). The "don't veto what is allowed" invariant is applied to only one of the two regex families.

**Fix:**
1. Build `allowed_texts` once: the details of completed steps, the target's detail at level ≥ 3, and possibly the student's own messages.
2. Drop *any* regex (result or step) that matches an allowed text.
3. Add a `check_fitxes` rule: no later-step regex may match an earlier step's `detall`. That way sheets also get fixed at the source; some of these regexes are simply too broad, such as `[0,1]`.

### H5. `tancar` does not end the session; the next turn gives hints on step 1 [V]
**Where:** `politica.py:117-245` (`state.tancat` is never read; `tancat=pla.accio=="tancar"` overwrites it), `pipeline.py`, `app.js` (input never disabled).

**Repro (case D):**
1. Turn 1: correct and justified, so `tancar`. `completats=[]` (the diagnosis didn't mark the steps), `tancat=True`.
2. Turn 2: "gràcies" gives `pista` on `candidat`, level 1, `tancat=False`.
3. Turn 3: a restatement of the result without justification gives `demanar_justificacio`.

The result regexes are vetoed again even though the tutor itself has just said the result.

**Root cause:** the state has no terminal state. `tancar` does not normalise the state (it doesn't mark all steps completed, and the "result revealed" fact isn't kept).

**Fix:** in `decide()`, if `state.tancat`, use a post-close action. It allows the result, gives no hints, and offers the next exercise or a review. Keep `tancat` sticky. On `tancar`, set `completats = all steps`. In the UI, show the closed state.

### H6. Fallbacks use up hint levels the student never received [V]
**Where:** `pipeline.py:152-156` (`s.estat = nou_estat` is committed whatever the outcome), `pipeline.py:44-53`.

**Repro (`pipeline_state.py` case I):** the guard rejects every draft for four turns. The plan goes pista 2, pista 3, pista 3, then `mostrar_pas` 4. All four replies are the same generic "Centrem-nos en el pas següent: …". The student reaches level 4 eligibility, and `nivell_per_pas = 4` is recorded, without ever seeing the idea, the detail or the step.

**Root cause:** `nivell_per_pas` records the level that was *planned*, not the level that was *delivered*. The fallback is level-agnostic.

**Fix:** pick one.
- (a) On fallback, commit the state with the step's previous level (keep the completion updates from the diagnosis).
- (b) Better: make the fallback authored content *at the planned level*: objective at 1, idea at 2, detail at 4. This is safe once H4 is fixed. Then the level that was given really was given.

---

## MEDIUM

### M1. A conceptual question raises the hint level and opens the step's strategy [V]
**Where:** `politica.py:186-193` (`nivell_pista=max(current, 2)`), `politica.py:221` (`no_progress`), `politica.py:287-289`.

**Repro (case E):** turn 1, "què vol dir que existeixi el límit?", gives `explicar_concepte` at level 2. `allowed_content` now includes the step's *idea*, and `allowed_theory` the step's theorem. Turn 2, an ordinary message (step `en_curs`), gives pista at **level 3** (detail).

`teoria_extra` (chosen by the diagnosis from the sheet plus the tema index) can also be a later step's theorem. That bypasses the level ≥ 2 gate on step theory. Example: "quin teorema hauria de fer servir?" names the strategy.

**Root cause:** an action that isn't a hint writes into the hint ladder (`nivell_per_pas`, `ultim_pas`).

**Fix:** `explicar_concepte` keeps `nivell_pista=current`. Its content is `teoria_extra` only, with no idea. It doesn't update `nivell_per_pas` or `ultim_pas`. Filter `teoria_extra` against the theory of the target and later steps unless the level is ≥ 2.

### M2. The no-progress escalation ignores partial progress and counts turns that weren't hints [V]
**Where:** `politica.py:221-222`.

**Repro (case F):** a student who is `en_cami` and whose step is `en_curs` (working through a long calculation) gets levels 1, 2, 3 in three messages. Redirect turns (`redirigir`, which sets `pas_objectiu=target`) and question turns also count as "no progress".

**Root cause:** progress is measured only by newly *completed* steps. `ultim_pas` is written by every action, not only by hints.

**Fix:**
- Escalate only when the previous action on that step was a hint (`state.ultima_accio == "pista"`), and the step's state didn't improve (no_iniciat → en_curs → completat).
- Store the previous step states in `EstatSessio`.
- `ultim_pas` should be set only by hint actions.

### M3. Level-3 plateau, and `mostrar_pas` doesn't move the session forward [V]
**Where:** `politica.py:195-227`.

**Repro:**
- Case H: `frustracio` + `perdut` for five turns gives levels 2, 3, 3, 3, 3. `mostrar_pas` needs the intent `demana_solucio`, so a frustrated or lost student never gets the step.
- After `mostrar_pas`, the student says "d'acord, i ara?". The step isn't completed, because the diagnosis only counts what the student *wrote*. The result is a pista at level 3 on the step that was just shown, while `nivell_per_pas` stays at 4.

**Root cause:** the state has no notion of "step shown by the tutor". The trigger for `mostrar_pas` depends on a single intent label.

**Fix (needs a product decision):**
- Allow `mostrar_pas` after k turns at level 3 with stuck or frustration signals.
- Record `mostrats: list[str]`. Treat a shown step as resolved for targeting, so the next target is the following step. Optionally ask the student to restate it, at most once.

### M4. `tancar` takes precedence over detected errors [V]
**Where:** `politica.py:130` comes before `politica.py:140`.

**Repro (case K):** `resultat_proposat="correcte"`, `resultat_justificat=True` and `errors_detectats=["camins_com_a_prova"]` give `tancar`, which congratulates a proof by paths.

**Root cause:** the policy trusts `resultat_justificat` even when the same diagnosis reports an error.

**Fix:** if `errors_detectats` is not empty, treat the diagnosis as not justified (normalise it in `normalize_diagnosi`), or move the error branch above `tancar`.

### M5. Contradictions in the diagnosis are never reconciled [V/R]
**Where:** `schemas.py:458-465` (`normalize_diagnosi`), `politica.py`.

- `pas_actual` is never used. If it disagrees with `estat_passos`, nobody notices. [R]
- A step marked `erroni` with no error id gives a plain hint. The error is ignored. [R]
- Case M: a wrong result after all steps are completed gives `questionar_resultat` with `pas_objectiu=None`. The instruction says "pregunta-li per revisar el pas objectiu" and there is none. [V]
- Case N: `errors_detectats=["altre"]` with an empty `error_altre` gives `questionar_error` with no error text in the allowed content. The reply has to question an error it is never told about. [V]

**Fix:** enforce invariants in `normalize_diagnosi`, and record the contradictions in the trace:
- `pas_actual` must equal the first step that isn't completed;
- `altre` requires a non-empty `error_altre` (otherwise drop it);
- an `erroni` step with no error gives `altre`, with the step named.

In `questionar_resultat` with no target, use the action wording for "review the conclusion".

### M6. An exception mid-turn leaves the history inconsistent, and a judge JSON error escapes fail-closed [V]
**Where:** `pipeline.py:115-150`, `llm.py:170,244,314` (`json.loads`), `app.py:168-191`.

**Repro (`pipeline_state.py`):**
- J1: a provider SDK exception in the reply stage (e.g. a rate limit, which is not an `LLMError`) leaves `historial == ['alumne']` with `torns == 0`. When the student resends, the conversation has two student messages in a row.
- J2: the judge returns invalid JSON. `json.JSONDecodeError` is not caught by `except (LLMError, ValidationError)`, so it escapes `turn()`, and `_call_llm` turns it into a 500 error.

**Root cause:** only the diagnosis stage rolls back. JSON parse errors are not wrapped in `LLMError` in `llm.py`.

**Fix:**
- Make the turn transactional: snapshot `historial` and `estat`, and restore both on *any* exception.
- In `llm.py`, wrap the `json.loads` and provider errors in `LLMError` (keeping the status for the HTTP mapping).
- Treat any judge failure as a rejection.

### M7. Citation extraction attaches the wrong theory item [V]
**Where:** `teoria.py:381-396` (`CITA`, `cited_items`), `app.js:79-111`.

**Repro:** `cited_items("B és tancat (Teorema 17(d) del Tema 2).", [T1.17, T2.17], default_tema=1)` returns `['T1.17']`, which is *Proposició 17 (Tema 1)*. The `(d)` breaks the optional tema group, so the default tema is used, and the key ignores the item type ("Teorema" maps to a "Proposició"). The sheet texts contain 24 citations in the "Teorema N(x)" form, and 324 sheet references cross tema, so the default-tema fallback is often wrong. The frontend links the same wrong item. The frontend also links *any* item in the notes (`byKey` over all items), while the backend chips use only the allowed items. The guard then sees a declared reference that doesn't match the text, which can cause spurious `cita_teoria_incorrecta` rejections.

**Fix:**
- Allow an optional `(\([a-z]\))?` after the number.
- Key the lookup on `(tipus, tema, num)`.
- Serve a single pattern (or the extracted spans) from the backend, so the frontend doesn't keep a second regex.
- Link only the items returned in `referencies`.

### M8. A problem's `indicacio` never reaches the student or any LLM stage [V]
**Where:** `fitxes.py:175` (`Problema.indicacio` is loaded), `fitxes.py:147-152` (`enunciat_md`), `fitxes.py:154-168` (`public`).

**Repro:** in 6 problems (t1-6, t1-19, t2-19, t3-10, t4-14, t5-10) the indication text is not in any sub-part's statement. Examples: t1-6 loses "dibuixeu aquests conjunts…", and t4-14 loses "useu el teorema del valor mitjà".

**Fix:** put `indicacio` in `Exercici` (via `_exercici` defaults), in `enunciat_md()` and in `public()`.

### M9. Prompt contradictions that guarantee guard rejections [R]
- `INSTRUCCIONS["demanar_justificacio"]` says "Reconeix que el valor és bo", while the plan says "Pot dir el resultat final: NO", and the guard's `revela_resultat` is "deixa deduir… el resultat". A correct draft can be rejected, and the fallback doesn't acknowledge anything.
- `RESPOSTA_SYSTEM` says "aporta-hi un element nou" when the plan repeats, but the level is fixed. The reply is pushed into `excedeix_nivell_pista`.
- `RESPOSTA_SYSTEM` says "acaba amb UNA sola pregunta", but the deterministic check only requires a "?" somewhere.
- `GUARDIA_SYSTEM` exempts only `mostrar_pas`/`tancar` from `fa_la_feina_de_l_alumne`, but level 3 explicitly allows "començar el DETALL".

**Fix:**
- Make `pot_dir_resultat` three-valued: `no` / `ja_dit_per_l_alumne` / `si`. Phrase both the reply and guard prompts from that value.
- Tie "new element" to "within the level, or a different angle on the same level".
- Add level 3 to the guard's exemption, with its limit stated.

### M10. Frontend: a reply that arrives after the student has switched exercise lands in the new session [R]
**Where:** `app.js:379-415` (`send`), `app.js:480-525` (`attachPhoto`).

`send()` reads `state.session` after the `await`. The reply bubble, its citation links and `traces.push` all go to whichever session is current at that moment. A transcribed photo is likewise written into the new exercise's input box. `state.sending` also stays `true`, which silently blocks sending in the new session.

**Fix:** capture `const sess = state.session` before the request. On return, if `state.session !== sess`, drop the result (or attach it to `sess` only).

### M11. Errades grading: the LLM can override where the code places a highlight, and the scoring rewards silence [V]
**Where:** `errades.py:446-455`, `errades.py:386`, `errades.py:283-299`.

`errades_grade.py` shows:
- an annotation exactly on the quoted error, where the LLM omits its evaluation or returns `"cap"`, scores 0, found 0 and **1 false positive**;
- a wrong explanation scores 30, but no explanation scores 40;
- highlighting the whole fragment counts as `exacta`;
- `compare_verification` matches by fragment only. A verifier that finds a *different* error in the declared fragment counts as confirming the declared one.

**Fix:**
- The code's overlap result should decide whether the error was found. The LLM should only grade the explanation.
- Missing evaluations should be retried, not counted as `cap`.
- Score `absent` ≤ `incorrecta`.
- Make "exact" require the highlight to cover at least X% of the quote and be shorter than about 3× the quote.
- Match verifier findings by overlap of the quote, not just by fragment.

### M12. Sessions: no locking, no eviction, and history grows without limit [R]
**Where:** `app.py:38-39, 194-197`, `prompts.py:63-65`.

FastAPI sync endpoints run in a threadpool. Two concurrent posts to the same session (two tabs, or a retry) both read the same `s.estat`, both append to `historial`, and the last write wins. `SESSIONS` and `ERRADES_SESSIONS` are never evicted. The whole transcript goes to 3 or more calls per turn, so cost grows as O(n²), and after `tancar` the session never ends (H5).

**Fix:**
- Add a per-session `threading.Lock`, or reject a turn while one is already running (409).
- Expire sessions with a TTL or LRU.
- Cap or summarise the transcript after N turns.

---

## LOW

- **L1. The sentence counter overcounts** [V] (`guardia.py:191-197`). "p. ex." counts as 2 sentence ends, and the `explicar_concepte` instruction itself uses "p. ex.". Numbered lists ("1. … 2. …") count as sentences. Inside `$$…$$` the `$[^$]*$` pattern matches the empty `$$`, so periods in display math are counted. A lone currency-style `$` swallows prose. The +1 tolerance hides most of this. Fix: strip `$$…$$` first, and ignore abbreviations and list markers.
- **L2. The professor panel is on by default** [R] (`index.html:33`, `app.js:592`, `app.py:125`). It shows the student `resultat`, the allowed content and the diagnosis. `POST /api/sessions` returns `resultat` to the browser. That's acceptable for a demo, but it is a leak in any real student use. Gate it behind a flag.
- **L3. Sub-parts that depend on earlier ones** [R]. 73 sheet texts say "l'apartat anterior / de l'apartat (a)", but the session for part (c) has no record of the student's work on (a). The UI shows only the preamble and the student's own part. The diagnosis cannot credit "per l'apartat (a)…" against a sheet it doesn't have. Fix: give the earlier parts' statements and results as background, or carry over completion between sibling sessions.
- **L4. Theory items with no number** [V]. 12 sheet references point to items with no number (e.g. `T1.x4`, `T2.x1`). Their label ("Apunts del Tema N, §…") can't be matched by `CITA`, so they can never become chips or links.
- **L5. Fallback text ignores the action's meaning** [R] (`pipeline.py:44-53`). For `explicar_concepte`, `questionar_resultat`, `validar_i_avancar`, `demanar_justificacio` and `mostrar_pas`, the fallback is the generic "Centrem-nos en el pas següent…". It doesn't answer the question, doesn't say the result is wrong, and doesn't validate. It also bypasses `deterministic_check`: titles are currently clean, but `check_fitxes` doesn't check titles. See H6 for the authored fix.
- **L6. `demanar_conclusio` takes precedence over everything when `target is None`** [R]. When all steps are done, "dona'm la solució" or a conceptual question loops on the fixed "Com formularies la conclusió final?".
- **L7. A level-3 hint on the last step removes the result regex** [R] (`politica.py:104-106`). The target's detail is "shown" from level 3, so the result regex is dropped. At level 3 the final calculation must still be left to the student, so only the LLM guard protects the result.
- **L8. Errades frontend** [R].
  - `renderShell()` adds a new `selectionchange` listener on every visit, so they leak.
  - Switching difficulty quickly starts two `carregar()` calls, and whichever finishes last wins, which may not match the selected chip.
  - `tokenize` doesn't handle an escaped `\$`, while backend validation does.
- **L9. Photo `origen`** [R]. The message is tagged `foto` even if the student deleted the transcription and typed something else (`app.js:393`).

---

## Suggested order of work
1. **One escalation and state module.** A single `nivell()` function, plus explicit session facts (`resultat_dit`, `mostrats`, `tancat` sticky, `errors_vistos`, `ultima_accio`). This fixes H1, H3, H5, M1, M2 and M3 at the root.
2. **Generalise the "allowed text" filter** in `_forbidden_regexes`, and add a `check_fitxes` rule for the 22 sheet collisions (H4).
3. **Commit only delivered levels**, with authored fallbacks by level (H6, L5).
4. **Make the turn transactional** and wrap errors in `llm.py` (M6).
5. **Decide with Matías:** the oracle policy (H2), and when `mostrar_pas` triggers without an explicit request (M3).
