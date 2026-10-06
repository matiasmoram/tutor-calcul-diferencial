"use strict";

/* Labs for temes 4–6: inverse function and changes of variables, implicit function, Taylor,
   critical points and the Hessian, Lagrange multipliers, manifolds with tangent/normal spaces.
   Uses the helpers in visual.js. */

/* ---------- Tema 4: inverse function theorem / changes of variables ---------- */

lab({
  id: "inversa", tema: 4, seccio: "Teorema de la funció inversa", icon: "⇄",
  titol: "Canvis de variables i funció inversa",
  resum: "Com deforma $F:\\mathbb{R}^2\\to\\mathbb{R}^2$ una quadrícula. On $\\det JF\\ne0$ és localment invertible; on s'anul·la, la quadrícula es plega.",
  idea: "Si $\\det JF(a)\\neq0$, $F$ és un difeomorfisme d'un entorn de $a$ (Teorema 5 del Tema 4): a prop de $a$, $F$ s'assembla a la seva diferencial, que envia el quadradet a un paral·lelogram d'àrea $|\\det JF(a)|$ vegades més gran. Però localment invertible a tot arreu no vol dir injectiva globalment (Exemple 3 del Tema 4): mira $z\\mapsto z^2$ o l'exponencial complexa.",
  refs: ["T4.3", "T4.5", "T4.6", "T4.9", "T4.11"],
  mount({ side, main }) {
    const c = pal();
    const presets = [
      { tex: "(r\\cos\\theta,\\,r\\sin\\theta)", f1: "x*cos(y)", f2: "x*sin(y)", X: [0, 2], Y: [0, 2 * Math.PI], a: [1, 1], title: "Coordenades polars (x = r, y = θ)" },
      { tex: "(x^2-y^2,\\,2xy)", f1: "x^2 - y^2", f2: "2*x*y", X: [-1.2, 1.2], Y: [-1.2, 1.2], a: [0.7, 0.4], title: "z ↦ z²" },
      { tex: "(e^x\\cos y,\\,e^x\\sin y)", f1: "exp(x)*cos(y)", f2: "exp(x)*sin(y)", X: [-1, 0.8], Y: [-4, 4], a: [0, 0.5], title: "Exponencial complexa: det ≠ 0 a tot arreu, però no injectiva" },
      { tex: "(x+\\tfrac12\\sin y,\\,y+\\tfrac12\\sin x)", f1: "x + 0.5*sin(y)", f2: "y + 0.5*sin(x)", X: [-3, 3], Y: [-3, 3], a: [1, -1], title: "Difeomorfisme global" },
      { tex: "(x,\\,y^3-xy)", f1: "x", f2: "y^3 - x*y", X: [-1, 1.5], Y: [-1.3, 1.3], a: [0.5, 0.2], title: "Plec (corba on det = 0)" },
    ];
    const S = { ...presets[0], sq: 0.15 };
    const f1 = formulaField({ label: "$F_1(x,y)=$", value: S.f1 }, () => render());
    const f2 = formulaField({ label: "$F_2(x,y)=$", value: S.f2 }, () => render());
    const sa = slider({ label: "$a_1$", min: S.X[0], max: S.X[1], value: S.a[0] }, (v) => { S.a = [v, S.a[1]]; render(); });
    const sb = slider({ label: "$a_2$", min: S.Y[0], max: S.Y[1], value: S.a[1] }, (v) => { S.a = [S.a[0], v]; render(); });
    const ss = slider({ label: "Mida del quadradet", min: 0.02, max: 0.5, value: S.sq }, (v) => { S.sq = v; render(); });
    const figD = plotBox("Domini: quadrícula i signe de $\\det JF$");
    const figI = plotBox("Imatge per $F$");
    const out = readout();
    const render = () => {
      const A = f1.fn, B = f2.fn; if (!A || !B) return;
      const F = (x, y) => [A.f(x, y), B.f(x, y)];
      const J = (x, y) => [A.grad(x, y), B.grad(x, y)];
      const det = (x, y) => { const m = J(x, y); return m[0][0] * m[1][1] - m[0][1] * m[1][0]; };
      const NL = 16, xs = linspace(...S.X, NL), ys = linspace(...S.Y, NL), fine = 80;
      const tr = [], im = [];
      // Grid lines: vertical family in accent, horizontal in reveal, so the deformation can be followed.
      for (const [fam, color, name] of [["v", c.accent, "x = const"], ["h", c.reveal, "y = const"]]) {
        const D = { x: [], y: [] }, I = { x: [], y: [] };
        for (const k of fam === "v" ? xs : ys) {
          for (const t of linspace(...(fam === "v" ? S.Y : S.X), fine)) {
            const [x, y] = fam === "v" ? [k, t] : [t, k];
            const [u, v] = F(x, y);
            D.x.push(x); D.y.push(y); I.x.push(u); I.y.push(v);
          }
          D.x.push(null); D.y.push(null); I.x.push(null); I.y.push(null);
        }
        tr.push({ ...D, mode: "lines", name, line: { color, width: 1 }, opacity: 0.8, hoverinfo: "skip" });
        im.push({ ...I, mode: "lines", name: `F(${name})`, line: { color, width: 1 }, opacity: 0.8, hoverinfo: "skip" });
      }
      const gd = grid(det, S.X, S.Y, 90);
      const zero = contourLines(gd, 0);
      const m = Math.max(...gd.z.flat().filter(Number.isFinite).map(Math.abs)) || 1;
      const a = S.a, h = S.sq / 2;
      const sqD = [[-h, -h], [h, -h], [h, h], [-h, h], [-h, -h]].map(([dx, dy]) => [a[0] + dx, a[1] + dy]);
      const sqDense = [];
      for (let k = 0; k < 4; k++) for (const t of linspace(0, 1, 20)) sqDense.push([sqD[k][0] + t * (sqD[k + 1][0] - sqD[k][0]), sqD[k][1] + t * (sqD[k + 1][1] - sqD[k][1])]);
      const Ja = J(...a), Fa = F(...a), da = det(...a);
      const lin = sqD.map(([x, y]) => [Fa[0] + Ja[0][0] * (x - a[0]) + Ja[0][1] * (y - a[1]), Fa[1] + Ja[1][0] * (x - a[0]) + Ja[1][1] * (y - a[1])]);
      const imZero = zero.map((l) => l.map((p) => F(...p)));
      draw(figD.div, [
        { type: "heatmap", x: gd.xs, y: gd.ys, z: gd.z, colorscale: divScale(), zmin: -m, zmax: m, opacity: 0.55, showscale: true,
          colorbar: { title: { text: "det JF" }, thickness: 10, len: 0.6 }, hovertemplate: "det JF = %{z:.3f}<extra></extra>", name: "det JF" },
        ...tr,
        ...(zero.length ? [{ ...joinLines(zero), mode: "lines", name: "det JF = 0", line: { color: c.bad, width: 3 } }] : []),
        { x: sqD.map((p) => p[0]), y: sqD.map((p) => p[1]), mode: "lines", fill: "toself", name: "quadradet", line: { color: c.ink, width: 2 } },
        marker(a, c.ink, "a"),
      ], layout2d({ xaxis: axis2d({ range: S.X }), yaxis: axis2d({ range: S.Y }) }));
      draw(figI.div, [
        ...im,
        ...(imZero.length ? [{ ...joinLines(imZero), mode: "lines", name: "F(det = 0)", line: { color: c.bad, width: 3 } }] : []),
        { x: sqDense.map((p) => F(...p)[0]), y: sqDense.map((p) => F(...p)[1]), mode: "lines", fill: "toself", name: "F(quadradet)", line: { color: c.ink, width: 2 } },
        { x: lin.map((p) => p[0]), y: lin.map((p) => p[1]), mode: "lines", name: "DF(a) aplicada al quadradet", line: { color: c.warn, width: 2, dash: "dash" } },
        marker(Fa, c.ink, "F(a)"),
      ], layout2d({ xaxis: axis2d({ scaleanchor: "y" }), yaxis: axis2d() }));
      const t = [[A.tex(["x"]), A.tex(["y"])], [B.tex(["x"]), B.tex(["y"])]];
      out.set(
        t.flat().every(Boolean) ? el("div", { text: `$JF=\\begin{pmatrix}${t[0][0]}&${t[0][1]}\\\\${t[1][0]}&${t[1][1]}\\end{pmatrix}$` }) : null,
        el("div", { text: `$\\det JF(a)=${fmt(da)}$` }),
        Math.abs(da) > 1e-6
          ? verdict(`det JF(a) ≠ 0: F és un difeomorfisme local a prop de a. El quadradet es transforma en gairebé un paral·lelogram d'àrea ×${fmt(Math.abs(da), 2)}${da < 0 ? ", amb l'orientació invertida" : ""}.`, "ok")
          : verdict("det JF(a) = 0: el teorema de la funció inversa no s'aplica (i la quadrícula es plega aquí).", "bad"),
        para("Fes petit el quadradet: la imatge (negre) i la seva aproximació lineal (discontínua) coincideixen cada cop més.", "small muted"));
    };
    side.append(
      chips("Exemples", presets, (p) => {
        Object.assign(S, p); f1.set(p.f1); f2.set(p.f2);
        sa.set(p.a[0], { min: p.X[0], max: p.X[1] }); sb.set(p.a[1], { min: p.Y[0], max: p.Y[1] }); render();
      }),
      f1.node, f2.node, sa.node, sb.node, ss.node, out.node);
    main.append(el("div", { class: "vl-row" }, figD.node, figI.node));
    render();
  },
});

/* ---------- Tema 4: implicit function theorem ---------- */

lab({
  id: "implicita", tema: 4, seccio: "Teorema de la funció implícita", icon: "∅",
  titol: "Funció implícita",
  resum: "Recorre la corba $F(x,y)=0$: on $\\partial_yF\\neq0$ és localment una gràfica $y=g(x)$ amb $g'=-F_x/F_y$.",
  idea: "Si $F(a,b)=0$ i $\\partial_yF(a,b)\\neq0$, a prop de $(a,b)$ la corba és la gràfica d'una funció $y=g(x)$, amb $g'(x)=-\\frac{\\partial_xF}{\\partial_yF}$ (Teorema 13 del Tema 4). Als punts amb $\\partial_yF=0$ la tangent és vertical o la corba és singular, i el teorema no s'aplica.",
  refs: ["T4.12", "T4.13", "T4.14"],
  mount({ side, main }) {
    const c = pal();
    const presets = [
      { tex: "x^2+y^2-1", src: "x^2 + y^2 - 1", R: 1.5 },
      { tex: "x^3+y^3-3xy", src: "x^3 + y^3 - 3*x*y", R: 2.2, title: "Folium de Descartes" },
      { tex: "y^2-x^3", src: "y^2 - x^3", R: 1.5, title: "Cúspide" },
      { tex: "(x^2+y^2)^2-2(x^2-y^2)", src: "(x^2 + y^2)^2 - 2*(x^2 - y^2)", R: 1.7, title: "Lemniscata" },
      { tex: "y^3+y-x^2", src: "y^3 + y - x^2", R: 2, title: "Gràfica global: F_y > 0 sempre" },
    ];
    const S = { R: 1.5, s: 0.1, win: 0.35 };
    const ff = formulaField({ label: "$F(x,y)=$", value: presets[0].src }, () => render());
    const ss = slider({ label: "Posició sobre la corba", min: 0, max: 1, step: 0.002, value: S.s }, (v) => { S.s = v; render(); });
    const sw = slider({ label: "Mida de l'entorn", min: 0.05, max: 1, value: S.win }, (v) => { S.win = v; render(); });
    const fig = plotBox("Corba $F(x,y)=0$");
    const out = readout();
    const render = () => {
      const fn = ff.fn; if (!fn) return;
      const g = grid(fn.f, [-S.R, S.R], [-S.R, S.R], 241);
      const lines = contourLines(g, 0);
      if (!lines.length) { draw(fig.div, [contour2d(g)], layout2d()); out.set(verdict("La corba és buida en aquesta finestra.", "warn")); return; }
      const arc = arcParam(lines);
      const Fx = fn.d("x").f, Fy = fn.d("y").f;
      // Points with F_y = 0 along the curve (sign change between consecutive vertices, refined by Newton).
      const vert = [];
      for (const l of lines) for (let k = 0; k < l.length - 1; k++) {
        if (Fy(...l[k]) * Fy(...l[k + 1]) <= 0) {
          const p = newton(([x, y]) => [fn.f(x, y), Fy(x, y)], l[k]);
          if (p && Math.abs(p[0]) <= S.R && Math.abs(p[1]) <= S.R) vert.push(p);
        }
      }
      const vpts = dedupe(vert, 1e-3);
      const sing = vpts.filter((p) => Math.abs(Fx(...p)) < 1e-4);
      const vt = vpts.filter((p) => Math.abs(Fx(...p)) >= 1e-4);
      let P = arc.at(S.s).p;
      P = newton(([x, y]) => { const gr = [Fx(x, y), Fy(x, y)]; return [fn.f(x, y), (x - P[0]) * gr[1] - (y - P[1]) * gr[0]]; }, P) || P;  // snap onto F = 0
      const fx = Fx(...P), fy = Fy(...P);
      const traces = [
        contour2d(g, { opacity: 0.35, showlegend: false, contours: { coloring: "heatmap", showlabels: false } }),
        { ...joinLines(lines), mode: "lines", name: "F = 0", line: { color: c.ink, width: 2.5 } },
      ];
      const ann = [];
      const w = S.win;
      if (Math.abs(fy) > 1e-6 * (1 + Math.abs(fx))) {
        // Local graph y = g(x): solve F(x, y) = 0 for y by Newton, continuing from P while F_y keeps its sign.
        const branch = (dir) => {
          const pts = [];
          let y = P[1];
          for (const x of linspace(P[0], P[0] + dir * w, 60)) {
            const r = newton(([yy]) => [fn.f(x, yy)], [y]);
            if (!r || Math.sign(Fy(x, r[0])) !== Math.sign(fy) || Math.abs(r[0] - y) > w) break;
            y = r[0]; pts.push([x, y]);
          }
          return pts;
        };
        const gpts = [...branch(-1).reverse(), ...branch(1)];
        const slope = -fx / fy;
        traces.push(
          { x: gpts.map((p) => p[0]), y: gpts.map((p) => p[1]), mode: "lines", name: "y = g(x) local", line: { color: c.accent, width: 6 }, opacity: 0.75 },
          { x: [P[0] - w, P[0] + w], y: [P[1] - w * slope, P[1] + w * slope], mode: "lines", name: `tangent, g'(x) = ${fmt(slope)}`, line: { color: c.warn, width: 2, dash: "dash" } });
      } else if (Math.abs(fx) > 1e-6) {
        traces.push({ x: [P[0], P[0]], y: [P[1] - w, P[1] + w], mode: "lines", name: "tangent vertical", line: { color: c.warn, width: 2, dash: "dash" } });
      }
      const gn = norm([fx, fy]) || 1;
      ann.push(arrow2d(P, [fx / gn * 0.4, fy / gn * 0.4], c.ok, "∇F"));
      traces.push(
        marker(P, c.bad, "P"),
        ...(vt.length ? [{ x: vt.map((p) => p[0]), y: vt.map((p) => p[1]), mode: "markers", name: "F_y = 0 (tangent vertical)", marker: { color: c.warn, size: 11, symbol: "square" } }] : []),
        ...(sing.length ? [{ x: sing.map((p) => p[0]), y: sing.map((p) => p[1]), mode: "markers", name: "singular (∇F = 0)", marker: { color: c.bad, size: 12, symbol: "x" } }] : []),
        { x: [null], y: [null], mode: "lines", name: "∇F(P)", line: { color: c.ok, width: 3 } });
      draw(fig.div, traces, layout2d({ xaxis: axis2d({ scaleanchor: "y", range: [-S.R, S.R] }), yaxis: axis2d({ range: [-S.R, S.R] }), annotations: ann }));
      const tx = fn.tex(["x"]), ty = fn.tex(["y"]);
      out.set(
        tx && ty ? el("div", { text: `$\\partial_xF=${tx}$, $\\partial_yF=${ty}$` }) : null,
        el("div", { text: `$P=${vfmt(P)}$` }),
        el("div", { text: `$\\partial_xF(P)=${fmt(fx)}$, $\\partial_yF(P)=${fmt(fy)}$` }),
        Math.abs(fy) > 1e-6 * (1 + Math.abs(fx))
          ? verdict(`F_y(P) ≠ 0: a prop de P la corba és y = g(x), amb g'(x) = −F_x/F_y = ${fmt(-fx / fy)}.`, "ok")
          : Math.abs(fx) > 1e-6
            ? verdict("F_y(P) = 0 però F_x(P) ≠ 0: no és gràfica de y = g(x), però sí de x = h(y).", "warn")
            : verdict("∇F(P) = 0: punt singular, cap de les dues versions del teorema s'aplica.", "bad"),
        para("El gradient ∇F és sempre perpendicular a la corba: la tangent és horitzontal quan F_x = 0 i vertical quan F_y = 0.", "small muted"));
    };
    side.append(
      chips("Exemples", presets, (p) => { ff.set(p.src); S.R = p.R; render(); }),
      ff.node, ss.node, sw.node, out.node);
    main.append(fig.node);
    render();
  },
});

/* ---------- Tema 5: Taylor polynomials ---------- */

const fact = (n) => (n <= 1 ? 1 : n * fact(n - 1));

function taylor(fn, a, order) {
  // Coefficients c[i][j] of (x-a1)^i (y-a2)^j for i + j <= order (Teorema 14 del Tema 5).
  const terms = [];
  for (let m = 0; m <= order; m++) for (let i = m; i >= 0; i--) {
    const j = m - i;
    const seq = [...Array(i).fill("x"), ...Array(j).fill("y")];
    terms.push({ i, j, c: fn.d(...seq).f(...a) / (fact(i) * fact(j)) });
  }
  const P = (x, y) => terms.reduce((s, t) => s + t.c * (x - a[0]) ** t.i * (y - a[1]) ** t.j, 0);
  return { terms, P };
}

function taylorTex(terms, a) {
  const X = a[0] ? `(x${a[0] > 0 ? "-" : "+"}${fmt(Math.abs(a[0]), 2)})` : "x";
  const Y = a[1] ? `(y${a[1] > 0 ? "-" : "+"}${fmt(Math.abs(a[1]), 2)})` : "y";
  const pw = (b, k) => (k === 0 ? "" : k === 1 ? b : `${b}^{${k}}`);
  if (terms.some((t) => !Number.isFinite(t.c))) return "\\text{(}f\\text{ no és derivable a }a\\text{)}";
  let s = "";
  for (const t of terms) {
    if (Math.abs(t.c) < 5e-5) continue;
    const mono = pw(X, t.i) + pw(Y, t.j);
    const coef = fmt(Math.abs(t.c), 4);
    const sign = t.c < 0 ? "-" : s ? "+" : "";
    s += `${sign}${mono && coef === "1" ? "" : coef}${mono}`;
  }
  return s || "0";
}

lab({
  id: "taylor", tema: 5, seccio: "Fórmula de Taylor", icon: "Σ",
  titol: "Polinomi de Taylor",
  resum: "Superposa a $f$ el seu polinomi de Taylor d'ordre 1, 2 o 3 en un punt, i mira com l'error decreix com $\\|h\\|^{r+1}$.",
  idea: "El polinomi de Taylor d'ordre $r$ en $a$ aproxima $f$ amb un error $o(\\|x-a\\|^r)$ (Teorema 14 del Tema 5). D'ordre 1 és el pla tangent; d'ordre 2 hi afegeix la hessiana i ja capta si la superfície és un bol, una cúpula o una sella.",
  refs: ["T5.12", "T5.14", "T5.15", "T5.16", "T5.17"],
  mount({ side, main }) {
    const c = pal();
    const S = { a: 0.5, b: 0.3, r: 2, R: 1.5 };
    const ff = formulaField({ label: "$f(x,y)=$", value: "exp(x)*sin(y) + x*y^2" }, () => render());
    const sa = slider({ label: "$a_1$", min: -1.5, max: 1.5, value: S.a }, (v) => { S.a = v; render(); });
    const sb = slider({ label: "$a_2$", min: -1.5, max: 1.5, value: S.b }, (v) => { S.b = v; render(); });
    const sr = slider({ label: "Ordre $r$", min: 1, max: 3, step: 1, value: S.r, format: (v) => String(v) }, (v) => { S.r = v; render(); });
    const sR = slider({ label: "Finestra al voltant de $a$", min: 0.2, max: 3, step: 0.05, value: S.R }, (v) => { S.R = v; render(); });
    const fig3 = plotBox("$f$ (blau) i $P_r$ (taronja)");
    const figE = plotBox("$\\max_{\\|h\\|=\\rho}|f(a+h)-P_r(a+h)|$ (escala log)");
    const out = readout();
    const render = () => {
      const fn = ff.fn; if (!fn) return;
      const a = [S.a, S.b];
      const T = taylor(fn, a, S.r);
      const X = [a[0] - S.R, a[0] + S.R], Y = [a[1] - S.R, a[1] + S.R];
      const g = clipGrid(grid(fn.f, X, Y, 61));
      const gp = grid(T.P, X, Y, 41);
      draw(fig3.div, [
        surface(g, { opacity: 0.85, name: "f" }),
        { ...surface(gp), colorscale: [[0, c.warn], [1, c.warn]], opacity: 0.6, name: `P${S.r}`, contours: {}, hoverinfo: "skip" },
        marker([...a, fn.f(...a)], c.bad, "(a, f(a))"),
      ], layout3d({}, { zaxis: axis3d("z", { range: g.range }) }));
      const rs = linspace(-3, 0, 31).map((e) => 10 ** e);
      const angles = linspace(0, 2 * Math.PI, 181);
      const err = (P) => rs.map((r) => Math.max(...angles.map((t) => Math.abs(fn.f(a[0] + r * Math.cos(t), a[1] + r * Math.sin(t)) - P(a[0] + r * Math.cos(t), a[1] + r * Math.sin(t)))).filter(Number.isFinite)));
      const traces = [];
      for (let k = 1; k <= 3; k++) {
        const e = err(taylor(fn, a, k).P);
        traces.push({ x: rs, y: e.map((v) => Math.max(v, 1e-16)), mode: "lines+markers", name: `r = ${k}`,
          line: { color: k === S.r ? c.warn : c.muted, width: k === S.r ? 3 : 1.4, dash: ["solid", "dash", "dot"][k - 1] }, marker: { size: k === S.r ? 6 : 4 } });
      }
      // Reference slope ρ^(r+1).
      const e0 = traces[S.r - 1].y[15];
      traces.push({ x: rs, y: rs.map((r) => e0 * (r / rs[15]) ** (S.r + 1)), mode: "lines", name: `pendent ρ^${S.r + 1}`, line: { color: c.accent, width: 1, dash: "dashdot" } });
      draw(figE.div, traces, layout2d({ xaxis: axis2d({ type: "log", title: { text: "ρ" }, exponentformat: "power" }), yaxis: axis2d({ type: "log", exponentformat: "power" }) }));
      out.set(
        el("div", { text: `$a=${vfmt(a, 2)}$` }),
        el("div", { class: "vl-scroll", text: `$P_{${S.r}}(x,y)=${taylorTex(T.terms, a)}$` }),
        para(`En escala log-log, l'error de l'ordre r és una recta de pendent r+1: dividir ρ per 10 divideix l'error per 10^${S.r + 1}.`, "small muted"));
    };
    side.append(
      chips("Exemples", [
        { tex: "e^x\\sin y+xy^2", src: "exp(x)*sin(y) + x*y^2" },
        { tex: "\\cos(x)\\cos(y)", src: "cos(x)*cos(y)" },
        { tex: "\\ln(1+x^2+y^2)", src: "log(1 + x^2 + y^2)" },
        { tex: "\\sqrt{1+x+2y}", src: "sqrt(1 + x + 2*y)" },
      ], (p) => { ff.set(p.src); render(); }, ff.fn?.src),
      ff.node, sa.node, sb.node, sr.node, sR.node, out.node);
    main.append(el("div", { class: "vl-row" }, fig3.node, figE.node));
    render();
  },
});

/* ---------- Tema 5: critical points and the Hessian ---------- */

const CLASS = {
  min: { label: "mínim local", color: () => pal().ok, symbol: "circle" },
  max: { label: "màxim local", color: () => pal().bad, symbol: "diamond" },
  sella: { label: "punt de sella", color: () => pal().warn, symbol: "x" },
  deg: { label: "degenerat (el criteri no decideix)", color: () => pal().muted, symbol: "square" },
};

function classify(H) {
  const d1 = H[0][0], d2 = H[0][0] * H[1][1] - H[0][1] * H[1][0];
  const scale = Math.max(1, ...H.flat().map(Math.abs)) ** 2;
  if (Math.abs(d2) < 1e-7 * scale) return "deg";
  if (d2 < 0) return "sella";
  return d1 > 0 ? "min" : "max";
}

function criticalPoints(fn, R, seeds = 14) {
  // Newton on ∇f = 0 from a grid of seeds (Hessian from the symbolic second derivatives).
  const found = [];
  for (const x0 of linspace(-R, R, seeds)) for (const y0 of linspace(-R, R, seeds)) {
    const p = newton(([x, y]) => fn.grad(x, y), [x0, y0], { iters: 50, tol: 1e-12 });
    if (p && Math.abs(p[0]) <= R * 1.001 && Math.abs(p[1]) <= R * 1.001) found.push(p.map((v) => (Math.abs(v) < 1e-9 ? 0 : v)));
  }
  return dedupe(found, 1e-3).slice(0, 40);
}

lab({
  id: "extrems", tema: 5, seccio: "Extrems locals", icon: "⛰",
  titol: "Punts crítics i hessiana",
  resum: "Troba els punts crítics de $f$, classifica'ls amb la hessiana (Sylvester, valors propis) i compara $f$ amb la seva aproximació quadràtica.",
  idea: "Als extrems locals el gradient s'anul·la (Proposició 23 del Tema 5). A un punt crític, $f(a+h)\\approx f(a)+\\tfrac12 h^THf(a)h$: si la forma quadràtica és definida positiva és un mínim, definida negativa un màxim, i indefinida una sella (Teorema 33 del Tema 5). Si és semidefinida, el criteri no decideix.",
  refs: ["T5.22", "T5.23", "T5.25", "T5.29", "T5.31", "T5.32", "T5.33", "T5.34", "T5.35"],
  mount({ side, main }) {
    const c = pal();
    const presets = [
      { tex: "x^3-3x+y^2", src: "x^3 - 3*x + y^2", R: 2 },
      { tex: "x^4+y^4-4xy", src: "x^4 + y^4 - 4*x*y", R: 1.8 },
      { tex: "xy\\,e^{-(x^2+y^2)/2}", src: "x*y*exp(-(x^2 + y^2)/2)", R: 2.5 },
      { tex: "\\sin x\\sin y", src: "sin(x)*sin(y)", R: 4 },
      { tex: "x^4+y^2", src: "x^4 + y^2", R: 1.5, title: "Hessiana semidefinida: mínim que el criteri no veu" },
      { tex: "x^3-3xy^2", src: "x^3 - 3*x*y^2", R: 1.5, title: "Sella de mico: degenerat" },
    ];
    const S = { R: 2, sel: 0, quad: true };
    const ff = formulaField({ label: "$f(x,y)=$", value: presets[0].src }, () => { S.sel = 0; render(); });
    const sR = slider({ label: "Finestra $[-R,R]^2$", min: 0.5, max: 6, step: 0.1, value: S.R }, (v) => { S.R = v; render(); });
    const fig3 = plotBox("Gràfica i aproximació quadràtica al punt triat");
    const fig2 = plotBox("Mapa de nivell i punts crítics (clica'n un)");
    const list = el("div", { class: "vl-list" });
    const out = readout();
    let pts = [];
    const render = () => {
      const fn = ff.fn; if (!fn) return;
      pts = criticalPoints(fn, S.R).map((p) => ({ p, H: fn.hess(...p), z: fn.f(...p) })).map((q) => ({ ...q, cls: classify(q.H) }));
      S.sel = clamp(S.sel, 0, Math.max(0, pts.length - 1));
      const g = clipGrid(grid(fn.f, [-S.R, S.R], [-S.R, S.R], 71));
      const byCls = Object.keys(CLASS).map((k) => ({ k, q: pts.filter((p) => p.cls === k) })).filter((b) => b.q.length);
      const sel = pts[S.sel];
      const quad = [];
      if (sel && S.quad) {
        const h = S.R / 3, [x0, y0] = sel.p, H = sel.H;
        quad.push({ ...flatSurface(linspace(x0 - h, x0 + h, 25), linspace(y0 - h, y0 + h, 25),
          (x, y) => sel.z + 0.5 * (H[0][0] * (x - x0) ** 2 + 2 * H[0][1] * (x - x0) * (y - y0) + H[1][1] * (y - y0) ** 2), c.warn, { opacity: 0.6 }), name: "f(a) + ½ hᵀHh" });
      }
      draw(fig3.div, [
        surface(g, { opacity: 0.85 }),
        ...quad,
        ...byCls.map(({ k, q }) => ({ type: "scatter3d", mode: "markers", x: q.map((p) => p.p[0]), y: q.map((p) => p.p[1]), z: q.map((p) => p.z), name: CLASS[k].label,
          marker: { color: CLASS[k].color(), size: 6, symbol: { circle: "circle", diamond: "diamond", x: "x", square: "square" }[CLASS[k].symbol], line: { color: c.panel, width: 1 } } })),
      ], layout3d({}, { zaxis: axis3d("z", { range: g.range }) }));
      draw(fig2.div, [
        contour2d(g),
        ...byCls.map(({ k, q }) => ({ x: q.map((p) => p.p[0]), y: q.map((p) => p.p[1]), mode: "markers", name: CLASS[k].label,
          customdata: q.map((p) => pts.indexOf(p)), marker: { color: CLASS[k].color(), size: 13, symbol: CLASS[k].symbol, line: { color: c.panel, width: 2 } },
          hovertemplate: "(%{x:.3f}, %{y:.3f})<extra>" + CLASS[k].label + "</extra>" })),
        ...(sel ? [{ x: [sel.p[0]], y: [sel.p[1]], mode: "markers", name: "triat", showlegend: false, hoverinfo: "skip", marker: { size: 24, color: "rgba(0,0,0,0)", line: { color: c.ink, width: 2 } } }] : []),
      ], layout2d({ xaxis: axis2d({ scaleanchor: "y", range: [-S.R, S.R] }), yaxis: axis2d({ range: [-S.R, S.R] }) }));
      fig2.div.removeAllListeners?.("plotly_click");
      fig2.div.on?.("plotly_click", (e) => { const i = e.points?.[0]?.customdata; if (i != null) { S.sel = i; render(); } });
      list.replaceChildren(...pts.map((q, i) => {
        const b = el("button", { type: "button", class: `vl-item${i === S.sel ? " on" : ""}` },
          el("span", { class: "vl-dot", style: `background:${CLASS[q.cls].color()}` }),
          el("span", { text: `${vfmt(q.p, 3)} · ${CLASS[q.cls].label}` }));
        b.addEventListener("click", () => { S.sel = i; render(); });
        return b;
      }));
      if (!pts.length) list.append(para("Cap punt crític a la finestra.", "muted small"));
      if (!sel) { out.set(); return; }
      const H = sel.H, [l1, l2] = eig2(H);
      const d1 = H[0][0], d2 = H[0][0] * H[1][1] - H[0][1] * H[1][0];
      const ht = [fn.tex(["x", "x"]), fn.tex(["x", "y"]), fn.tex(["y", "y"])];
      out.set(
        ht.every(Boolean) ? el("div", { class: "vl-scroll", text: `$Hf=\\begin{pmatrix}${ht[0]}&${ht[1]}\\\\${ht[1]}&${ht[2]}\\end{pmatrix}$` }) : null,
        el("div", { text: `$a=${vfmt(sel.p)}$, $f(a)=${fmt(sel.z)}$` }),
        el("div", { text: `$Hf(a)=\\begin{pmatrix}${fmt(H[0][0])}&${fmt(H[0][1])}\\\\${fmt(H[1][0])}&${fmt(H[1][1])}\\end{pmatrix}$` }),
        el("div", { text: `Sylvester: $\\Delta_1=${fmt(d1)}$, $\\Delta_2=${fmt(d2)}$` }),
        el("div", { text: `Valors propis: $\\lambda_1=${fmt(l1)}$, $\\lambda_2=${fmt(l2)}$` }),
        verdict({
          min: "Δ₁ > 0 i Δ₂ > 0 (forma definida positiva): mínim local estricte.",
          max: "Δ₁ < 0 i Δ₂ > 0 (forma definida negativa): màxim local estricte.",
          sella: "Δ₂ < 0 (forma indefinida, valors propis de signe oposat): punt de sella.",
          deg: "Δ₂ = 0: forma semidefinida. Cal estudiar f directament (ordres superiors, restriccions a rectes…).",
        }[sel.cls], { min: "ok", max: "ok", sella: "warn", deg: "bad" }[sel.cls]));
    };
    side.append(
      chips("Exemples", presets, (p) => { ff.set(p.src); S.R = p.R; sR.set(p.R); S.sel = 0; render(); }),
      ff.node, sR.node,
      toggle("Aproximació quadràtica al punt triat", S.quad, (v) => { S.quad = v; render(); }).node,
      el("div", { class: "vl-group" }, el("span", { class: "vl-label", text: "Punts crítics trobats" }), list),
      out.node);
    main.append(el("div", { class: "vl-row" }, fig3.node, fig2.node));
    render();
  },
});

/* ---------- Tema 6: Lagrange multipliers in the plane ---------- */

lab({
  id: "lagrange", tema: 6, seccio: "Extrems condicionats", icon: "λ",
  titol: "Multiplicadors de Lagrange",
  resum: "Mou un punt sobre la restricció $g=0$ i mira $\\nabla f$ i $\\nabla g$: als extrems condicionats són paral·lels, $\\nabla f=\\lambda\\nabla g$.",
  idea: "Un extrem de $f$ sobre la corba $g=0$ és un punt on la corba de nivell de $f$ és tangent a la restricció; equivalentment, $\\nabla f(a)$ és normal a la corba, $\\nabla f(a)=\\lambda\\nabla g(a)$ (Proposició 13 del Tema 6 i Corol·lari 17 del Tema 6). Si la restricció és compacta, Weierstrass garanteix màxim i mínim, i són entre aquests candidats.",
  refs: ["T6.12", "T6.13", "T6.16", "T6.17", "T6.18", "T2.23"],
  mount({ side, main }) {
    const c = pal();
    const presets = [
      { tex: "x+y\\ \\text{a}\\ x^2+y^2=1", f: "x + y", g: "x^2 + y^2 - 1", R: 1.8 },
      { tex: "xy\\ \\text{a}\\ \\tfrac{x^2}{4}+y^2=1", f: "x*y", g: "x^2/4 + y^2 - 1", R: 2.5 },
      { tex: "x^2+2y^2\\ \\text{a}\\ x+y=1", f: "x^2 + 2*y^2", g: "x + y - 1", R: 2, title: "Restricció no compacta: només hi ha mínim" },
      { tex: "x^2-y^2\\ \\text{a}\\ x^4+y^4=1", f: "x^2 - y^2", g: "x^4 + y^4 - 1", R: 1.6 },
      { tex: "y\\ \\text{a}\\ y^3=x^2", f: "y", g: "y^3 - x^2", R: 1.2, title: "Mínim en un punt singular: ∇g = 0 i Lagrange no el detecta" },
    ];
    const S = { ...presets[0], s: 0.1, show3d: true };
    const ffi = formulaField({ label: "$f(x,y)=$", value: S.f }, () => render());
    const gfi = formulaField({ label: "$g(x,y)=0$, amb $g=$", value: S.g }, () => render());
    const sR = slider({ label: "Finestra $[-R,R]^2$", min: 0.5, max: 5, step: 0.1, value: S.R }, (v) => { S.R = v; render(); });
    const ss = slider({ label: "Posició sobre la restricció", min: 0, max: 1, step: 0.002, value: S.s }, (v) => { S.s = v; render(); });
    const fig2 = plotBox("Corbes de nivell de $f$ i restricció $g=0$");
    const figP = plotBox("$f$ al llarg de la restricció");
    const fig3 = plotBox("La restricció aixecada sobre la gràfica de $f$");
    const out = readout();
    const cands = el("div", { class: "vl-list" });
    const render = () => {
      const F = ffi.fn, G = gfi.fn; if (!F || !G) return;
      const R = S.R;
      const gg = grid(G.f, [-R, R], [-R, R], 241);
      const lines = contourLines(gg, 0);
      const gf = clipGrid(grid(F.f, [-R, R], [-R, R], 81));
      if (!lines.length) { draw(fig2.div, [contour2d(gf)], layout2d()); out.set(verdict("La restricció g = 0 no talla la finestra.", "warn")); return; }
      const arc = arcParam(lines);
      // Candidates: solve ∇f = λ∇g, g = 0 (3 unknowns) from seeds where the 2D cross product ∇f × ∇g changes sign.
      const cross = (x, y) => { const a = F.grad(x, y), b = G.grad(x, y); return a[0] * b[1] - a[1] * b[0]; };
      const seeds = [];
      for (const l of lines) for (let k = 0; k < l.length - 1; k++) if (cross(...l[k]) * cross(...l[k + 1]) <= 0) seeds.push(l[k]);
      const sols = [];
      for (const s of seeds) {
        const gs = G.grad(...s), fs = F.grad(...s);
        const lam0 = dot(fs, gs) / (dot(gs, gs) || 1);
        const r = newton(([x, y, l]) => { const a = F.grad(x, y), b = G.grad(x, y); return [a[0] - l * b[0], a[1] - l * b[1], G.f(x, y)]; }, [...s, lam0]);
        if (r && Math.abs(r[0]) <= R && Math.abs(r[1]) <= R) sols.push(r);
      }
      const cand = dedupe(sols, 1e-4).map(([x, y, l]) => ({ p: [x, y], lam: l, v: F.f(x, y) }));
      // Singular points of the constraint (∇g = 0 on g = 0): Lagrange's condition does not apply there.
      const sing = [];
      for (const l of lines) for (const p of l) if (norm(G.grad(...p)) < 0.05) {
        const r = newton(([x, y]) => G.grad(x, y), p);
        if (r && Math.abs(G.f(...r)) < 1e-8) sing.push(r);
      }
      const singPts = dedupe(sing, 1e-3);
      const closed = lines.every((l) => norm([l[0][0] - l[l.length - 1][0], l[0][1] - l[l.length - 1][1]]) < 1e-9);
      const vals = [...cand.map((q) => q.v), ...singPts.map((p) => F.f(...p))];
      const vmax = Math.max(...vals), vmin = Math.min(...vals);
      const tie = (v, w) => Math.abs(v - w) < 1e-7 * (1 + Math.abs(w));
      const kind = (v) => (!closed ? "" : tie(v, vmax) ? "màxim" : tie(v, vmin) ? "mínim" : "");
      const at = arc.at(S.s), P = at.p;
      const gfP = F.grad(...P), ggP = G.grad(...P);
      const sc = 0.25 * R;
      const u = (v) => { const n = norm(v) || 1; return v.map((x) => (x / n) * sc); };
      const ang = Math.acos(clamp(Math.abs(dot(gfP, ggP)) / ((norm(gfP) * norm(ggP)) || 1), 0, 1)) * 180 / Math.PI;
      const fP = F.f(...P);
      draw(fig2.div, [
        contour2d(gf, { opacity: 0.55 }),
        { ...joinLines(lines), mode: "lines", name: "g = 0", line: { color: c.ink, width: 3.5 } },
        { ...joinLines(contourLines(gf, fP)), mode: "lines", name: "nivell de f per P", line: { color: c.accent, width: 2, dash: "dash" } },
        ...(cand.length ? [{ x: cand.map((q) => q.p[0]), y: cand.map((q) => q.p[1]), mode: "markers", name: "∇f = λ∇g",
          marker: { color: cand.map((q) => ({ "màxim": c.bad, "mínim": c.ok }[kind(q.v)] || c.warn)), size: 13, symbol: "star", line: { color: c.panel, width: 1 } },
          text: cand.map((q) => `λ = ${fmt(q.lam)}, f = ${fmt(q.v)}`), hovertemplate: "%{text}<extra></extra>" }] : []),
        ...(singPts.length ? [{ x: singPts.map((p) => p[0]), y: singPts.map((p) => p[1]), mode: "markers", name: "∇g = 0 (singular)", marker: { color: c.bad, size: 13, symbol: "x" } }] : []),
        marker(P, c.bad, "P"),
        { x: [null], y: [null], mode: "lines", name: "∇f(P)", line: { color: c.ok, width: 3 } },
        { x: [null], y: [null], mode: "lines", name: "∇g(P)", line: { color: c.reveal, width: 3 } },
      ], layout2d({
        xaxis: axis2d({ scaleanchor: "y", range: [-R, R] }), yaxis: axis2d({ range: [-R, R] }),
        annotations: [arrow2d(P, u(gfP), c.ok, "∇f"), arrow2d(P, u(ggP), c.reveal, "∇g")],
      }));
      // Profile of f along the curve.
      const ss_ = linspace(0, 1, 600);
      const prof = ss_.map((t) => { const q = arc.at(t); return { s: t * arc.total, v: F.f(...q.p), li: q.seg.li }; });
      const profX = [], profY = [];
      prof.forEach((q, i) => { if (i && q.li !== prof[i - 1].li) { profX.push(null); profY.push(null); } profX.push(q.s); profY.push(q.v); });
      const sOf = (p) => {
        let best = null;
        for (const sg of arc.segs) {
          const d = [sg.b[0] - sg.a[0], sg.b[1] - sg.a[1]];
          const t = clamp(dot([p[0] - sg.a[0], p[1] - sg.a[1]], d) / (dot(d, d) || 1), 0, 1);
          const dist = norm([sg.a[0] + t * d[0] - p[0], sg.a[1] + t * d[1] - p[1]]);
          if (!best || dist < best.dist) best = { dist, s: sg.s0 + t * sg.len };
        }
        return best.s;
      };
      draw(figP.div, [
        { x: profX, y: profY, mode: "lines", name: "f sobre g = 0", line: { color: c.accent, width: 2.5 } },
        ...(cand.length ? [{ x: cand.map((q) => sOf(q.p)), y: cand.map((q) => q.v), mode: "markers", name: "candidats de Lagrange", marker: { color: c.warn, size: 12, symbol: "star" } }] : []),
        marker([S.s * arc.total, fP], c.bad, "P"),
      ], layout2d({ xaxis: axis2d({ title: { text: "longitud d'arc" } }), showlegend: false }));
      if (S.show3d) {
        draw(fig3.div, [
          surface(gf, { opacity: 0.7 }),
          { type: "scatter3d", mode: "lines", ...joinLines(lines, (x, y) => F.f(x, y)), name: "f sobre g = 0", line: { color: c.ink, width: 6 } },
          ...(cand.length ? [{ type: "scatter3d", mode: "markers", x: cand.map((q) => q.p[0]), y: cand.map((q) => q.p[1]), z: cand.map((q) => q.v), name: "candidats", marker: { color: c.warn, size: 6 } }] : []),
          marker([...P, fP], c.bad, "P"),
        ], layout3d({}, { zaxis: axis3d("z", { range: gf.range }) }));
      }
      fig3.node.classList.toggle("hidden", !S.show3d);
      // Singular points of the constraint are candidates too: Lagrange's condition says nothing there.
      const all = [...cand, ...singPts.map((p) => ({ p, lam: NaN, v: F.f(...p), sing: true }))];
      cands.replaceChildren(...all.map((q) => {
        const tag = kind(q.v) ? ` · ${kind(q.v)}` : "";
        const b = el("button", { type: "button", class: "vl-item" },
          el("span", { text: `${vfmt(q.p)}  ${q.sing ? "∇g=0" : `λ=${fmt(q.lam)}`}  f=${fmt(q.v)}${tag}` }));
        b.addEventListener("click", () => { S.s = sOf(q.p) / arc.total; ss.set(S.s); render(); });
        return b;
      }));
      if (!all.length) cands.append(para("Cap solució de ∇f = λ∇g a la finestra.", "muted small"));
      const parallel = ang < 1.5;
      out.set(
        el("div", { text: `$P=${vfmt(P)}$, $f(P)=${fmt(fP)}$` }),
        el("div", { text: `$\\nabla f(P)=${vfmt(gfP)}$, $\\nabla g(P)=${vfmt(ggP)}$` }),
        el("div", { text: `Angle entre $\\nabla f$ i $\\nabla g$: $${fmt(ang, 1)}^\\circ$` }),
        parallel
          ? verdict(`∇f ∥ ∇g: P és un punt crític condicionat, amb λ ≈ ${fmt(dot(gfP, ggP) / dot(ggP, ggP))}. La corba de nivell de f és tangent a la restricció.`, "ok")
          : verdict("∇f no és paral·lel a ∇g: ∇f té component tangent a la corba, així que movent-se sobre la restricció f encara creix o decreix.", ""),
        closed ? para("La restricció és tancada i fitada (compacta): f hi assoleix màxim i mínim (Teorema 23 del Tema 2), i són entre els candidats (o als punts singulars).", "small muted")
          : para("La restricció no és compacta en aquesta finestra: un candidat pot no ser extrem global.", "small muted"));
    };
    side.append(
      chips("Exemples", presets, (p) => { Object.assign(S, p); ffi.set(p.f); gfi.set(p.g); sR.set(p.R); render(); }),
      ffi.node, gfi.node, sR.node, ss.node,
      toggle("Vista 3D", S.show3d, (v) => { S.show3d = v; render(); }).node,
      el("div", { class: "vl-group" }, el("span", { class: "vl-label", text: "Candidats (clica per anar-hi)" }), cands),
      out.node);
    main.append(el("div", { class: "vl-row" }, fig2.node, figP.node), fig3.node);
    render();
  },
});

/* ---------- Tema 6: manifolds, tangent and normal spaces, constrained extrema in R^3 ---------- */

const MANIFOLDS = [
  { tex: "x^2+y^2+z^2=1", nom: "Esfera", phi: "x^2 + y^2 + z^2 - 1", rho: (u, v) => [Math.cos(u) * Math.sin(v), Math.sin(u) * Math.sin(v), Math.cos(v)], U: [0, 2 * Math.PI], V: [0, Math.PI] },
  { tex: "\\tfrac{x^2}{2.6}+y^2+\\tfrac{z^2}{0.5}=1", nom: "El·lipsoide", phi: "x^2/2.6 + y^2 + z^2/0.5 - 1", rho: (u, v) => [Math.sqrt(2.6) * Math.cos(u) * Math.sin(v), Math.sin(u) * Math.sin(v), Math.sqrt(0.5) * Math.cos(v)], U: [0, 2 * Math.PI], V: [0, Math.PI] },
  { tex: "x^2+y^2-z^2=1", nom: "Hiperboloide", phi: "x^2 + y^2 - z^2 - 1", rho: (u, v) => [Math.cosh(v) * Math.cos(u), Math.cosh(v) * Math.sin(u), Math.sinh(v)], U: [0, 2 * Math.PI], V: [-1.2, 1.2] },
  { tex: "x^2+y^2=z^2", nom: "Con (no és varietat a l'origen)", phi: "x^2 + y^2 - z^2", rho: (u, v) => [v * Math.cos(u), v * Math.sin(u), v], U: [0, 2 * Math.PI], V: [-1.2, 1.2] },
  { tex: "(\\sqrt{x^2+y^2}-2)^2+z^2=\\tfrac14", nom: "Tor", phi: "(sqrt(x^2 + y^2) - 2)^2 + z^2 - 0.25", rho: (u, v) => [(2 + 0.5 * Math.cos(v)) * Math.cos(u), (2 + 0.5 * Math.cos(v)) * Math.sin(u), 0.5 * Math.sin(v)], U: [0, 2 * Math.PI], V: [0, 2 * Math.PI] },
];

lab({
  id: "varietats", tema: 6, seccio: "Espais tangent i normal", icon: "◯",
  titol: "Varietats: tangent, normal i extrems",
  resum: "Superfícies $\\Phi=0$ a $\\mathbb{R}^3$ amb el pla tangent i el vector normal $\\nabla\\Phi$. Busca els extrems d'una $f$ sobre la superfície: la component tangent de $\\nabla f$ s'hi anul·la.",
  idea: "Si $\\nabla\\Phi(p)\\neq0$, $M=\\{\\Phi=0\\}$ és una varietat a prop de $p$, amb $N_pM=\\langle\\nabla\\Phi(p)\\rangle$ i $T_pM=\\nabla\\Phi(p)^\\perp$ (Teorema 10 del Tema 6). Un extrem condicionat de $f$ és un punt on $\\nabla f(p)\\in N_pM$, és a dir, on la projecció de $\\nabla f$ al pla tangent és zero (Proposició 13 del Tema 6). Visualment: la superfície de nivell de $f$ hi és tangent a $M$.",
  refs: ["T6.2", "T6.3", "T6.6", "T6.7", "T6.9", "T6.10", "T6.11", "T6.13", "T6.17"],
  mount({ side, main }) {
    const c = pal();
    const S = { m: 0, u: 0.8, v: 1.0, level: true };
    const ff = formulaField({ label: "$f(x,y,z)=$", value: "x + 2*y + 3*z", vars: ["x", "y", "z"] }, () => render());
    const su = slider({ label: "Paràmetre $u$", min: 0, max: 2 * Math.PI, value: S.u }, (v) => { S.u = v; render(); });
    const sv = slider({ label: "Paràmetre $v$", min: 0, max: Math.PI, value: S.v }, (v) => { S.v = v; render(); });
    const fig = plotBox("Varietat, pla tangent, normal i $\\nabla f$");
    const out = readout();
    const opt = el("div", { class: "vl-btns" });
    const goExt = (sign) => {
      // Coarse grid search of f∘ρ over the parameter domain, then local refinement around the best cell.
      const man = MANIFOLDS[S.m], fn = ff.fn; if (!fn) return;
      const val = (u, v) => sign * fn.f(...man.rho(u, v));
      let best = null;
      for (const u of linspace(...man.U, 120)) for (const v of linspace(...man.V, 80)) {
        const w = val(u, v);
        if (Number.isFinite(w) && (!best || w > best.w)) best = { u, v, w };
      }
      let du = (man.U[1] - man.U[0]) / 120, dv = (man.V[1] - man.V[0]) / 80;
      for (let k = 0; k < 40; k++) {
        for (const [a, b] of [[du, 0], [-du, 0], [0, dv], [0, -dv]]) {
          const u = best.u + a, v = clamp(best.v + b, ...man.V), w = val(u, v);
          if (w > best.w) best = { u, v, w };
        }
        du *= 0.7; dv *= 0.7;
      }
      S.u = ((best.u - man.U[0]) % (man.U[1] - man.U[0]) + (man.U[1] - man.U[0])) % (man.U[1] - man.U[0]) + man.U[0];
      S.v = best.v; su.set(S.u); sv.set(S.v); render();
    };
    for (const [label, sgn] of [["Ves al màxim de f", 1], ["Ves al mínim de f", -1]]) {
      const b = el("button", { type: "button", class: "btn ghost small-btn", text: label });
      b.addEventListener("click", () => goExt(sgn));
      opt.append(b);
    }
    let phi = null;
    const render = () => {
      const man = MANIFOLDS[S.m], fn = ff.fn; if (!fn) return;
      phi ??= new Fn(man.phi, ["x", "y", "z"]);
      const us = linspace(...man.U, 60), vs = linspace(...man.V, 40);
      const P = vs.map((v) => us.map((u) => man.rho(u, v)));
      const p = man.rho(S.u, S.v);
      const n = phi.grad(...p), nn = norm(n);
      const gf = fn.grad(...p);
      // Tangent basis from the parametrization (numeric ρ_u, ρ_v), orthonormalized.
      const h = 1e-5;
      const ru = man.rho(S.u + h, S.v).map((x, i) => (x - p[i]) / h);
      const rv = man.rho(S.u, S.v + h).map((x, i) => (x - p[i]) / h);
      const e1 = ru.map((x) => x / (norm(ru) || 1));
      const rv2 = rv.map((x, i) => x - dot(rv, e1) * e1[i]);
      const e2 = rv2.map((x) => x / (norm(rv2) || 1));
      const plane = linspace(-0.6, 0.6, 2);
      const tp = { x: [], y: [], z: [] };
      for (const b of plane) { const row = { x: [], y: [], z: [] }; for (const a of plane) { const q = p.map((x, i) => x + a * e1[i] + b * e2[i]); row.x.push(q[0]); row.y.push(q[1]); row.z.push(q[2]); } tp.x.push(row.x); tp.y.push(row.y); tp.z.push(row.z); }
      const gT = [dot(gf, e1), dot(gf, e2)];
      const gTan = e1.map((x, i) => gT[0] * x + gT[1] * e2[i]);
      const nU = nn > 1e-9 ? n.map((x) => x / nn) : [0, 0, 0];
      const lim = Math.max(1.3, ...P.flat().flat().map(Math.abs)) * 1.05;
      const traces = [
        { type: "surface", x: P.map((r) => r.map((q) => q[0])), y: P.map((r) => r.map((q) => q[1])), z: P.map((r) => r.map((q) => q[2])),
          surfacecolor: P.map((r) => r.map((q) => fn.f(...q))), colorscale: seqScale(), showscale: true, opacity: 0.85, name: "M",
          colorbar: { title: { text: "f" }, thickness: 10, len: 0.6 }, hovertemplate: "f = %{surfacecolor:.3f}<extra></extra>" },
        { type: "surface", ...tp, colorscale: [[0, c.warn], [1, c.warn]], showscale: false, opacity: 0.45, name: "TₚM", hoverinfo: "skip" },
        ...(nn > 1e-9 ? arrow3d(p, nU, c.reveal, "normal ∇Φ/‖∇Φ‖", 0.8) : []),
        ...(norm(gf) > 1e-9 ? arrow3d(p, gf.map((x) => x / norm(gf)), c.ok, "∇f (normalitzat)", 0.8) : []),
        ...(norm(gTan) > 1e-3 ? arrow3d(p, gTan.map((x) => x / norm(gf)), c.bad, "projecció tangent de ∇f", 0.8) : []),
        marker(p, c.ink, "p"),
      ];
      if (S.level) {
        // Level surface {f = f(p)} as an isosurface on a coarse grid around the manifold.
        const N = 26, ax = linspace(-lim, lim, N), X = [], Y = [], Z = [], V = [];
        for (const x of ax) for (const y of ax) for (const z of ax) { X.push(x); Y.push(y); Z.push(z); V.push(fn.f(x, y, z)); }
        const fp = fn.f(...p);
        traces.push({ type: "isosurface", x: X, y: Y, z: Z, value: V, isomin: fp, isomax: fp, surface: { count: 1 }, caps: { x: { show: false }, y: { show: false }, z: { show: false } },
          colorscale: [[0, c.accent], [1, c.accent]], showscale: false, opacity: 0.25, name: "f = f(p)", hoverinfo: "skip" });
      }
      const rng = [-lim, lim];
      draw(fig.div, traces, layout3d({ uirevision: man.nom }, { xaxis: axis3d("x", { range: rng }), yaxis: axis3d("y", { range: rng }), zaxis: axis3d("z", { range: rng }) }));
      const ang = norm(gf) > 1e-9 && nn > 1e-9 ? Math.acos(clamp(Math.abs(dot(gf, n)) / (norm(gf) * nn), 0, 1)) * 180 / Math.PI : NaN;
      const tn = [0, 1, 2].map((i) => phi.tex([["x", "y", "z"][i]]));
      out.set(
        el("div", { text: `$\\Phi=${phi.node.toTex()}$` }),
        tn.every(Boolean) ? el("div", { text: `$\\nabla\\Phi=\\left(${tn.join(",\\ ")}\\right)$` }) : null,
        el("div", { text: `$p=${vfmt(p)}$, $\\nabla\\Phi(p)=${vfmt(n)}$` }),
        nn < 1e-6 ? verdict("∇Φ(p) = 0: l'equació no defineix una varietat regular aquí (com el vèrtex del con, Exemple 7 del Tema 6).", "bad") : null,
        el("div", { text: `$T_pM=\\{w:\\ \\nabla\\Phi(p)\\cdot w=0\\}$` }),
        el("div", { text: `$\\nabla f(p)=${vfmt(gf)}$, component tangent $\\|\\mathrm{proj}_{T_pM}\\nabla f\\|=${fmt(norm(gTan))}$` }),
        Number.isFinite(ang) ? el("div", { text: `Angle entre $\\nabla f(p)$ i la normal: $${fmt(ang, 1)}^\\circ$` }) : null,
        norm(gTan) < 1e-3 * Math.max(1, norm(gf))
          ? verdict(`∇f(p) ∈ NₚM: p és un punt crític de f sobre M (∇f = λ∇Φ amb λ ≈ ${fmt(dot(gf, n) / (nn * nn || 1))}). La superfície de nivell de f és tangent a M.`, "ok")
          : verdict("∇f(p) té component tangent (fletxa vermella): seguint-la sobre M, f creix. p no és extrem condicionat.", ""));
    };
    const manSel = el("div", { class: "vl-chips" });
    MANIFOLDS.forEach((m, i) => {
      const b = el("button", { type: "button", class: `vl-chip${i === 0 ? " on" : ""}`, title: m.nom }, tex(m.tex));
      b.addEventListener("click", () => {
        manSel.querySelectorAll(".vl-chip").forEach((x) => x.classList.toggle("on", x === b));
        S.m = i; phi = null;
        S.u = (m.U[0] + m.U[1]) / 2 - 0.7; S.v = (m.V[0] + m.V[1]) / 2 - 0.4;
        su.set(S.u, { min: m.U[0], max: m.U[1] }); sv.set(S.v, { min: m.V[0], max: m.V[1] });
        render();
      });
      manSel.append(b);
    });
    side.append(
      el("div", { class: "vl-group" }, el("span", { class: "vl-label", text: "Varietat M" }), manSel),
      ff.node,
      chips("Funcions", [
        { tex: "x+2y+3z", src: "x + 2*y + 3*z" },
        { tex: "z", src: "z" },
        { tex: "xyz", src: "x*y*z" },
        { tex: "x^2-y^2+z", src: "x^2 - y^2 + z" },
      ], (p) => { ff.set(p.src); render(); }, ff.fn?.src),
      su.node, sv.node, opt,
      toggle("Superfície de nivell $f=f(p)$", S.level, (v) => { S.level = v; render(); }).node,
      out.node);
    main.append(fig.node);
    fig.node.classList.add("tall");
    render();
  },
});
