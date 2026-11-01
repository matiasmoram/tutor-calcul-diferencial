# Construeix el contraexemple (Beta)

Code: `backend/core/counterexamples/`. Challenges: `backend/contraexemples/reptes.yaml`. Route: `#/contraexemples`.

Beta: the checker is in testing and its verdicts may contain errors. The UI marks the mode accordingly.

Paths below are relative to the code directory named above, unless they start with `backend/` or `frontend/`.

## Purpose

The student builds the pathological function instead of reading it. A challenge asks for $f$ with properties at the
origin that look incompatible: partial derivatives but no continuity, the same limit along every line but no limit,
differentiable but not $C^1$, crossed second derivatives that differ. **No model is called**: every verdict is
computed with sympy.

## Student flow

1. Pick one of the 13 challenges. Each shows its statement, the items of the notes it is about, a hint, and the
   properties to achieve, each with what kind of certificate it needs.
2. Write $f(x,y)$ off the origin and $f(0,0)$ in sympy syntax (`x**2*y/(x**4+y**2)`, `Abs`, `sqrt`, `cbrt`, `sin`,
   `exp`…), plus a certificate for each property that needs one.
3. Submit. Each property comes back with a status, a reason and the computations behind it (LaTeX lines). A failed
   property shows the definition to review ("Repassa").
4. Once every property passes, the challenge's authored example is revealed with its explanation and the items of the
   notes that contain such an example. A "Visualitza" link opens the function in the point-analysis tool of the
   [Visualitzador](visualitzador.md).

## Properties and certificates

Fifteen property kinds (`domain/values/properties.py`), each with the certificate it needs:

| Certificate | Properties | What the student gives |
|---|---|---|
| none | same limit along every line, that limit equals $f(0,0)$, equal iterated limits, partials exist, some partial does not exist, every directional derivative exists, directional derivatives linear in the direction, crossed second derivatives differ | nothing |
| paths | the limit does not exist, $f$ is not continuous | 1 or 2 paths $(x(t),y(t))\to(0,0)$ as $t\to0^+$ |
| paths, optional | $f$ is not differentiable | paths if needed; often decided without (a missing partial, or a directional derivative that is not $\nabla f\cdot v$) |
| radial bound | $f$ is continuous, $f$ is differentiable | $G(r)$ with $\lvert f(r\cos\theta, r\sin\theta)-f(0,0)\rvert\le G(r)$ (for differentiability, the same for the remainder) and $G\to0$ |
| direction | some directional derivative does not exist | $v=(u,w)$ |
| partial + path | a partial derivative is not continuous | which partial, and a path |

## How a verdict is reached (trust model)

- **Only one-variable limits are trusted.** sympy's two-variable limits are unsound: with the angle left free, the
  polar limit of $x^2y/(x^4+y^2)$ is 0, yet the limit does not exist. So partial and directional derivatives are
  limits of difference quotients in $h$, iterated limits are two one-variable limits, and a path reduces $f$ to a
  function of $t$. Each sympy limit is cross-checked numerically.
- **Negative properties need witnesses.** "The limit does not exist" is shown by two paths with different limits, or
  one path without a limit, never by sympy alone.
- **Positive properties need a radial bound.** $G\to0$ is checked exactly. The inequality is sampled on a polar grid
  whose angles hug the axes, so that a curve such as $y=x^2$ is caught, and it is also checked exactly along fixed
  rays and along every path given anywhere in the submission. Sampling makes the verdict **plausible**, not proved.

Statuses (`domain/values/verdict.py`):

| Status | Meaning | Passes |
|---|---|---|
| `ok` | Decided exactly | yes |
| `plausible` | Exact limits, sampled inequality | yes |
| `falla` | The property is shown false for this $f$, or $f$ is not a real function off the origin | no |
| `indeterminat` | Not decided: sympy cannot tell, or the certificate is missing or proves nothing (shown as "No demostrat") | no |

The response reports `superat` (all properties pass) and `rigoros` (all are `ok`).

## Hardening

- Input is parsed with the shared whitelisted parser, never evaluated as Python, at most 300 characters per
  expression. Nested exponentials deeper than 2, numeric exponents above 1000, and constants outside
  $[10^{-6}, 10^6]$ are rejected with a reason (422), as are common slips such as `|x|` for `Abs(x)`.
- $f$ must be real on the whole plane minus the origin. This is checked on a 4096-angle sweep at three radii, and by
  looking for sign changes of the denominator on circles, each confirmed at exact points.
- sympy's "no limit" counts only when the numbers confirm it: the function must visibly keep oscillating, jumping or
  growing at every scale. An unbounded or oscillating answer is first retried on rewritten forms (expand, trigsimp,
  simplify). A finite limit that the numbers contradict is left undecided. Equality of limits is exact, with no
  tolerance.

## Ties to the notes

`reptes.yaml` maps every property kind to the items of `backend/teoria` that define it (`teoria_propietats`). Each
challenge cites the items it is about (`teoria`) and the items that already contain such a counterexample
(`teoria_reservada`, shown only with the authored example). Hints and explanations cite the notes, and the citations
become links to the PDF page. The server refuses to start if a challenge or a property cites an item that does not
exist (`SpecCatalog.check_theory`).

## Authoring a challenge

An entry of `reptes:` has `id`, `tema`, `titol`, `enunciat`, `propietats`, `teoria`, `teoria_reservada`,
`dificultat`, `pista`, `exemple` (`funcio`, `valor`, `certificats`) and `explicacio`. The tests run every authored
example through the checker, so a challenge whose own example does not pass fails CI.

## Execution

`SubmissionGrader` (`application/submission_grader.py`) parses the submission (cheap, on the event loop), then
`PoolPropertyChecker` decides each property in its own process of the server's `SympyCheckPool`, under the pool's
deadline per check (25 s). Decided verdicts are kept in a process-wide cache. `TUTOR_SYMPY_WORKERS` sets the number of
worker processes (default 1), `TUTOR_SYMPY_WORKER_MEMORY_MB` caps each one's memory on POSIX (default 256), and
`TUTOR_SYMPY_WARM_CACHE=1` decides every authored example at start-up.

## Endpoints

| Endpoint | Body | Returns |
|---|---|---|
| `GET /api/contraexemples` | — | Challenges with their properties |
| `GET /api/contraexemples/{id}` | — | Statement, hint, theory items, properties; the authored example for professors |
| `POST /api/contraexemples/{id}/comprova` | `{funcio, valor, certificats: {<property>: {camins, fita, direccio, parcial}}}` | `superat`, `rigoros`, `veredictes`; the example once passed |

The check endpoint is rate-limited per client, since each submission keeps sympy workers busy. Nothing is stored.

## Limits

- `plausible` is a sampled verdict, not a proof.
- sympy can fail to decide a limit that a human would settle; the student then sees `indeterminat` and may add or
  change a certificate.
- The set of properties is fixed; a new kind needs a decider in `domain/services/deciders/` and its definition in
  `teoria_propietats`.
