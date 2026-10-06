"use strict";

/* Laboratori visual: interactive figures for the course theory (surfaces, level curves,
   gradients, Taylor, critical points, Lagrange multipliers, manifolds, inverse/implicit maps…).
   Plotly.js draws (WebGL 3D + 2D), math.js parses the student's formulas and differentiates
   them symbolically. Both load lazily from cdnjs the first time a lab opens.
   Shares el(), math(), tex(), api(), crumbs(), show(), theoryPopup(), linkCitations() with app.js.
   The labs themselves live in visual-labs*.js and register with lab({...}). */

const VIS_LIBS = [
  "https://cdnjs.cloudflare.com/ajax/libs/mathjs/14.0.1/math.min.js",
  "https://cdnjs.cloudflare.com/ajax/libs/plotly.js/3.1.1/plotly.min.js",
];
const LABS = [];
const TEMES_VIS = {
  1: "Topologia a $\\mathbb{R}^n$",
  2: "Límits i continuïtat",
  3: "Diferenciabilitat",
  4: "Funció inversa i implícita",
  5: "Taylor i extrems locals",
  6: "Varietats i extrems condicionats",
};
let M = null;          // math.js instance with real-valued results (sqrt(-1) = NaN, not a complex)
let visLibs = null;    // Promise of the loaded libraries

function lab(def) { LABS.push(def); }

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = src;
    s.onload = resolve;
    s.onerror = () => reject(new Error(`No s'ha pogut carregar ${src.split("/").pop()} (cal connexió a internet)`));
    document.head.append(s);
  });
}

function loadVisLibs() {
  // math.js installs itself as window.math, which would shadow app.js's math() (KaTeX auto-render):
  // take its instance and put the app's function back.
  const appMath = window.math;
  visLibs ??= Promise.all([loadScript(VIS_LIBS[0]).then(() => {
    const mathjs = window.math;
    window.math = appMath;
    M = mathjs.create(mathjs.all, { predictable: true });
  }), loadScript(VIS_LIBS[1])])
    .catch((err) => { window.math = appMath; visLibs = null; throw err; });
  return visLibs;
}

/* ---------- formulas: parse once, evaluate fast, differentiate symbolically ---------- */

const NUM_H = 1e-4;

class Fn {
  // A real function of `vars` given as text. Partial derivatives are symbolic (math.js) when
  // possible, with a central finite difference as fallback (e.g. functions math.js cannot derive).
  constructor(src, vars = ["x", "y"]) {
    this.src = src.trim();
    this.vars = vars;
    this.node = M.parse(this.src);
    const unknown = new Set();
    this.node.traverse((n, path, parent) => {
      if (!n.isSymbolNode) return;
      if (parent?.isFunctionNode && path === "fn") return;
      if (!vars.includes(n.name) && !(n.name in M)) unknown.add(n.name);
    });
    if (unknown.size) throw new Error(`Variable desconeguda: ${[...unknown].join(", ")} (fes servir ${vars.join(", ")})`);
    this.f = compileNode(this.node, vars);
    this.derivs = new Map([["", { node: this.node, f: this.f }]]);
  }

  // d("x", "y") = ∂²f/∂y∂x as { node (null if numeric), f }.
  d(...seq) {
    const key = seq.join(",");
    if (this.derivs.has(key)) return this.derivs.get(key);
    const parent = this.d(...seq.slice(0, -1));
    const v = seq[seq.length - 1];
    let out = null;
    if (parent.node) {
      try {
        const node = M.derivative(parent.node, v);
        out = { node, f: compileNode(node, this.vars) };
      } catch { /* not derivable symbolically: numeric below */ }
    }
    if (!out) {
      const i = this.vars.indexOf(v), g = parent.f;
      out = {
        node: null,
        f: (...a) => {
          const h = NUM_H * Math.max(1, Math.abs(a[i]));
          const p = a.slice(), q = a.slice();
          p[i] += h; q[i] -= h;
          return (g(...p) - g(...q)) / (2 * h);
        },
      };
    }
    this.derivs.set(key, out);
    return out;
  }

  grad(...a) { return this.vars.map((v) => this.d(v).f(...a)); }
  hess(...a) { return this.vars.map((u) => this.vars.map((v) => this.d(u, v).f(...a))); }
  tex(seq = []) { const n = this.d(...seq).node; return n ? n.toTex({ parenthesis: "auto", implicit: "hide" }) : null; }
}

function compileNode(node, vars) {
  const code = node.compile();
  const scope = {};
  return (...a) => {
    for (let i = 0; i < vars.length; i++) scope[vars[i]] = a[i];
    try {
      const r = code.evaluate(scope);
      return typeof r === "number" && Number.isFinite(r) ? r : NaN;
    } catch { return NaN; }
  };
}

/* ---------- numerics ---------- */

const linspace = (a, b, n) => Array.from({ length: n }, (_, i) => a + (b - a) * i / (n - 1));
const fmt = (v, d = 3) => !Number.isFinite(v) ? "—" : Math.abs(v) < 10 ** -d / 2 ? "0" : (+v.toFixed(d)).toString();
const vfmt = (a, d = 3) => `(${a.map((v) => fmt(v, d)).join(", ")})`;
const norm = (a) => Math.hypot(...a);
const dot = (a, b) => a.reduce((s, v, i) => s + v * b[i], 0);
const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));

function grid(f, [x0, x1], [y0, y1], n = 71, m = n) {
  // Plotly convention: z[j][i] = f(xs[i], ys[j]).
  const xs = linspace(x0, x1, n), ys = linspace(y0, y1, m);
  const z = ys.map((y) => xs.map((x) => f(x, y)));
  return { xs, ys, z };
}

function robustRange(z, q = 0.02) {
  const v = z.flat().filter(Number.isFinite).sort((a, b) => a - b);
  if (!v.length) return [-1, 1];
  const lo = v[Math.floor(q * (v.length - 1))], hi = v[Math.ceil((1 - q) * (v.length - 1))];
  const pad = (hi - lo) * 0.35 || 1;
  return [lo - pad, hi + pad];
}

function clipGrid(g, range = robustRange(g.z)) {
  // Blow-ups (1/r near a pole) would flatten the whole picture: cut them out of the surface.
  const [lo, hi] = range;
  return { ...g, z: g.z.map((row) => row.map((v) => (Number.isFinite(v) && v >= lo && v <= hi ? v : null))), range };
}

function contourLines(g, level) {
  // Marching squares with linear interpolation. Crossing points are keyed by the grid edge they
  // lie on, so neighbouring cells share them exactly and segments chain into polylines.
  const { xs, ys, z } = g;
  const pts = new Map(), adj = new Map();
  const val = (i, j) => { const v = z[j][i]; return v == null || Number.isNaN(v) ? NaN : v - level; };
  const cross = (key, x0, y0, a, x1, y1, b) => {
    if (!pts.has(key)) { const t = a / (a - b); pts.set(key, [x0 + t * (x1 - x0), y0 + t * (y1 - y0)]); }
    return key;
  };
  const link = (p, q) => {
    for (const [u, w] of [[p, q], [q, p]]) { if (!adj.has(u)) adj.set(u, []); adj.get(u).push(w); }
  };
  for (let j = 0; j < ys.length - 1; j++) {
    for (let i = 0; i < xs.length - 1; i++) {
      const a = val(i, j), b = val(i + 1, j), c = val(i + 1, j + 1), d = val(i, j + 1);
      if ([a, b, c, d].some(Number.isNaN)) continue;
      const e = [];
      if ((a > 0) !== (b > 0)) e.push(cross(`h${i},${j}`, xs[i], ys[j], a, xs[i + 1], ys[j], b));
      if ((b > 0) !== (c > 0)) e.push(cross(`v${i + 1},${j}`, xs[i + 1], ys[j], b, xs[i + 1], ys[j + 1], c));
      if ((d > 0) !== (c > 0)) e.push(cross(`h${i},${j + 1}`, xs[i], ys[j + 1], d, xs[i + 1], ys[j + 1], c));
      if ((a > 0) !== (d > 0)) e.push(cross(`v${i},${j}`, xs[i], ys[j], a, xs[i], ys[j + 1], d));
      if (e.length === 2) link(e[0], e[1]);
      else if (e.length === 4) {
        // Saddle cell: the centre value decides which corners connect.
        if ((a + b + c + d) / 4 > 0 === a > 0) { link(e[0], e[1]); link(e[2], e[3]); }
        else { link(e[0], e[3]); link(e[1], e[2]); }
      }
    }
  }
  const seen = new Set(), lines = [];
  const walk = (start) => {
    const line = [start];
    seen.add(start);
    let cur = start;
    for (;;) {
      const next = (adj.get(cur) || []).find((k) => !seen.has(k));
      if (!next) break;
      seen.add(next); line.push(next); cur = next;
    }
    return line;
  };
  // Open curves first (start at an end), then closed loops.
  for (const k of adj.keys()) if (!seen.has(k) && adj.get(k).length === 1) lines.push(walk(k));
  for (const k of adj.keys()) {
    if (seen.has(k)) continue;
    const line = walk(k);
    if ((adj.get(line[line.length - 1]) || []).includes(k)) line.push(k);  // close the loop
    lines.push(line);
  }
  return lines.map((l) => l.map((k) => pts.get(k))).filter((l) => l.length > 1);
}

function joinLines(lines, z = null) {
  // Several polylines in one Plotly trace, separated by gaps.
  const x = [], y = [], zz = [];
  for (const l of lines) {
    for (const [px, py] of l) { x.push(px); y.push(py); if (z) zz.push(typeof z === "function" ? z(px, py) : z); }
    x.push(null); y.push(null); if (z) zz.push(null);
  }
  return z ? { x, y, z: zz } : { x, y };
}

function newton(F, x0, { iters = 40, tol = 1e-10, h = 1e-7 } = {}) {
  // Newton for F: R^n -> R^n with a finite-difference Jacobian; null if it does not converge.
  let x = x0.slice();
  const n = x.length;
  for (let it = 0; it < iters; it++) {
    const fx = F(x);
    if (fx.some((v) => !Number.isFinite(v))) return null;
    if (norm(fx) < tol) return x;
    const J = Array.from({ length: n }, () => new Array(n));
    for (let j = 0; j < n; j++) {
      const xp = x.slice(); xp[j] += h;
      const fp = F(xp);
      for (let i = 0; i < n; i++) J[i][j] = (fp[i] - fx[i]) / h;
    }
    const dx = solve(J, fx.map((v) => -v));
    if (!dx) return null;
    x = x.map((v, i) => v + dx[i]);
  }
  return norm(F(x)) < 1e-7 ? x : null;
}

function solve(A, b) {
  // Gaussian elimination with partial pivoting.
  const n = b.length, m = A.map((r, i) => [...r, b[i]]);
  for (let c = 0; c < n; c++) {
    let p = c;
    for (let r = c + 1; r < n; r++) if (Math.abs(m[r][c]) > Math.abs(m[p][c])) p = r;
    if (Math.abs(m[p][c]) < 1e-14) return null;
    [m[c], m[p]] = [m[p], m[c]];
    for (let r = 0; r < n; r++) {
      if (r === c) continue;
      const k = m[r][c] / m[c][c];
      for (let k2 = c; k2 <= n; k2++) m[r][k2] -= k * m[c][k2];
    }
  }
  return m.map((r, i) => r[n] / r[i]);
}

function dedupe(points, eps = 1e-4) {
  const out = [];
  for (const p of points) if (!out.some((q) => norm(p.map((v, i) => v - q[i])) < eps)) out.push(p);
  return out;
}

function eig2(H) {
  // Eigenvalues of a symmetric 2×2 matrix (T5.30).
  const [[a, b], [, d]] = H;
  const m = (a + d) / 2, r = Math.hypot((a - d) / 2, b);
  return [m - r, m + r];
}

function arcParam(lines) {
  // Cumulative arc length over several polylines, to move a point along a curve with one slider.
  const segs = [];
  let total = 0;
  lines.forEach((l, li) => {
    for (let k = 0; k < l.length - 1; k++) {
      const len = Math.hypot(l[k + 1][0] - l[k][0], l[k + 1][1] - l[k][1]);
      segs.push({ li, k, a: l[k], b: l[k + 1], s0: total, len });
      total += len;
    }
  });
  const at = (t) => {
    const s = clamp(t, 0, 1) * total;
    const seg = segs.find((g) => s <= g.s0 + g.len) || segs[segs.length - 1];
    if (!seg) return null;
    const u = seg.len ? (s - seg.s0) / seg.len : 0;
    return { p: [seg.a[0] + u * (seg.b[0] - seg.a[0]), seg.a[1] + u * (seg.b[1] - seg.a[1])], seg };
  };
  return { segs, total, at };
}

/* ---------- theme: colors come from the app's CSS tokens, so light and dark both work ---------- */

function css(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
function dark() { return matchMedia("(prefers-color-scheme: dark)").matches; }

function pal() {
  return {
    ink: css("--ink"), muted: css("--muted"), line: css("--line"), panel: css("--panel"),
    accent: css("--accent"), ok: css("--ok"), warn: css("--warn"), bad: css("--bad"), reveal: css("--reveal"),
  };
}

// Magnitude = one hue, light to dark (sequential). Signed quantities = two hues + neutral middle.
function seqScale() {
  return dark()
    ? [[0, "#16212c"], [0.5, "#3f6f9c"], [1, "#cfe4f7"]]
    : [[0, "#e4edf6"], [0.5, "#4f7fae"], [1, "#16304a"]];
}
function divScale() {
  return dark()
    ? [[0, "#f08a82"], [0.5, "#3a3a40"], [1, "#7fb0e0"]]
    : [[0, "#b3261e"], [0.5, "#ecebe6"], [1, "#2f5d8a"]];
}

function axis2d(extra = {}) {
  const c = pal();
  return { gridcolor: c.line, zerolinecolor: c.muted, linecolor: c.line, tickfont: { size: 11 }, ...extra };
}
function axis3d(title, extra = {}) {
  const c = pal();
  return { title: { text: title }, gridcolor: c.line, zerolinecolor: c.muted, showbackground: false, ...extra };
}

function layout2d(extra = {}) {
  const c = pal();
  return {
    paper_bgcolor: "rgba(0,0,0,0)", plot_bgcolor: "rgba(0,0,0,0)",
    font: { color: c.ink, family: "system-ui, -apple-system, Segoe UI, sans-serif", size: 12 },
    margin: { l: 44, r: 14, t: 12, b: 40 },
    xaxis: axis2d(), yaxis: axis2d(),
    showlegend: true, legend: { orientation: "h", y: -0.14, font: { size: 11 } },
    hovermode: "closest", hoverlabel: { bgcolor: c.panel, bordercolor: c.line, font: { color: c.ink } },
    uirevision: "keep",
    ...extra,
  };
}
function layout3d(extra = {}, scene = {}) {
  return layout2d({
    margin: { l: 0, r: 0, t: 0, b: 0 },
    scene: {
      xaxis: axis3d("x"), yaxis: axis3d("y"), zaxis: axis3d("z"),
      aspectmode: "cube", camera: { eye: { x: 1.55, y: -1.55, z: 1.1 } }, ...scene,
    },
    ...extra,
  });
}

const PLOT_CFG = { responsive: true, displaylogo: false, modeBarButtonsToRemove: ["toImage", "sendDataToCloud", "select2d", "lasso2d"] };
function draw(div, traces, lay) { return Plotly.react(div, traces, lay, PLOT_CFG); }

function surface(g, extra = {}) {
  return {
    type: "surface", x: g.xs, y: g.ys, z: g.z, colorscale: seqScale(), showscale: false, opacity: 0.95,
    contours: { z: { show: true, usecolormap: true, project: { z: false }, width: 1 } },
    hovertemplate: "x=%{x:.3f}<br>y=%{y:.3f}<br>z=%{z:.3f}<extra></extra>",
    lighting: { ambient: 0.75, diffuse: 0.6, specular: 0.15, roughness: 0.9 },
    ...extra,
  };
}
function flatSurface(xs, ys, fz, color, extra = {}) {
  // A surface of one color (tangent planes, Taylor polynomials, level planes).
  return {
    type: "surface", x: xs, y: ys, z: ys.map((y) => xs.map((x) => fz(x, y))),
    colorscale: [[0, color], [1, color]], showscale: false, opacity: 0.55, hoverinfo: "skip", ...extra,
  };
}
function contour2d(g, extra = {}) {
  return {
    type: "contour", x: g.xs, y: g.ys, z: g.z, colorscale: seqScale(), showscale: false, ncontours: 18,
    contours: { coloring: "heatmap", showlabels: true, labelfont: { size: 10, color: pal().ink } },
    line: { width: 0.6, color: pal().panel }, opacity: 0.8, name: "f", showlegend: false,
    hovertemplate: "x=%{x:.3f}<br>y=%{y:.3f}<br>f=%{z:.3f}<extra></extra>",
    ...extra,
  };
}
function arrow3d(p, v, color, name, scale = 1) {
  // Shaft + cone head. Returns two traces.
  const q = p.map((c, i) => c + v[i] * scale);
  return [
    { type: "scatter3d", mode: "lines", x: [p[0], q[0]], y: [p[1], q[1]], z: [p[2], q[2]],
      line: { color, width: 7 }, name, hoverinfo: "name" },
    { type: "cone", x: [q[0]], y: [q[1]], z: [q[2]], u: [v[0]], v: [v[1]], w: [v[2]], anchor: "tip",
      sizemode: "absolute", sizeref: 0.18 * norm(v) * scale || 0.1, colorscale: [[0, color], [1, color]],
      showscale: false, hoverinfo: "skip", showlegend: false },
  ];
}
function arrow2d(p, v, color, text = "") {
  // A layout annotation: arrow from p to p + v in data coordinates.
  return {
    x: p[0] + v[0], y: p[1] + v[1], ax: p[0], ay: p[1], xref: "x", yref: "y", axref: "x", ayref: "y",
    showarrow: true, arrowhead: 2, arrowsize: 1.2, arrowwidth: 2.4, arrowcolor: color, text,
    font: { color, size: 13 }, standoff: 0, startstandoff: 0,
  };
}
function marker(p, color, name, extra = {}) {
  const is3 = p.length === 3;
  return {
    type: is3 ? "scatter3d" : "scatter", mode: "markers", x: [p[0]], y: [p[1]], ...(is3 ? { z: [p[2]] } : {}),
    marker: { color, size: is3 ? 6 : 11, line: { color: pal().panel, width: 2 } }, name, ...extra,
  };
}

/* ---------- controls ---------- */

function slider({ label, min, max, step = 0.01, value, unit = "", format = (v) => fmt(v, 2) }, onInput) {
  const out = el("output", { class: "vl-out" });
  const input = el("input", { type: "range", min, max, step, value });
  const sync = () => { out.textContent = format(+input.value) + unit; };
  input.addEventListener("input", () => { sync(); onInput(+input.value); });
  sync();
  const node = el("label", { class: "vl-slider" }, el("span", { class: "vl-label" }, math(el("span", { text: label })), out), input);
  return {
    node, input,
    get value() { return +input.value; },
    set(v, { min: lo, max: hi } = {}) {
      if (lo != null) input.min = lo;
      if (hi != null) input.max = hi;
      input.value = v; sync();
    },
  };
}

function formulaField({ label, value, vars = ["x", "y"] }, onChange) {
  // Text input for a formula, with a live KaTeX preview and parse errors shown in place.
  const input = el("input", { type: "text", value, spellcheck: "false", autocomplete: "off" });
  const prev = el("div", { class: "vl-preview" });
  const err = el("div", { class: "vl-error small" });
  const node = el("label", { class: "vl-formula" }, math(el("span", { class: "vl-label", text: label })), input, prev, err);
  let fn = null;
  const parse = (fire) => {
    try {
      fn = new Fn(input.value, vars);
      prev.replaceChildren(tex(fn.node.toTex({ parenthesis: "auto", implicit: "hide" })));
      err.textContent = "";
      input.classList.remove("bad");
      if (fire) onChange(fn);
    } catch (e) {
      err.textContent = e.message.replace(/^Error: /, "");
      input.classList.add("bad");
    }
  };
  let t = null;
  input.addEventListener("input", () => { clearTimeout(t); t = setTimeout(() => parse(true), 450); });
  input.addEventListener("keydown", (e) => { if (e.key === "Enter") { clearTimeout(t); parse(true); } });
  parse(false);
  return {
    node,
    get fn() { return fn; },
    set(v) { input.value = v; parse(false); },
  };
}

function chips(label, presets, onPick, current) {
  // Example buttons; each label is LaTeX. The one matching `current` (default: the first) starts selected.
  const wrap = el("div", { class: "vl-chips" });
  for (const p of presets) {
    const b = el("button", { type: "button", class: "vl-chip", title: p.title || "" }, tex(p.tex));
    b.addEventListener("click", () => {
      wrap.querySelectorAll(".vl-chip").forEach((c) => c.classList.toggle("on", c === b));
      onPick(p);
    });
    wrap.append(b);
  }
  const i = current === undefined ? 0 : presets.findIndex((p) => (p.src ?? p.f) === current);
  if (i >= 0) wrap.children[i].classList.add("on");
  return el("div", { class: "vl-group" }, el("span", { class: "vl-label", text: label }), wrap);
}

function toggle(label, checked, onChange) {
  const input = el("input", { type: "checkbox" });
  input.checked = checked;
  input.addEventListener("change", () => onChange(input.checked));
  return { node: el("label", { class: "vl-check" }, input, math(el("span", { text: label }))), get value() { return input.checked; } };
}

function readout() {
  // A block of live text with math; set() re-renders it.
  const node = el("div", { class: "vl-readout" });
  return {
    node,
    set(...children) { node.replaceChildren(...children.filter(Boolean)); math(node); linkCitations(node, null); },
  };
}

function para(text, cls = "") { return el("p", { class: cls, text }); }
function verdict(text, kind = "") { return el("div", { class: `vl-verdict ${kind}`, text }); }

function rafThrottle(fn) {
  let pending = false;
  return () => {
    if (pending) return;
    pending = true;
    requestAnimationFrame(() => { pending = false; fn(); });
  };
}

function plotBox(title, cls = "") {
  const div = el("div", { class: "vl-plot" });
  return { node: el("figure", { class: `vl-figure ${cls}` }, title ? math(el("figcaption", { text: title })) : null, div), div };
}

/* ---------- views ---------- */

function purgePlots(root) {
  // Each 3D plot holds a WebGL context and browsers allow only a few: free them on every view change.
  if (!window.Plotly) return;
  root.querySelectorAll(".js-plotly-plot").forEach((d) => Plotly.purge(d));
}

async function viewVisual(id) {
  show("visual");
  const root = $("#view-visual");
  purgePlots(root);
  const def = LABS.find((l) => l.id === id);
  if (!def) return viewVisualGaleria(id);
  crumbs([["Inici", "#/"], ["Laboratori visual", "#/visual"], [def.titol, null]]);
  const loading = el("p", { class: "muted center", text: "Carregant les eines de visualització…" });
  root.replaceChildren(loading);
  await loadVisLibs();
  await getTeoria().then((t) => t.byKey || indexTeoria(t)).catch(() => null);  // citation links in the texts

  const side = el("aside", { class: "vl-side" });
  const main = el("div", { class: "vl-main" });
  const teoria = el("button", { type: "button", class: "btn ghost vl-teoria", text: "Teoria relacionada" });
  teoria.addEventListener("click", async () => {
    const items = await Promise.all(def.refs.map((r) => api(`/api/teoria/${r}`).catch(() => null)));
    theoryPopup(def.titol, items.filter(Boolean));
  });
  const idx = LABS.indexOf(def);
  const nav = el("div", { class: "vl-nav small" },
    idx > 0 ? el("a", { href: `#/visual/${LABS[idx - 1].id}`, text: `← ${LABS[idx - 1].titol}` }) : el("span"),
    idx < LABS.length - 1 ? el("a", { href: `#/visual/${LABS[idx + 1].id}`, text: `${LABS[idx + 1].titol} →` }) : el("span"));
  const head = el("section", { class: "vl-head" },
    el("div", {},
      el("div", { class: "eyebrow", text: `Tema ${def.tema} · ${def.seccio || ""}` }),
      el("h2", { text: def.titol }),
      linkCitations(math(el("p", { class: "muted vl-idea", text: def.idea })), def.tema)),
    teoria);
  root.replaceChildren(head, el("div", { class: "vl-layout" }, side, main), nav);
  math(head);
  try {
    def.mount({ side, main, tema: def.tema });
  } catch (err) {
    main.replaceChildren(verdict(`Error dibuixant: ${err.message}`, "bad"));
    console.error(err);
  }
}

function viewVisualGaleria(focus) {
  crumbs([["Inici", "#/"], ["Laboratori visual", null]]);
  const root = $("#view-visual");
  const temes = [...new Set(LABS.map((l) => l.tema))].sort();
  root.replaceChildren(
    el("section", { class: "hero left" },
      el("div", { class: "eyebrow", text: "Laboratori visual" }),
      el("h2", { text: "Mira la teoria" }),
      math(el("p", { class: "muted", text: "Figures interactives dels resultats del curs: gràfiques i corbes de nivell, límits per camins, gradient i pla tangent, Taylor, hessiana, multiplicadors de Lagrange, varietats, funció inversa i implícita. Escriu la teva pròpia funció o tria un exemple dels apunts; mou els controls i observa." }))),
    ...temes.map((t) => el("section", { class: "vl-tema", id: `vis-tema-${t}` },
      math(el("h3", { class: "section-heading", text: `Tema ${t} · ${TEMES_VIS[t]}` })),
      el("div", { class: "vl-cards" }, ...LABS.filter((l) => l.tema === t).map((l) =>
        el("a", { class: "mode vl-card", href: `#/visual/${l.id}` },
          el("span", { class: "mode-icon", text: l.icon }),
          el("h3", { text: l.titol }),
          math(el("p", { text: l.resum })),
          el("span", { class: "mode-cta", text: "Obre →" })))))));
  math(root);
  const m = /^tema-(\d)$/.exec(focus || "");
  if (m) requestAnimationFrame(() => $(`#vis-tema-${m[1]}`)?.scrollIntoView({ behavior: "smooth" }));
}

// Re-draw with the new palette when the system switches between light and dark.
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
  if (location.hash.startsWith("#/visual/") && window.Plotly) viewVisual(location.hash.split("/")[2]);
});
