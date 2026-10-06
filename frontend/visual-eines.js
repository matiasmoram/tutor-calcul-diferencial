"use strict";

/* The three tools of the Visualitzador. Helpers in visual.js. */

/* ---------- shared analysis ---------- */

const KIND = {
  min: { label: "mínim local", color: () => pal().ok, symbol: "circle" },
  max: { label: "màxim local", color: () => pal().bad, symbol: "diamond" },
  sella: { label: "punt de sella", color: () => pal().warn, symbol: "x" },
  deg: { label: "degenerat: la hessiana no decideix", color: () => pal().muted, symbol: "square" },
};

function classify(H) {
  const d1 = H[0][0], d2 = H[0][0] * H[1][1] - H[0][1] * H[1][0];
  const scale = Math.max(1, ...H.flat().map(Math.abs)) ** 2;
  if (Math.abs(d2) < 1e-7 * scale) return "deg";
  if (d2 < 0) return "sella";
  return d1 > 0 ? "min" : "max";
}

function criticalPoints(fn, X, Y, seeds = 16) {
  // Newton on ∇f = 0 from a grid of seeds.
  const found = [];
  const inside = (p) => p[0] >= X[0] - 1e-9 && p[0] <= X[1] + 1e-9 && p[1] >= Y[0] - 1e-9 && p[1] <= Y[1] + 1e-9;
  for (const x0 of linspace(...X, seeds)) for (const y0 of linspace(...Y, seeds)) {
    const p = newton(([x, y]) => fn.grad(x, y), [x0, y0], { iters: 50, tol: 1e-12 });
    if (p && inside(p)) found.push(p.map((v) => (Math.abs(v) < 1e-9 ? 0 : v)));
  }
  return dedupe(found, 1e-3 * Math.max(X[1] - X[0], Y[1] - Y[0])).slice(0, 60)
    .map((p) => { const H = fn.hess(...p); return { p, H, v: fn.f(...p), kind: classify(H) }; });
}

function parseConstraint(line) {
  // "x^2 + y^2 <= 1" -> { op, strict, g } with g = lhs - rhs; inside: h = ±g <= 0 (< 0 if strict), or g = 0.
  const m = /^(.*?)(<=|>=|=|<|>|≤|≥)(.*)$/.exec(line.trim());
  if (!m) throw new Error(`«${line.trim()}»: falta =, <=, <, >= o >`);
  const strict = m[2] === "<" || m[2] === ">";
  const op = { "<": "<=", ">": ">=", "≤": "<=", "≥": ">=" }[m[2]] || m[2];
  const g = new Fn(`(${m[1]}) - (${m[3]})`);
  const sign = op === ">=" ? -1 : 1;
  const rel = op === "=" ? "=" : op === "<=" ? (strict ? "<" : "\\le") : (strict ? ">" : "\\ge");
  return { src: line.trim(), op, strict, g, h: (x, y) => sign * g.f(x, y), tex: `${texOf(m[1])} ${rel} ${texOf(m[3])}` };
}

function regionCandidates(F, cons, X, Y) {
  // Candidates for absolute extrema of f on {constraints}: interior critical points, Lagrange points on each
  // boundary curve, intersections of two boundaries ("cantonades") and singular points of a constraint.
  const eqs = cons.filter((c) => c.op === "="), span = Math.max(X[1] - X[0], Y[1] - Y[0]);
  const feasible = (p, tol = 1e-7) => cons.every((c) => (c.op === "=" ? Math.abs(c.g.f(...p)) < 1e-6 : c.h(...p) <= tol));
  const inWin = (p) => p[0] >= X[0] && p[0] <= X[1] && p[1] >= Y[0] && p[1] <= Y[1];
  const out = [];
  if (!eqs.length) {
    for (const q of criticalPoints(F, X, Y)) if (cons.every((c) => c.h(...q.p) < -1e-9)) out.push({ p: q.p, tipus: "interior (∇f = 0)" });
  }
  for (const c of cons) {
    const lines = contourLines(grid(c.g.f, X, Y, 181), 0);
    const cross = (x, y) => { const a = F.grad(x, y), b = c.g.grad(x, y); return a[0] * b[1] - a[1] * b[0]; };
    const seeds = [];
    for (const l of lines) for (let k = 0; k < l.length - 1; k++) if (cross(...l[k]) * cross(...l[k + 1]) <= 0) seeds.push(l[k]);
    for (const s of seeds) {
      const gs = c.g.grad(...s), fs = F.grad(...s);
      const r = newton(([x, y, l]) => { const a = F.grad(x, y), b = c.g.grad(x, y); return [a[0] - l * b[0], a[1] - l * b[1], c.g.f(x, y)]; },
        [...s, dot(fs, gs) / (dot(gs, gs) || 1)]);
      if (r && inWin(r) && feasible(r.slice(0, 2))) out.push({ p: r.slice(0, 2), lam: r[2], tipus: `Lagrange a ${c.op === "=" ? "la restricció" : "la vora"} $${c.tex}$` });
    }
    // Singular points of the curve: ∇g = 0 there, Lagrange's condition says nothing.
    for (const l of lines) for (const p of l) if (norm(c.g.grad(...p)) < 0.05) {
      const r = newton(([x, y]) => c.g.grad(x, y), p);
      if (r && Math.abs(c.g.f(...r)) < 1e-8 && feasible(r)) out.push({ p: r, tipus: `punt singular de $${c.tex}$ (∇g = 0)` });
    }
  }
  for (let i = 0; i < cons.length; i++) for (let j = i + 1; j < cons.length; j++) {
    const a = cons[i], b = cons[j];
    for (const x0 of linspace(...X, 14)) for (const y0 of linspace(...Y, 14)) {
      const r = newton(([x, y]) => [a.g.f(x, y), b.g.f(x, y)], [x0, y0]);
      if (r && inWin(r) && feasible(r)) out.push({ p: r, tipus: "cantonada (dues restriccions actives)" });
    }
  }
  const cands = dedupe(out, 1e-4 * span, (q) => q.p).map((q) => ({ ...q, v: F.f(...q.p) })).filter((q) => Number.isFinite(q.v));
  // Bounded? A feasible point on the edge of the window means the region (probably) continues outside it.
  const g = grid((x, y) => (feasible([x, y], 1e-9) ? 1 : 0), X, Y, 61);
  const edge = g.z[0].some(Boolean) || g.z[g.z.length - 1].some(Boolean) || g.z.some((r) => r[0] || r[r.length - 1]);
  // Points on a strict boundary (x² + y² < 1) are not in the region: they can only be a supremum/infimum
  // that is not attained.
  for (const q of cands) q.open = cons.some((k) => k.strict && Math.abs(k.g.f(...q.p)) < 1e-6);
  const tie = (v, w) => Math.abs(v - w) < 1e-7 * (1 + Math.abs(w));
  const all = cands.map((q) => q.v), inn = cands.filter((q) => !q.open).map((q) => q.v);
  const sup = Math.max(...all), inf = Math.min(...all);
  for (const q of cands) {
    q.ext = tie(q.v, sup) ? (q.open ? "sup" : "max") : tie(q.v, inf) ? (q.open ? "inf" : "min") : "";
  }
  const closed = !cons.some((k) => k.strict);
  return { cands, bounded: !edge, closed, feasible, maxAttained: inn.some((v) => tie(v, sup)), minAttained: inn.some((v) => tie(v, inf)) };
}

function feasibleMask(cons, X, Y) {
  return grid((x, y) => (cons.every((c) => (c.op === "=" ? true : c.h(x, y) <= 0)) ? 0 : 1), X, Y, 121);
}

function autoWindow(fn, cons) {
  // Window that shows the region (if it is bounded) or [-3,3]² by default.
  const W = [-3, 3];
  if (!cons.length) return [W, W];
  for (const R of [3, 6, 12]) {
    const X = [-R, R];
    const pts = [];
    const g = grid((x, y) => (cons.every((c) => (c.op === "=" ? Math.abs(c.g.f(x, y)) < R / 40 * (1 + norm(c.g.grad(x, y))) : c.h(x, y) <= 0)) ? 1 : 0), X, X, 121);
    g.z.forEach((r, j) => r.forEach((v, i) => { if (v) pts.push([g.xs[i], g.ys[j]]); }));
    if (!pts.length) continue;
    const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
    const box = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
    if (box[0] > -R && box[1] < R && box[2] > -R && box[3] < R) {
      const pad = 0.25 * Math.max(box[1] - box[0], box[3] - box[2], 0.5);
      const r = (v) => Math.round(v * 100) / 100;
      return [[r(box[0] - pad), r(box[1] + pad)], [r(box[2] - pad), r(box[3] + pad)]];
    }
  }
  return [W, W];
}

/* ---------- Explorador f(x,y) ---------- */

const EXPL_EXAMPLES = [
  { label: "x⁴ + y⁴ − 2y² + 4xy − 2x²  (punts crítics)", f: "x^4 + y^4 - 2*y^2 + 4*x*y - 2*x^2", g: [] },
  { label: "sin x + sin y + cos(x+y)  (punts crítics)", f: "sin(x) + sin(y) + cos(x + y)", g: [], X: [-4, 4], Y: [-4, 4] },
  { label: "(y − 3x²)(y − x²)  (la hessiana no decideix)", f: "(y - 3*x^2)*(y - x^2)", g: [], X: [-1, 1], Y: [-0.5, 1.5] },
  { label: "x − x² − y² al disc x² + y² ≤ 1", f: "x - x^2 - y^2", g: ["x^2 + y^2 <= 1"] },
  { label: "x² + y² − xy + x + y al triangle", f: "x^2 + y^2 - x*y + x + y", g: ["x <= 0", "y <= 0", "x + y >= -3"] },
  { label: "x sobre l'el·lipse x² + 2y² = 3", f: "x", g: ["x^2 + 2*y^2 = 3"] },
  { label: "x³ − 3xy² al disc  (sella de mico)", f: "x^3 - 3*x*y^2", g: ["x^2 + y^2 <= 1"] },
];

eina({
  id: "explorador", icon: "∇", titol: "Explorador f(x,y)",
  resum: "Gràfica i corbes de nivell de $f$. Clica un punt: $f$, $\\nabla f$, pla tangent i hessiana. Afegeix restriccions per trobar extrems absoluts.",
  usos: ["Corbes de nivell i domini (Tema 2)", "Gradient i pla tangent (Tema 3)", "Punts crítics i hessiana (Tema 5)", "Extrems absoluts en un compacte i Lagrange (Tema 6)"],
  refs: ["T2.4", "T3.9", "T3.13", "T5.22", "T5.33", "T2.23", "T6.13", "T6.17"],
  mount(root, params) {
    const c = pal();
    const S = { a: null, tangent: true, quad: false, field: false, cons: [], consErr: "" };
    const fIn = formulaInput({ label: "$f(x,y) =$", value: params.get("f") || EXPL_EXAMPLES[0].f, placeholder: "x^2 + y^2" }, () => { S.a = null; update(true); });
    const gText = el("textarea", { rows: 3, spellcheck: "false", placeholder: "Opcional, una per línia:\nx^2 + y^2 <= 1\nx + y = 1" });
    gText.value = (params.get("g") || "").split(";").filter(Boolean).join("\n");
    gText.addEventListener("change", () => update(true));
    const gErr = el("div", { class: "vt-error" });
    const readCons = () => {
      try { S.cons = gText.value.split("\n").filter((l) => l.trim()).map(parseConstraint); S.consErr = ""; gText.classList.remove("bad"); }
      catch (e) { S.consErr = e.message; gText.classList.add("bad"); }
      gErr.textContent = S.consErr;
    };
    readCons();
    [S.X, S.Y] = fIn.fn ? autoWindow(fIn.fn, S.cons) : [[-3, 3], [-3, 3]];
    const xIn = rangeInput("$x \\in$", S.X, (v) => { S.X = v; update(true); });
    const yIn = rangeInput("$y \\in$", S.Y, (v) => { S.Y = v; update(true); });
    const ex = examples(EXPL_EXAMPLES, (p) => {
      fIn.set(p.f); gText.value = p.g.join("\n"); readCons();
      [S.X, S.Y] = p.X ? [p.X, p.Y] : autoWindow(fIn.fn, S.cons);
      xIn.set(S.X); yIn.set(S.Y); S.a = null; update(true);
    });
    const tg = toggle("Pla tangent", S.tangent, (v) => { S.tangent = v; update(); });
    const tq = toggle("Taylor d'ordre 2", S.quad, (v) => { S.quad = v; update(); });
    const tf = toggle("Camp de gradients", S.field, (v) => { S.field = v; update(); });

    const map2 = plotBox("Corbes de nivell · clica per triar un punt");
    const fig3 = plotBox("Gràfica $z=f(x,y)$");
    const point = box();
    let crit = null, region = null;
    const critR = reveal("Troba els punts crítics", () => {
      crit ??= criticalPoints(fIn.fn, S.X, S.Y);
      update();
      if (!crit.length) return note("Cap punt crític a la finestra.");
      return el("div", { class: "vt-list" }, ...crit.map((q) => listItem(q.p, KIND[q.kind].label, KIND[q.kind].color(), `f = ${fmt(q.v)}`)));
    });
    const regR = reveal("Calcula els candidats", () => {
      region ??= regionCandidates(fIn.fn, S.cons, S.X, S.Y);
      update();
      const { cands, bounded, closed } = region;
      const LBL = { max: "MÀXIM absolut", min: "MÍNIM absolut", sup: "SUPREM, no assolit", inf: "ÍNFIM, no assolit" };
      return [
        cands.length ? el("div", { class: "vt-list" }, ...cands.map((q) =>
          listItem(q.p, LBL[q.ext] || "", extColor(q.ext), `f = ${fmt(q.v)}`,
            `${q.tipus}${q.lam != null ? `, $\\lambda=${fmt(q.lam)}$` : ""}${q.open ? " · fora de la regió (vora oberta)" : ""}`)))
          : note("Cap candidat a la finestra."),
        !bounded
          ? verdict("La regió surt de la finestra: pot ser no fitada, i aleshores els extrems absoluts poden no existir. Amplia la finestra per comprovar-ho.", "warn")
          : closed
            ? note("La regió és tancada i fitada (compacta): pel Teorema 23 del Tema 2, $f$ hi assoleix màxim i mínim, i són entre aquests candidats.")
            : verdict("La regió és fitada però no tancada (té vores amb < o >): Weierstrass no s'aplica. Un extrem pot no assolir-se: els valors a la vora oberta en donen el suprem o l'ínfim.", "warn"),
      ];
    });
    const listItem = (p, label, color, val, sub = "") => {
      const b = el("button", { type: "button", class: "vt-item" },
        el("span", { class: "vt-dot", style: `background:${color}` }),
        el("span", { class: "vt-item-main" }, math(el("span", { text: `$${vfmt(p)}$` })), label ? el("strong", { text: label }) : null,
          sub ? math(el("span", { class: "vt-item-sub", text: sub })) : null),
        el("span", { class: "vt-item-val", text: val }));
      b.addEventListener("click", () => { S.a = p.slice(); update(); });
      return b;
    };
    const regCard = card("Extrems absoluts a la regió", regR.node);

    root.append(
      el("div", { class: "vt-bar" },
        el("div", { class: "vt-bar-main" }, fIn.node, el("div", { class: "vt-field vt-cons" }, math(el("span", { class: "vt-label", text: "Restriccions" })), gText, gErr)),
        el("div", { class: "vt-bar-side" }, xIn.node, yIn.node, ex),
        el("div", { class: "vt-bar-toggles" }, tg.node, tq.node, tf.node)),
      el("div", { class: "vt-plots" }, map2.node, fig3.node),
      el("div", { class: "vt-cards" }, card("Punt triat", point.node), card("Punts crítics", critR.node), regCard));

    let bound = false;
    const update = (recompute = false) => {
      readCons();
      const fn = fIn.fn; if (!fn) return;
      if (recompute) { crit = null; region = null; critR.close(); regR.close(); }
      regCard.classList.toggle("hidden", !S.cons.length);
      const g = clipGrid(grid(fn.f, S.X, S.Y, 101));
      const mask = S.cons.some((k) => k.op !== "=") ? feasibleMask(S.cons, S.X, S.Y) : null;
      const curves = S.cons.map((k) => ({ k, lines: contourLines(grid(k.g.f, S.X, S.Y, 181), 0) }));
      const t2 = [contour2d(g)], t3 = [];
      if (mask) {
        // Outside the region: a veil. A contour trace (not a heatmap) so it stacks above the map of f and keeps alpha.
        const veil = dark() ? "rgba(20,20,22,0.78)" : "rgba(255,255,255,0.8)";
        t2.push({ type: "contour", x: mask.xs, y: mask.ys, z: mask.z, zmin: 0, zmax: 1, autocontour: false,
          contours: { start: 0.5, end: 0.5, size: 1, coloring: "fill", showlines: false },
          colorscale: [[0, "rgba(0,0,0,0)"], [0.49, "rgba(0,0,0,0)"], [0.51, veil], [1, veil]],
          showscale: false, hoverinfo: "skip", name: "fora de la regió", showlegend: true, line: { width: 0 } });
      }
      for (const { k, lines } of curves) t2.push({ ...joinLines(lines), mode: "lines", name: k.src, line: { color: c.ink, width: k.op === "=" ? 3.5 : 2.5 }, hoverinfo: "name" });
      if (S.field) t2.push(gradField(fn, S.X, S.Y));
      // 3D: on a region, the part of the graph over it is solid and the rest faint.
      if (S.cons.length) {
        const feas = (x, y) => S.cons.every((k) => (k.op === "=" ? true : k.h(x, y) <= 1e-9));
        t3.push(surface(g, { opacity: 0.22, showlegend: false, contours: {}, hoverinfo: "skip" }));
        if (mask) t3.push(surface({ ...g, z: g.z.map((r, j) => r.map((v, i) => (feas(g.xs[i], g.ys[j]) ? v : null))) }, { name: "f a la regió" }));
        curves.forEach(({ lines }, i) => t3.push({ type: "scatter3d", mode: "lines", ...joinLines(lines, (x, y) => (feas(x, y) ? fn.f(x, y) : null)),
          name: "f a la vora", showlegend: i === 0, line: { color: c.ink, width: 6 } }));
      } else t3.push(surface(g));
      const ann = [];
      if (S.a) {
        const a = S.a, fa = fn.f(...a), gr = fn.grad(...a), H = fn.hess(...a);
        const span = Math.max(S.X[1] - S.X[0], S.Y[1] - S.Y[0]);
        const ng = norm(gr);
        if (ng > 1e-9) ann.push(arrow2d(a, gr.map((v) => (v / ng) * span * 0.14), c.ok, "∇f"));
        if (Number.isFinite(fa)) t2.push({ ...joinLines(contourLines(g, fa)), mode: "lines", name: "nivell per a", line: { color: c.accent, width: 2, dash: "dash" }, hoverinfo: "skip" });
        t2.push(marker(a, c.bad, "a"));
        t3.push(marker([...a, fa], c.bad, "(a, f(a))"));
        const P = span * 0.18, xs = linspace(a[0] - P, a[0] + P, 15), ys = linspace(a[1] - P, a[1] + P, 15);
        if (S.tangent && Number.isFinite(fa)) t3.push(flatSurface(xs, ys, (x, y) => fa + gr[0] * (x - a[0]) + gr[1] * (y - a[1]), c.warn, { name: "pla tangent", showlegend: true, opacity: 0.6 }));
        if (S.quad && Number.isFinite(fa)) t3.push(flatSurface(linspace(a[0] - 2 * P, a[0] + 2 * P, 25), linspace(a[1] - 2 * P, a[1] + 2 * P, 25),
          (x, y) => { const h = [x - a[0], y - a[1]]; return fa + dot(gr, h) + 0.5 * (H[0][0] * h[0] ** 2 + 2 * H[0][1] * h[0] * h[1] + H[1][1] * h[1] ** 2); },
          c.reveal, { name: "Taylor 2", showlegend: true, opacity: 0.5 }));
        point.set(...pointInfo(fn, a));
      } else point.set(note("Clica el mapa de nivell (o la superfície) per triar un punt $a$."), gradFormula(fn));
      if (crit && critR.open) for (const k of Object.keys(KIND)) {
        const q = crit.filter((p) => p.kind === k); if (!q.length) continue;
        t2.push({ x: q.map((p) => p.p[0]), y: q.map((p) => p.p[1]), mode: "markers", name: KIND[k].label, marker: { color: KIND[k].color(), size: 13, symbol: KIND[k].symbol, line: { color: c.panel, width: 2 } } });
        t3.push({ type: "scatter3d", mode: "markers", x: q.map((p) => p.p[0]), y: q.map((p) => p.p[1]), z: q.map((p) => p.v), name: KIND[k].label, showlegend: false, marker: { color: KIND[k].color(), size: 5 } });
      }
      if (region && regR.open) {
        const q = region.cands;
        const col = (p) => extColor(p.ext);
        t2.push({ x: q.map((p) => p.p[0]), y: q.map((p) => p.p[1]), mode: "markers", name: "candidats", marker: { color: q.map(col), size: 14, symbol: "star", line: { color: c.panel, width: 1 } },
          text: q.map((p) => `f = ${fmt(p.v)}${p.ext ? ` (${{ max: "màxim", min: "mínim", sup: "suprem", inf: "ínfim" }[p.ext]})` : ""}`), hovertemplate: "%{text}<extra></extra>" });
        t3.push({ type: "scatter3d", mode: "markers", x: q.map((p) => p.p[0]), y: q.map((p) => p.p[1]), z: q.map((p) => p.v), name: "candidats", showlegend: false, marker: { color: q.map(col), size: 6 } });
      }
      draw(map2.div, t2, layout2d({ xaxis: axis2d({ range: S.X, scaleanchor: "y", constrain: "domain" }), yaxis: axis2d({ range: S.Y }), annotations: ann, uirevision: `${S.X}${S.Y}` }));
      draw(fig3.div, t3, layout3d({ uirevision: fn.src }, { xaxis: axis3d("x", { range: S.X }), yaxis: axis3d("y", { range: S.Y }), zaxis: axis3d("f", { range: g.range }) }));
      if (!bound) {
        bound = true;
        const pick = (e) => { const p = e.points?.[0]; if (p && Number.isFinite(p.x) && Number.isFinite(p.y)) { S.a = snap([p.x, p.y]); update(); } };
        map2.div.on("plotly_click", pick);
        fig3.div.on("plotly_click", pick);
      }
    };
    const snap = (p) => {
      // A click near a critical point or candidate selects it exactly.
      const span = Math.max(S.X[1] - S.X[0], S.Y[1] - S.Y[0]);
      const near = [...(critR.open && crit ? crit.map((q) => q.p) : []), ...(regR.open && region ? region.cands.map((q) => q.p) : [])]
        .find((q) => norm([q[0] - p[0], q[1] - p[1]]) < 0.025 * span);
      return near ? near.slice() : p;
    };
    update();
  },
});

function extColor(ext) {
  const c = pal();
  return { max: c.bad, sup: c.bad, min: c.ok, inf: c.ok }[ext] || c.warn;
}

function gradField(fn, X, Y) {
  // Normalized gradient arrows on a 15×15 grid (direction only; length would hide small gradients).
  const x = [], y = [], size = [];
  const L = 0.03 * Math.max(X[1] - X[0], Y[1] - Y[0]);
  for (const px of linspace(...X, 15)) for (const py of linspace(...Y, 15)) {
    const g = fn.grad(px, py), n = norm(g);
    if (!(n > 1e-9)) continue;
    x.push(px - (g[0] / n) * L, px + (g[0] / n) * L, null);
    y.push(py - (g[1] / n) * L, py + (g[1] / n) * L, null);
    size.push(0, 8, 0);
  }
  return { x, y, mode: "lines+markers", name: "∇f (direcció)", line: { color: pal().ok, width: 1.4 },
    marker: { symbol: "arrow", angleref: "previous", size, color: pal().ok }, hoverinfo: "skip" };
}

function gradFormula(fn) {
  const gx = fn.tex(["x"]), gy = fn.tex(["y"]);
  return gx && gy ? row("Gradient", `$\\nabla f=\\left(${gx},\\ ${gy}\\right)$`) : null;
}

function pointInfo(fn, a) {
  const fa = fn.f(...a), gr = fn.grad(...a), H = fn.hess(...a), ng = norm(gr);
  const d2 = H[0][0] * H[1][1] - H[0][1] * H[1][0], [l1, l2] = eig2(H);
  const isCrit = ng < 1e-6 * Math.max(1, Math.abs(fa));
  const sgn = (v) => (v < 0 ? "-" : "+");
  return [
    row("Punt", `$a=${vfmt(a)}$`),
    row("Valor", `$f(a)=${tfmt(fa, 4)}$`),
    gradFormula(fn),
    row("Gradient a $a$", `$\\nabla f(a)=${vfmt(gr)}$, $\\ \\|\\nabla f(a)\\|=${tfmt(ng)}$`),
    Number.isFinite(fa) && !isCrit ? row("Pla tangent", `$z=${tfmt(fa)}${sgn(gr[0])}${tfmt(Math.abs(gr[0]))}(x${sgn(-a[0])}${tfmt(Math.abs(a[0]))})${sgn(gr[1])}${tfmt(Math.abs(gr[1]))}(y${sgn(-a[1])}${tfmt(Math.abs(a[1]))})$`) : null,
    row("Hessiana", `$Hf(a)=\\begin{pmatrix}${tfmt(H[0][0])}&${tfmt(H[0][1])}\\\\${tfmt(H[1][0])}&${tfmt(H[1][1])}\\end{pmatrix}$`),
    row("Determinant i valors propis", `$\\det=${tfmt(d2)}$, $\\ \\lambda=${tfmt(l1)},\\ ${tfmt(l2)}$`),
    isCrit
      ? verdict(`$a$ és un punt crític: ${KIND[classify(H)].label}${classify(H) === "deg" ? ". Estudia el signe de f(a+h) − f(a) directament." : "."}`, classify(H) === "deg" ? "warn" : "ok")
      : note("$\\nabla f(a)$ apunta on $f$ creix més ràpid i és perpendicular a la corba de nivell (discontínua)."),
  ];
}

/* ---------- Punt: limit, directional derivatives and differentiability at a point ---------- */

const PUNT_EXAMPLES = [
  { label: "xy / (x² + y²)", f: "x*y/(x^2 + y^2)", a: [0, 0], fa: 0 },
  { label: "x²y / (x⁴ + y²)  (rectes enganyen)", f: "x^2*y/(x^4 + y^2)", a: [0, 0], fa: 0 },
  { label: "x⁵ / (x⁴ + y²)", f: "x^5/(x^4 + y^2)", a: [0, 0], fa: 0 },
  { label: "x|y| / √(x² + y²)", f: "x*abs(y)/sqrt(x^2 + y^2)", a: [0, 0], fa: 0 },
  { label: "√|xy|", f: "sqrt(abs(x*y))", a: [0, 0], fa: 0 },
  { label: "2(x² + y²) sin(1/√(x² + y²))", f: "2*(x^2 + y^2)*sin(1/sqrt(x^2 + y^2))", a: [0, 0], fa: 0 },
];

eina({
  id: "punt", icon: "→", titol: "Anàlisi en un punt",
  resum: "Límit, continuïtat, derivades direccionals i diferenciabilitat de $f$ en un punt $a$, numèricament i en dibuix.",
  usos: ["Límits per camins i en coordenades polars (Tema 2)", "Continuïtat de funcions definides a trossos (Tema 2)", "Derivades direccionals i parcials (Tema 3)", "Diferenciabilitat a l'origen (Tema 3)"],
  refs: ["T2.6", "T2.10", "T2.14", "T3.1", "T3.8", "T3.9", "T3.17", "T3.18"],
  mount(root, params) {
    const c = pal();
    const a0 = (params.get("a") || "0,0").split(",").map(Number);
    const S = { a: a0.length === 2 && a0.every(Number.isFinite) ? a0 : [0, 0], fa: params.has("fa") ? Number(params.get("fa")) : null, k: "1", m: 1, zoom: -0.5 };
    const fIn = formulaInput({ label: "$f(x,y) =$ (fora de $a$)", value: params.get("f") || PUNT_EXAMPLES[0].f }, () => update());
    const aIn = rangeInput("Punt $a =$", S.a, (v) => { S.a = v; update(); });
    const faIn = numberInput("$f(a) =$", S.fa ?? "", (v) => { S.fa = v; update(); }, { placeholder: "si cal definir-la" });
    const ex = examples(PUNT_EXAMPLES, (p) => { fIn.set(p.f); S.a = p.a; S.fa = p.fa; aIn.set(p.a); faIn.set(p.fa); update(); });
    const seg = segmented([["1", "rectes $y-b=m(x-a)$"], ["2", "paràboles $y-b=m(x-a)^2$"]], S.k, (v) => { S.k = v; update(); });
    const sm = slider({ label: "Pendent $m$ del camí", min: -4, max: 4, step: 0.01, value: S.m }, (v) => { S.m = v; update(); });
    const sz = slider({ label: "Zoom (radi)", min: -3, max: 1, step: 0.05, value: S.zoom, format: (v) => fmt(10 ** v, 4) }, (v) => { S.zoom = v; update(); });

    const fig3 = plotBox("Gràfica a prop de $a$ i el camí triat");
    const figL = plotBox("Límit de $f$ sobre cada camí, en funció de $m$");
    const figS = plotBox("$\\sup_{\\|x-a\\|=r}|f(x)-L|$");
    const figD = plotBox("Derivada direccional $D_uf(a)$ segons l'angle de $u$");
    const figE = plotBox("Error del pla tangent $E(r)$");
    const vals = box();
    const conc = reveal("Mostra la conclusió", () => conclusions());
    root.append(
      el("div", { class: "vt-bar" },
        el("div", { class: "vt-bar-main" }, fIn.node),
        el("div", { class: "vt-bar-side" }, aIn.node, faIn.node, ex),
        el("div", { class: "vt-bar-toggles" }, seg.node, sm.node, sz.node)),
      el("div", { class: "vt-plots" }, fig3.node, figL.node),
      el("div", { class: "vt-plots three" }, figS.node, figD.node, figE.node),
      el("div", { class: "vt-cards" }, card("Valors a $a$", vals.node), card("Conclusió", conc.node)));

    let R = null;  // last numbers, for the conclusion
    const update = () => {
      const fn = fIn.fn; if (!fn) return;
      const a = S.a, k = Number(S.k);
      const fa = S.fa ?? fn.f(...a);
      const F = (x, y) => (Math.abs(x - a[0]) < 1e-14 && Math.abs(y - a[1]) < 1e-14 ? fa : fn.f(x, y));
      const gam = (t, m) => [a[0] + t, a[1] + m * t ** k];
      const T = 1e-6;
      const Lpath = (m) => [F(...gam(T, m)), F(...gam(-T, m))];
      // 3D near a.
      const rho = 10 ** S.zoom;
      const g = clipGrid(grid(F, [a[0] - rho, a[0] + rho], [a[1] - rho, a[1] + rho], 80));
      const ts = linspace(-rho, rho, 400).filter((t) => Math.abs(t) > rho * 1e-6 && Math.abs(gam(t, S.m)[1] - a[1]) <= rho);
      const Lm = Lpath(S.m);
      draw(fig3.div, [
        surface(g, { opacity: 0.85 }),
        { type: "scatter3d", mode: "lines", x: ts.map((t) => gam(t, S.m)[0]), y: ts.map((t) => gam(t, S.m)[1]), z: ts.map((t) => F(...gam(t, S.m))), name: "f sobre el camí", line: { color: c.bad, width: 7 } },
        ...(Number.isFinite(fa) ? [marker([...a, fa], c.ink, "(a, f(a))")] : []),
        marker([...a, Lm[0]], c.bad, `límit pel camí ≈ ${fmt(Lm[0])}`, { marker: { color: c.bad, size: 6, symbol: "diamond" } }),
      ], layout3d({ uirevision: `${fn.src}${a}` }, { zaxis: axis3d("f", { range: g.range }) }));
      // L(m), from both sides.
      const ms = linspace(-5, 5, 401);
      const L = ms.map(Lpath);
      draw(figL.div, [
        { x: ms, y: L.map((v) => v[0]), mode: "lines", name: "t → 0⁺", line: { color: c.accent, width: 2.5 } },
        { x: ms, y: L.map((v) => v[1]), mode: "lines", name: "t → 0⁻", line: { color: c.reveal, width: 2, dash: "dash" } },
        marker([S.m, Lm[0]], c.bad, "camí triat"),
        ...(Number.isFinite(fa) ? [{ x: [-5, 5], y: [fa, fa], mode: "lines", name: "f(a)", line: { color: c.muted, width: 1, dash: "dot" } }] : []),
      ], layout2d({ xaxis: axis2d({ title: { text: "m" } }), yaxis: axis2d({ range: valueRange(L.flat(), fa) }) }));
      // Sup over circles with L = f(a) (continuity) or the limit along the x axis.
      const Lref = Number.isFinite(fa) ? fa : L[200][0];
      const rs = linspace(-6, 0, 37).map((e) => 10 ** e), ang = linspace(0, 2 * Math.PI, 721);
      const sup = rs.map((r) => Math.max(...ang.map((t) => Math.abs(F(a[0] + r * Math.cos(t), a[1] + r * Math.sin(t)) - Lref)).filter(Number.isFinite)));
      draw(figS.div, [{ x: rs, y: sup.map((v) => Math.max(v, 1e-16)), mode: "lines+markers", name: `L = ${fmt(Lref)}`, line: { color: c.accent, width: 2 }, marker: { size: 4 } }],
        logLayout("r"));
      // Directional derivatives by the definition, against ∇f(a)·u.
      const part = (i) => {
        const h = 1e-6, e = i ? [0, h] : [h, 0];
        const fw = (F(a[0] + e[0], a[1] + e[1]) - fa) / h, bw = (fa - F(a[0] - e[0], a[1] - e[1])) / h;
        return Math.abs(fw - bw) < 1e-3 * Math.max(1, Math.abs(fw)) ? (fw + bw) / 2 : NaN;
      };
      const gr = [part(0), part(1)], hasGrad = gr.every(Number.isFinite);
      const th = linspace(0, 2 * Math.PI, 361);
      const Du = th.map((t) => (F(a[0] + T * Math.cos(t), a[1] + T * Math.sin(t)) - fa) / T);
      draw(figD.div, [
        { x: th.map((t) => t * 180 / Math.PI), y: Du, mode: "lines", name: "(f(a+tu) − f(a))/t", line: { color: c.accent, width: 2.5 } },
        ...(hasGrad ? [{ x: th.map((t) => t * 180 / Math.PI), y: th.map((t) => gr[0] * Math.cos(t) + gr[1] * Math.sin(t)), mode: "lines", name: "∇f(a)·u", line: { color: c.warn, width: 2, dash: "dash" } }] : []),
      ], layout2d({ xaxis: axis2d({ title: { text: "angle de u (graus)" }, dtick: 90 }) }));
      // Remainder of the tangent plane.
      const E = hasGrad ? rs.map((r) => Math.max(...ang.map((t) => {
        const h = [r * Math.cos(t), r * Math.sin(t)];
        return Math.abs(F(a[0] + h[0], a[1] + h[1]) - fa - dot(gr, h)) / r;
      }).filter(Number.isFinite))) : [];
      draw(figE.div, hasGrad ? [{ x: rs, y: E.map((v) => Math.max(v, 1e-16)), mode: "lines+markers", name: "E(r)", line: { color: c.accent, width: 2 }, marker: { size: 4 } }] : [],
        logLayout("r", hasGrad ? [] : [{ text: "Sense derivades parcials no hi ha pla candidat", showarrow: false, xref: "paper", yref: "paper", x: 0.5, y: 0.5, font: { color: c.muted } }]));
      // The conclusion tries more families than the one on screen: y−b = m(x−a)^k and x−a = m(y−b)^k, k = 1, 2, 3.
      // Sampling circles alone misses paths that hug an axis (y = x² meets the circle of radius r at angle ≈ r).
      const Lvals = [];
      for (const kk of [1, 2, 3]) for (const mm of linspace(-5, 5, 41)) for (const t of [T, -T]) {
        Lvals.push(F(a[0] + t, a[1] + mm * t ** kk), F(a[0] + mm * t ** kk, a[1] + t));
      }
      const Lfin = Lvals.filter(Number.isFinite);
      R = { fa, Lspread: Math.max(...Lfin) - Math.min(...Lfin), supSmall: sup[0] < 1e-3 && sup[0] < sup[12], Lref, hasGrad, gr,
        Esmall: hasGrad && E[0] < 1e-3, linearDu: hasGrad && Du.every((v, i) => Math.abs(v - (gr[0] * Math.cos(th[i]) + gr[1] * Math.sin(th[i]))) < 1e-3 * (1 + Math.abs(v))) };
      vals.set(
        row("Punt", `$a=${vfmt(a)}$`),
        row("Valor", Number.isFinite(fa) ? `$f(a)=${tfmt(fa, 4)}$${S.fa == null ? "" : " (definit a part)"}` : "$f$ no està definida a $a$: escriu-ne el valor a dalt"),
        row("Límit pel camí triat", `$\\approx ${tfmt(Lm[0], 4)}$`),
        row("Parcials", `$\\partial_xf(a)=${Number.isFinite(gr[0]) ? tfmt(gr[0]) : "\\nexists"}$, $\\ \\partial_yf(a)=${Number.isFinite(gr[1]) ? tfmt(gr[1]) : "\\nexists"}$`),
        note("Si la corba del límit sobre els camins no és plana, el límit no existeix. Si la derivada direccional no és una sinusoide $\\nabla f(a)\\cdot u$, $f$ no és diferenciable."));
      conc.refresh();
    };
    const conclusions = () => {
      if (!R) return [];
      const out = [];
      if (R.Lspread > 1e-3) out.push(verdict("El límit no existeix: camins diferents donen valors diferents (Proposició 10 del Tema 2). Per tant f no és contínua a a.", "bad"));
      else if (R.supSmall) out.push(verdict(`El límit existeix (numèricament) i val ${fmt(R.Lref, 4)}: el suprem sobre cercles de radi r tendeix a 0.`, "ok"),
        Number.isFinite(R.fa) && Math.abs(R.fa - R.Lref) < 1e-6 ? verdict("Coincideix amb f(a): f és contínua a a.", "ok") : null);
      else out.push(verdict("Tots els camins provats coincideixen, però el suprem sobre cercles no tendeix a 0: hi ha camins dolents que no són rectes ni paràboles. El límit no existeix.", "warn"));
      if (!R.hasGrad) out.push(verdict("Alguna derivada parcial no existeix: f no és diferenciable a a.", "bad"));
      else if (R.Esmall) out.push(verdict("E(r) → 0: f és diferenciable a a (numèricament), amb Df(a) = ∇f(a).", "ok"));
      else out.push(verdict(`Les parcials existeixen però E(r) no tendeix a 0: f no és diferenciable a a.${R.linearDu ? "" : " A més, les derivades direccionals no són lineals en u."}`, "bad"));
      out.push(note("Conclusions numèriques: indiquen què has de demostrar, no en són la demostració."));
      return out;
    };
    update();
  },
});

function valueRange(vals, extra) {
  // At least ±0.5 around the values: a limit of 0 evaluated at t = 10⁻⁶ leaves 10⁻⁵-sized noise that
  // autoscaling would blow up into fake spikes.
  const v = [...vals, extra].filter(Number.isFinite).sort((p, q) => p - q);
  if (!v.length) return [-1, 1];
  const lo = v[Math.floor(0.02 * (v.length - 1))], hi = v[Math.ceil(0.98 * (v.length - 1))];
  const mid = (lo + hi) / 2, half = Math.max((hi - lo) / 2 * 1.15, 0.5);
  return [mid - half, mid + half];
}

function logLayout(xt, annotations = []) {
  return layout2d({ xaxis: axis2d({ type: "log", title: { text: xt }, exponentformat: "power" }), yaxis: axis2d({ type: "log", exponentformat: "power" }), showlegend: false, annotations });
}

/* ---------- Canvis de variables F: R² → R² ---------- */

const CANVIS_EXAMPLES = [
  { label: "polars (r cos φ, r sin φ)", F1: "x*cos(y)", F2: "x*sin(y)", X: [0, 2], Y: [0, 6.2832] },
  { label: "(x²y, xy²)", F1: "x^2*y", F2: "x*y^2", X: [-1.5, 1.5], Y: [-1.5, 1.5] },
  { label: "(u³ − 3uv², 3u²v − v³)", F1: "x^3 - 3*x*y^2", F2: "3*x^2*y - y^3", X: [-1.2, 1.2], Y: [-1.2, 1.2] },
  { label: "(eˣ cos y, eˣ sin y)", F1: "exp(x)*cos(y)", F2: "exp(x)*sin(y)", X: [-1, 0.8], Y: [-4, 4] },
  { label: "(cosh s cos t, sinh s sin t)", F1: "cosh(x)*cos(y)", F2: "sinh(x)*sin(y)", X: [0, 1.5], Y: [0, 6.2832] },
];

eina({
  id: "canvis", icon: "⇄", titol: "Canvis de variables",
  resum: "Com deforma $F:\\mathbb{R}^2\\to\\mathbb{R}^2$ una quadrícula. On $\\det JF\\neq0$ és localment invertible; on s'anul·la, es plega.",
  usos: ["Teorema de la funció inversa: on hi ha inversa local (Tema 4)", "Injectivitat global i oberts maximals (Tema 4)", "Canvis a polars i altres coordenades (Tema 3 i 4)"],
  refs: ["T4.3", "T4.5", "T4.9", "T4.11"],
  mount(root, params) {
    const c = pal();
    const S = { X: [-1.5, 1.5], Y: [-1.5, 1.5], a: null, sq: 0.15 };
    const f1 = formulaInput({ label: "$F_1(x,y) =$", value: params.get("F1") || CANVIS_EXAMPLES[1].F1 }, () => update());
    const f2 = formulaInput({ label: "$F_2(x,y) =$", value: params.get("F2") || CANVIS_EXAMPLES[1].F2 }, () => update());
    const xIn = rangeInput("$x \\in$", S.X, (v) => { S.X = v; update(); });
    const yIn = rangeInput("$y \\in$", S.Y, (v) => { S.Y = v; update(); });
    const ex = examples(CANVIS_EXAMPLES, (p) => { f1.set(p.F1); f2.set(p.F2); S.X = p.X; S.Y = p.Y; xIn.set(p.X); yIn.set(p.Y); S.a = null; update(); });
    const ss = slider({ label: "Mida del quadradet", min: 0.02, max: 0.6, value: S.sq }, (v) => { S.sq = v; update(); });
    const figD = plotBox("Domini: signe de $\\det JF$ · clica per triar un punt");
    const figI = plotBox("Imatge per $F$");
    const info = box();
    root.append(
      el("div", { class: "vt-bar" },
        el("div", { class: "vt-bar-main two" }, f1.node, f2.node),
        el("div", { class: "vt-bar-side" }, xIn.node, yIn.node, ex),
        el("div", { class: "vt-bar-toggles" }, ss.node)),
      el("div", { class: "vt-plots" }, figD.node, figI.node),
      el("div", { class: "vt-cards" }, card("Jacobiana", info.node)));
    let bound = false;
    const update = () => {
      const A = f1.fn, B = f2.fn; if (!A || !B) return;
      const F = (x, y) => [A.f(x, y), B.f(x, y)];
      const J = (x, y) => [A.grad(x, y), B.grad(x, y)];
      const det = (x, y) => { const m = J(x, y); return m[0][0] * m[1][1] - m[0][1] * m[1][0]; };
      const a = S.a || [(S.X[0] + S.X[1]) / 2 + 0.17 * (S.X[1] - S.X[0]), (S.Y[0] + S.Y[1]) / 2 + 0.11 * (S.Y[1] - S.Y[0])];
      const NL = 16, xs = linspace(...S.X, NL), ys = linspace(...S.Y, NL), fine = 90;
      const tD = [], tI = [];
      for (const [fam, color, name] of [["v", c.accent, "x = constant"], ["h", c.reveal, "y = constant"]]) {
        const D = { x: [], y: [] }, I = { x: [], y: [] };
        for (const k of fam === "v" ? xs : ys) {
          for (const t of linspace(...(fam === "v" ? S.Y : S.X), fine)) {
            const [x, y] = fam === "v" ? [k, t] : [t, k];
            const [u, v] = F(x, y);
            D.x.push(x); D.y.push(y); I.x.push(u); I.y.push(v);
          }
          for (const o of [D, I]) { o.x.push(null); o.y.push(null); }
        }
        tD.push({ ...D, mode: "lines", name, line: { color, width: 1 }, opacity: 0.75, hoverinfo: "skip" });
        tI.push({ ...I, mode: "lines", name: `F(${name})`, line: { color, width: 1 }, opacity: 0.75, hoverinfo: "skip" });
      }
      const gd = grid(det, S.X, S.Y, 101);
      const zero = contourLines(gd, 0);
      const m = Math.max(...gd.z.flat().filter(Number.isFinite).map(Math.abs)) || 1;
      const h = S.sq * Math.min(S.X[1] - S.X[0], S.Y[1] - S.Y[0]) / 2;
      const sq = [[-h, -h], [h, -h], [h, h], [-h, h], [-h, -h]].map(([dx, dy]) => [a[0] + dx, a[1] + dy]);
      const dense = [];
      for (let k = 0; k < 4; k++) for (const t of linspace(0, 1, 24)) dense.push([sq[k][0] + t * (sq[k + 1][0] - sq[k][0]), sq[k][1] + t * (sq[k + 1][1] - sq[k][1])]);
      const Ja = J(...a), Fa = F(...a), da = det(...a);
      const lin = sq.map(([x, y]) => [Fa[0] + Ja[0][0] * (x - a[0]) + Ja[0][1] * (y - a[1]), Fa[1] + Ja[1][0] * (x - a[0]) + Ja[1][1] * (y - a[1])]);
      draw(figD.div, [
        { type: "heatmap", x: gd.xs, y: gd.ys, z: gd.z, colorscale: divScale(), zmin: -m, zmax: m, opacity: 0.6, showscale: true, name: "det JF",
          colorbar: { title: { text: "det JF" }, thickness: 10, len: 0.6 }, hovertemplate: "(%{x:.3f}, %{y:.3f})<br>det JF = %{z:.3f}<extra></extra>" },
        ...tD,
        ...(zero.length ? [{ ...joinLines(zero), mode: "lines", name: "det JF = 0", line: { color: c.bad, width: 3.5 } }] : []),
        { x: sq.map((p) => p[0]), y: sq.map((p) => p[1]), mode: "lines", fill: "toself", name: "quadradet", line: { color: c.ink, width: 2 } },
        marker(a, c.ink, "a"),
      ], layout2d({ xaxis: axis2d({ range: S.X }), yaxis: axis2d({ range: S.Y }), uirevision: `${S.X}${S.Y}` }));
      const imZero = zero.map((l) => l.map((p) => F(...p)));
      draw(figI.div, [
        ...tI,
        ...(imZero.length ? [{ ...joinLines(imZero), mode: "lines", name: "F(det JF = 0)", line: { color: c.bad, width: 3.5 } }] : []),
        { x: dense.map((p) => F(...p)[0]), y: dense.map((p) => F(...p)[1]), mode: "lines", fill: "toself", name: "F(quadradet)", line: { color: c.ink, width: 2 } },
        { x: lin.map((p) => p[0]), y: lin.map((p) => p[1]), mode: "lines", name: "DF(a)(quadradet)", line: { color: c.warn, width: 2, dash: "dash" } },
        marker(Fa, c.ink, "F(a)"),
      ], layout2d({ xaxis: axis2d({ scaleanchor: "y" }), yaxis: axis2d(), uirevision: `${A.src}${B.src}${S.X}${S.Y}` }));
      const t = [[A.tex(["x"]), A.tex(["y"])], [B.tex(["x"]), B.tex(["y"])]];
      info.set(
        t.flat().every(Boolean) ? row("Jacobiana", `$JF=\\begin{pmatrix}${t[0][0]}&${t[0][1]}\\\\${t[1][0]}&${t[1][1]}\\end{pmatrix}$`) : null,
        row("Punt", `$a=${vfmt(a)}$, $\\ F(a)=${vfmt(Fa)}$`),
        row("Determinant", `$\\det JF(a)=${tfmt(da)}$`),
        Math.abs(da) > 1e-8
          ? verdict(`$\\det JF(a)\\neq0$: pel Teorema 5 del Tema 4, $F$ té inversa local diferenciable a prop de $a$, amb $D(F^{-1})(F(a))=JF(a)^{-1}$. L'àrea del quadradet es multiplica per $${tfmt(Math.abs(da), 2)}$${da < 0 ? " i l'orientació s'inverteix" : ""}.`, "ok")
          : verdict("$\\det JF(a)=0$: el teorema de la funció inversa no s'aplica aquí (la quadrícula es plega).", "bad"),
        note("Les línies vermelles són on $\\det JF=0$. Si la imatge de la quadrícula es solapa amb si mateixa, $F$ no és injectiva globalment encara que sigui localment invertible."));
      if (!bound) {
        bound = true;
        figD.div.on("plotly_click", (e) => { const p = e.points?.[0]; if (p && Number.isFinite(p.x) && Number.isFinite(p.y)) { S.a = [p.x, p.y]; update(); } });
      }
    };
    update();
  },
});
