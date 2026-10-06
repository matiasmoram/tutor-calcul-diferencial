# Wave 1 spec — transcribe theory notes + problem statements for ONE tema

Course: "Càlcul Diferencial" (FME-UPC), Catalan. Sources were rendered to PNG at 110 dpi:

- Theory pages of tema N: `SCRATCH/img/tN-01.png` … (one PNG per PDF page, page number = file index).
- Problem collection pages: `SCRATCH/img/prob-XX.png`. Page ranges per tema:
  T1 = 03–06, T2 = 07–10, T3 = 11–14, T4 = 15–18, T5 = 19–20, T6 = 21–22.
- Rough text layers (math is mangled, use ONLY as a spell-check aid, never as the source of formulas):
  `SCRATCH/txt/temaN.pypdf.txt` (theory, decent prose) and `SCRATCH/txt/problemes.pypdf.txt`.

SCRATCH = `C:/Users/matia/AppData/Local/Temp/claude/C--Users-matia-Documents-ProjecteDiferencial/3150e06d-65b6-4837-8858-9c80cae58a98/scratchpad`

Read EVERY page image with the Read tool (it shows images). If a formula is small/unclear, re-render that page
at higher resolution: `pdftoppm -r 200 -png -f P -l P "<pdf>" SCRATCH/img/hi_tN_P` and read that.
PDFs: `C:/Users/matia/Documents/ProjecteDiferencial/sources/Teoria/Càlcul_Diferencial_FME_TemaN.pdf`,
`C:/Users/matia/Documents/ProjecteDiferencial/sources/Problemes/_Problemes Temes_1-6.pdf`.

## Output 1: `C:/Users/matia/Documents/ProjecteDiferencial/backend/teoria/temaN.yaml`

Faithful, COMPLETE transcription of the theory notes into Markdown + LaTeX. Nothing summarized, nothing skipped
(except page numbers, headers, and the cover page). Fix nothing mathematically; copy what is there.

```yaml
tema: 3
titol: "Diferenciabilitat"
seccions:
  - id: "3.1"
    titol: "Definició i primeres propietats"
items:
  - id: "T3.1"            # "T<tema>.<num>" — the notes number Definició/Teorema/Exemple/... with ONE shared counter per tema
    tipus: definicio       # definicio | teorema | proposicio | lema | corollari | observacio | exemple | exercici | nota | text
    num: 1
    resum: 66              # number in the green box in the right margin (link to "Resum de teoria"), null if none
    seccio: "3.1"
    pagina: 2              # PDF page index (the PNG file index)
    nom: "Derivada direccional"   # YOUR short descriptive name, <= 6 words, Catalan. Explicit name in the notes wins.
    enunciat: |
      Sigui $f:\Omega\subseteq\mathbb{R}^n\to\mathbb{R}$, $a\in\mathring{\Omega}$ i $u\in\mathbb{R}^n\setminus\{0\}$. ...
      $$D_uf(a)=\lim_{t\to0}\frac{f(a+tu)-f(a)}{t},$$
      si aquest límit existeix.
    demostracio: |         # only if the notes give a proof / worked solution right after; omit the key otherwise
      ...
    problemes: ["T2.6"]    # problems of the collection explicitly cited inside the item ("vegeu el problema 6 del tema 2"); [] if none
```

Rules:
- Every numbered environment = one item. Example parts (i), (ii) stay inside the same item.
- Substantive unnumbered prose between items (motivation, remarks, recall of 1-variable facts): an item with
  `tipus: text`, `num: null`, `id: "T3.x1"`, `"T3.x2"`, … in order. Do not drop it.
- Footnotes: append to the item where they are referenced, as `(Nota: ...)`.
- Figures: one line `[Figura: <what it shows>]` inside the item.
- Math: inline `$...$`, display `$$...$$` on its own lines. KaTeX-compatible LaTeX only (no \begin{align}; use
  `\begin{aligned}...\end{aligned}` inside `$$`). Use `\mathbb{R}`, `\mathring{A}` for interior, `\overline{A}` closure,
  `\partial`, `\|x\|`, `\langle x,y\rangle`, `\dfrac` where the notes have display fractions in text.
- Use YAML block scalars (`|`) for every text field so backslashes need no escaping. Quote `id` strings.
- Keep the Catalan exactly (accents, apostrophes ’ → ').

## Output 2: `SCRATCH/enunciats/temaN.yaml`

All problems of tema N from the problem collection, transcribed exactly.

```yaml
tema: 3
titol: "Diferenciabilitat"
problemes:
  - num: 5
    font: null              # e.g. "Exercici d'examen, maig 2008" when stated
    preambul: |
      Estudieu la continuïtat i l'existència de derivades direccionals a $\mathbb{R}^2$ de la funció
      $$f(x,y)=\begin{cases}\dfrac{x^2}{y} & \text{si } y\neq 0\\ 0 & \text{si } y=0.\end{cases}$$
    apartats: []            # list of {lletra: a, text: | ...}; [] if no sub-parts
    indicacio: null         # hint given in the statement ("Indicació: ..."), if any
```

## Done criteria
1. Both files parse: `C:/Users/matia/Documents/ProjecteDiferencial/.venv/Scripts/python.exe -I -c "import yaml,sys; d=yaml.safe_load(open(sys.argv[1],encoding='utf-8')); print(len(d.get('items',d.get('problemes'))))" <file>`
2. Item ids unique; numbers consecutive with what the notes show (report any gap you observe in the notes themselves).
3. Every problem number of the tema present; every sub-part present.
4. Final report (short): counts of items by tipus, number of problems/sub-parts, any page or formula you were unsure about.
