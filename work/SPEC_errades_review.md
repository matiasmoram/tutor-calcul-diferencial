# Spec — blind review of "Troba l'error" documents

Project root: `C:/Users/matia/Documents/ProjecteDiferencial`. You are the independent VERIFIER of the pipeline in
`backend/tutor/errades.py`. Your instructions are its prompts: `VERIFICACIO_SYSTEM` (problem resolutions) and
`VERIFICACIO_TEORIA_SYSTEM` (results of the notes). Read them first.

**Blind rule:** read ONLY the `.blind.md` file you are given. Never open the matching `.json` batch (it holds the
declared errors) or anything under `backend/generats/`. You may open the notes (`backend/teoria/`), the sheets
(`backend/exercicis/`) and run sympy (`PYTHONPATH=work/pylib .venv/Scripts/python.exe`) to check computations.

Each section `## <id>:<dificultat>` has the reference (sheet, or the ORIGINAL item of the notes) and the numbered
document to review. Theory documents mark fragments `(enunciat)` / `(demostració)`. List EVERY problem you find:

- `"error"`: this fragment is mathematically wrong, or makes the statement false / different from the notes.
- `"consequencia"`: correct reasoning that only fails because of an earlier error (inherits a wrong value, or uses a
  hypothesis that a wrong statement dropped).
- `"imprecisio"`: wording, condensed routine computation, minor lack of rigour that does not change the mathematics.

An equivalent rewording is not a problem. Be exhaustive and strict, but don't invent errors: a false "error" rejects a
good document, a missed one lets a broken document reach students. Report each problem once, on the fragment where it
happens; `cita` = shortest exact copy of the text at fault (character-for-character, `$` included).

Output: the JSON file given in your task (write it with Python, `ensure_ascii=False`):

```json
{"T3.21:normal": {"problemes": [{"fragment": 1, "cita": "...", "gravetat": "error", "explicacio": "..."}],
                  "valoracio": "one sentence"}}
```
One entry per section, keys exactly as the section titles. Final report: per document, the number of `error`
findings, and nothing else.
