# Visualitzador (Beta)

Code: `frontend/visual.js` (core: library loading, formulas, routing, home page), `frontend/visual-eines.js` (the three
tools), `frontend/visual-latex.js` (the statement reader). Route: `#/visual`.

Beta: the tools are in testing and their numerical results may contain errors. The UI marks the mode accordingly.

## Purpose

Plots and numerical analysis of functions of two variables, aimed at the exercises of the course: level curves,
gradients, limits along paths, differentiability, extrema on a region, changes of variables. It runs entirely in the
browser. There is no backend endpoint, no model and nothing stored.

## Tools

| Tool | Route | What it shows |
|---|---|---|
| Explorador f(x,y) | `#/visual/explorador` | Surface and contour map. Clicking a point gives $f$, $\nabla f$, the tangent plane and the Hessian. Critical points are found and classified. Constraints and regions, one per line (`x^2+y^2 <= 1`; `<` marks an open boundary), give the candidates for absolute extrema: interior critical points, Lagrange points on each boundary curve, corners where two constraints meet, and singular points of a constraint. The result is a max or min, or a sup or inf not attained on an open boundary, with a note when the region is compact |
| Anàlisi en un punt | `#/visual/punt` | At a point $a$: the limit along the paths $y-b=m(x-a)^k$ ($k$ = 1 or 2) as a function of $m$, $\sup\lvert f-L\rvert$ on circles of radius $r$, the directional derivative by its definition against $\nabla f\cdot u$, and the tangent-plane error $E(r)$. The value $f(a)$ can be set separately, for piecewise functions |
| Canvis de variables | `#/visual/canvis` | How $F:\mathbb{R}^2\to\mathbb{R}^2$ deforms a grid, the sign of $\det JF$ (local invertibility, fold curves), and $F$ against $DF(a)$ on a small square |

Each tool lists the topics it serves and links the items of the notes it relies on.

## Opening from an exercise

The statement of an exercise gets a "Visualitza" button when `extractVisual()` can read a function from its LaTeX.
The button opens the right tool in a new tab with the functions filled in:

- a map $F=(F_1,F_2)$ opens Canvis de variables;
- a function and a point with no constraints (`\lim_{(x,y)\to(a,b)}`, or a `cases` definition with a special point,
  or a formula followed by "si $(x,y)\neq a$" and $f(a)=c$) opens Anàlisi en un punt with $a$ and $f(a)$;
- otherwise a function $f(x,y)=\dots$ opens the Explorador, with any constraints and regions
  (`\{(x,y)\mid \dots\}`, bare inequalities) found in the statement.

`latexToExpr()` translates LaTeX into math.js syntax (fractions, roots, powers, trigonometric and hyperbolic
functions, `\ln`, absolute values, `cases`). Anything it cannot read is skipped, never guessed, and functions of three
variables are left out. Statements that are proofs, or that have no concrete function, get no button.

Results that would give an exercise away stay behind a click: "Troba els punts crítics", "Calcula els candidats" and
"Mostra la conclusió". The tab notes which exercise the functions were read from.

The [Construeix el contraexemple](contraexemples.md) mode links a submitted function to Anàlisi en un punt at the
origin in the same way.

## Deep links

Every state that can be opened from outside is a hash URL, built by `visualLink()`. Any page can link to a tool with
its functions filled in:

| Tool | URL | Parameters (math.js syntax, URL-encoded) |
|---|---|---|
| Explorador | `#/visual/explorador?f=…&g=…` | `f`: the function; `g`: constraints separated by `;` |
| Anàlisi en un punt | `#/visual/punt?f=…&a=…&fa=…` | `f`: the function off $a$; `a`: the point as `x,y`; `fa`: the value $f(a)$, optional |
| Canvis de variables | `#/visual/canvis?F1=…&F2=…` | the two components of $F$ |

Any of them may add `ex=<exercise id>`, which only labels where the functions came from.

## Implementation

- **Libraries.** Plotly.js 3.1.1 draws and math.js 14.0.1 parses and differentiates. Both load lazily from cdnjs on
  the first visit to `#/visual`, pinned with Subresource Integrity hashes, so a changed file on the CDN is refused,
  not run. Without a network connection the tools show an error and the rest of the app keeps working.
- **Formulas.** Each formula is parsed once into a real-valued math.js instance (`sqrt(-1)` is `NaN`, not complex).
  Partial derivatives are symbolic when math.js can differentiate the expression, with central finite differences as
  the fallback.
- **KaTeX coexistence.** math.js installs a global `math` that would shadow the app's KaTeX `math()` helper;
  `loadVisLibs()` takes the math.js instance and restores the app's function.
- **Verdicts are numerical and say so** ("numèricament"). Point analysis samples circles and tries several path
  families ($y-b=m(x-a)^k$ and $x-a=m(y-b)^k$, $k$ = 1, 2, 3) before concluding, since circles alone miss paths that
  hug an axis.
- Plots are redrawn with the matching palette when the system switches between light and dark mode.

## Limits

- Everything is floating point. A limit "exists numerically" or a function is "differentiable numerically": these are
  strong hints, not proofs. The rigorous checker is [Construeix el contraexemple](contraexemples.md).
- Only functions of two variables, and maps from $\mathbb{R}^2$ to $\mathbb{R}^2$.
- The statement reader covers the common notations of the collection; unusual LaTeX leaves the button out rather than
  opening a wrong function.
