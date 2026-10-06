# Wave 2 spec — write hidden solution sheets ("fitxes") for a Socratic tutor

Project: `C:/Users/matia/Documents/ProjecteDiferencial` — a Socratic tutor for "Càlcul Diferencial" (FME-UPC), Catalan.
All paths below are relative to the project root `C:/Users/matia/Documents/ProjecteDiferencial` (statements in `work/enunciats/`, outputs in `work/fitxes/`).

## How the sheet is used (read this, it drives every choice)
Per student message: (1) a DIAGNOSIS LLM sees the whole sheet + cited theory and classifies which steps the
student has done, which common errors appear, whether the result is right. (2) Deterministic code picks an
action and a hint level 1–4 for the first unfinished step. (3) A REPLY LLM sees ONLY:
  level 1 → step `objectiu`; level 2 → + `idea` and the step's `teoria`; level 3–4 → + `detall`.
  It never sees later steps or `resultat` (until the end). (4) A GUARD rejects the reply if it matches a
  forbidden regex: `resultat.fuites` always (until the student states the result), later steps' `fuites`,
  and the target step's own `fuites` below level 3.
So: `objectiu` = WHAT to achieve, as a question-able goal, no method. `idea` = the strategy / which result to
use, no computation. `detall` = the worked content of the step, complete and correct. Steps are in solving
order; each one is a natural "checkpoint" a student can reach and state.

## Inputs
- Statements: `work/enunciats/temaN.yaml` (transcribed from the problem collection).
- Theory: `backend/teoria/tema1.yaml` … `tema6.yaml` (items with ids like `T3.12`; one shared counter per tema;
  `T3.x4` = unnumbered prose). Read the whole theory file of your tema (and earlier temas as needed, grep by nom).
- Format example (study it): `work/fitxes/EXEMPLE_t2-4c.yaml`.
- Quality exemplars of the old format (same content model, older YAML style):
  `work/old_exercicis/limits_4.yaml` (Tema 2 problem 4 a–g — PORT these into your output if problem 4 of tema 2 is
  in your range, keeping their steps/errors, updating format, ids `t2-4a`…, adding theory refs; check 4(e)
  against the transcribed statement, the old sheet's note discusses the statement) and
  `work/old_exercicis/teoria_t3.yaml` (old Tema 3 theory problems, other numbering: reuse any sheet whose
  statement is the SAME problem as one in your range, e.g. old t3-5 likely = new T3 #5; renumber).

## Output
`work/fitxes/temaN_pK.yaml` (you are told N and K and your problem range). Top-level key `problemes:` only:

```yaml
problemes:
  - num: 4                     # problem number in the collection
    font: null                 # copy from statements file
    preambul: |                # shared statement text (copy from statements); "" if the problem has no sub-parts
      Calculeu els límits següents:
    indicacio: null            # copy from statements
    exercicis:                 # ONE sheet per sub-part; one single sheet (apartat: null) if no sub-parts
      - id: "t2-4c"            # t<tema>-<num><letter>; "t3-5" when no sub-parts
        apartat: "c"           # null when no sub-parts
        tipus: calcul          # calcul (compute/decide with computation) | teoric (prove, reason, counterexample)
        enunciat: |            # the sub-part text (or the full statement when no sub-parts), copied from statements
        teoria: [...]          # background items the STATEMENT relies on (definitions of the notions it names).
                               # Visible to the student from turn 1, so must not hint the method.
        teoria_reservada: []   # items of the notes that SOLVE this exercise (worked example of the same problem).
        resultat:
          valor: |             # final answer / conclusion, precise and complete (what a correct answer states)
          fuites: [...]        # regexes that detect the result being given away (may be [] for proofs)
        passos: [...]          # 2–6 steps: id (snake_case), titol, objectiu, idea, detall, fuites, teoria
        errors_comuns: [...]   # 2–4: id, descripcio (the misconception), pregunta (Socratic question that makes the
                               # student find it without naming the fix)
        nota_professor: |      # optional: subtleties, alternative methods, statement typos you noticed
```

### Theory references (the new feature — be accurate)
- Each step's `teoria`: the items (definitions/theorems/propositions…) that step actually USES. The tutor will cite
  them by name ("pel Teorema 12 del Tema 3"), so a wrong ref = a wrong citation shown to a student. Open the item and
  check its hypotheses match how the step uses it. Use `T3.12+dem` only if the PROOF technique is what the step
  reuses. Prefer numbered items; `T3.xK` only when the needed fact is only in prose.
- Cross-tema refs are fine (tema 3 problems often need tema 2 continuity results).
- If the notes contain no item for a fact a step uses (e.g. a 1-variable fact), leave that step's `teoria: []` and
  say what the fact is in `idea`. Never invent ids. Every exercise must cite at least one item overall.
- If an item of the notes works out this very problem (look at items with `problemes:` and at Exemples whose
  function is the same as the statement), put it in `teoria_reservada` and NOT in `teoria`/steps.

### Leak regexes (`fuites`) — Python `re`, IGNORECASE, matched against Catalan text with `$...$` LaTeX
- YAML single-quoted strings (`'...'`, backslash literal, write `''` for a quote).
- For each step with non-empty `fuites`, at least one regex MUST match that step's own `detall`, and none may match
  its own `objectiu` or `idea` (nor may `resultat.fuites` match any objectiu/idea or any error `pregunta`).
- Target the decisive content (the key bound, the key path, the value), tolerant to spacing/notation variants
  (`\s*`, `\{?2\}?`, `(\\le|\\leq|≤)`). Don't ban generic words; a regex that fires on harmless text makes every reply
  fail. Steps whose detail is generic may have `fuites: []`.
- `resultat.fuites`: catch statements of the final value/verdict ("el límit és 0", "no és diferenciable",
  "\\ker Df(0,0)=..."). For proofs the result is the statement itself: usually `[]`.

### Content rules
- Mathematically correct and rigorous, at first-year-of-degree FME level, consistent with the notes' definitions
  and notation. If you are not sure of an answer, work it fully (you may run Python/sympy via
  `.venv/Scripts/python.exe` with `PYTHONPATH=work/pylib` (sympy installed there, see PLA.md); else reason by hand) —
  a wrong `detall`/`resultat` is the worst possible defect.
- Catalan, KaTeX-compatible LaTeX, `$...$` inline (display `$$` only in `enunciat`/`preambul` if copied). Balanced `$`.
- Use block scalars `|` for every prose field.
- Sub-parts that depend on earlier ones ("Deduïu…"): the sheet may assume earlier parts' results as known and say so
  in the first step's `objectiu`.
- Exercises with several independent questions (e.g. "interior, frontera, adherència i acumulació"): one step per
  question, `resultat.valor` lists all answers.

## Self-check (mandatory before you finish)
Run: `C:/Users/matia/Documents/ProjecteDiferencial/.venv/Scripts/python.exe C:/Users/matia/Documents/ProjecteDiferencial/scripts/check_fitxes.py work/fitxes/temaN_pK.yaml --tema N`
Fix until it prints `0 problems`. Then re-read every `resultat` and `detall` once more for
mathematical errors.

Write ONLY your output file. Final report (short): number of sheets, any statement you think is mis-transcribed or
mis-printed, any answer you are less than sure about (exercise id + why).
