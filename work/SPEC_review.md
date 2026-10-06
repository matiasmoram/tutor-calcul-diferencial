# Phase 4 spec — review solution sheets of ONE chunk

Project root: `C:/Users/matia/Documents/ProjecteDiferencial`. First read `work/SPEC_wave2.md` (how sheets are used and
the authoring rules). You review `work/fitxes/temaN_pK.yaml` and FIX it in place. Many chunks were written by agents that
stopped before their final self-review, so expect real defects.

For every exercise, in this order of importance:
1. **Statement**: compare `enunciat`/`preambul` with `work/enunciats/temaN.yaml` (must match). If in doubt about the
   transcription itself, render the PDF page and read it:
   `pdftoppm -r 200 -png -f P -l P "sources/Problemes/_Problemes Temes_1-6.pdf" work/review_pP`
   (pages: T1 3–6, T2 7–10, T3 11–14, T4 15–18, T5 19–20, T6 21–22). Delete the PNG afterwards.
2. **Mathematics**: redo the solution yourself. `resultat.valor` and every `detall` must be correct, complete and
   rigorous (hypotheses checked, all cases covered). Verify computations with sympy:
   `PYTHONPATH=work/pylib .venv/Scripts/python.exe -c "..."`. Fix anything wrong.
3. **Theory references**: open each cited item in `backend/teoria/temaN.yaml` and check that it says what the step uses
   it for (hypotheses included) and that the id is the right one. Exercise-level `teoria` must not hint the method.
   Anything that solves this very exercise belongs in `teoria_reservada`.
4. **Hint ladder**: `objectiu` = what to achieve, no method; `idea` = method, no computation; neither gives away the
   step's key content or the result. Steps in solving order, each a natural checkpoint. 2–4 plausible common errors
   with genuinely Socratic questions (no answer inside the question).
5. **Leak regexes**: they must catch the decisive content in the forms a tutor might write it (spacing, `\dfrac`/`\frac`,
   `\ ` spacing, `\sqrt e` vs `\sqrt{e}`, `$` between formula and text), without firing on harmless text.

Finish with `.venv/Scripts/python.exe scripts/check_fitxes.py work/fitxes/temaN_pK.yaml --tema N` at 0 problems.
Edit only your chunk file. Final report (short): what you changed per exercise id (one line each, only changed ones),
and anything you could not resolve.
