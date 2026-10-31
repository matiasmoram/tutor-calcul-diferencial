"use strict";

/* Visualitzador: three working tools for the exercises of the course.
   - Explorador: a function f(x,y) as a surface and a contour map; click a point for f, ∇f, tangent plane and
     Hessian; critical points; constraints and regions with the candidates for absolute extrema.
   - Punt: local analysis at a point (limit along paths, directional derivatives, differentiability).
   - Canvis: a map F: R² → R² deforming a grid, det JF, local invertibility.
   Exercises open them with the functions of their statement (visual-latex.js reads the LaTeX).
   Plotly.js draws, math.js parses and differentiates; both load lazily from cdnjs.
   Shares el(), math(), tex(), api(), crumbs(), show(), theoryPopup(), linkCitations() with app.js.
   The tools live in visual-eines.js and register with eina({...}). */

// Pinned versions with their Subresource Integrity hashes: a changed file on the CDN is refused, not run.
const VIS_LIBS = [
  { src: "https://cdnjs.cloudflare.com/ajax/libs/mathjs/14.0.1/math.min.js",
    integrity: "sha512-PbOEC/cOHBQKshG/XgYoI+kff08IraowCgPlDT8NL91+ZPaeuvWVtC7jYTDua9Kow5QTpX+EMIM0RBKAA2Hsmg==" },
  { src: "https://cdnjs.cloudflare.com/ajax/libs/plotly.js/3.1.1/plotly.min.js",
    integrity: "sha512-QaIUFweb9pyRnQZEYIujSDTHndibSwqsTSb69aedsfAAUpJRUE5yyYfaNAJIbTDuNECyHR/Cc0N7lQJrp0IEpA==" },
];
const EINES = [];
let M = null;          // math.js instance with real-valued results (sqrt(-1) = NaN, not a complex)
let visLibs = null;    // Promise of the loaded libraries

function eina(def) { EINES.push(def); }

function loadScript({ src, integrity }) {
  return new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = src;
    s.integrity = integrity;
    s.crossOrigin = "anonymous";
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
  // possible, with a central finite difference as fallback.
  constructor(src, vars = ["x", "y"]) {
    this.src = String(src).trim();
    this.vars = vars;
    if (!this.src) throw new Error("Escriu una fórmula");
    this.node = M.parse(this.src);
    const unknown = new Set();
    this.node.traverse((n, path, parent) => {
      if (!n.isSymbolNode) return;
      if (parent?.isFunctionNode && path === "fn") return;
      if (!vars.includes(n.name) && !(n.name in M)) unknown.add(n.name);
    });
    if (unknown.size) throw new Error(`Variable desconeguda: ${[...unknown].join(", ")} (fes servir ${vars.join(", ")}; escriu 2*x, no 2x)`);
    this.f = compileNode(this.node, vars);
    this.derivs = new Map([["", { node: this.node, f: this.f }]]);
  }

  d(...seq) {
    // d("x", "y") = ∂²f/∂y∂x as { node (null if numeric), f }.
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

function texOf(src) {
  try { return M.parse(src).toTex({ parenthesis: "auto", implicit: "hide" }); } catch { return src; }
}

/* ---------- numerics ---------- */

const linspace = (a, b, n) => Array.from({ length: n }, (_, i) => a + (b - a) * i / (n - 1));
const fmt = (v, d = 3) => !Number.isFinite(v) ? "—" : Math.abs(v) < 10 ** -d / 2 ? "0" : (+v.toFixed(d)).toString();
const tfmt = (v, d = 3) => (Number.isFinite(v) ? fmt(v, d) : "\\text{—}");  // for LaTeX
const vfmt = (a, d = 3) => `(${a.map((v) => tfmt(v, d)).join(",\\,")})`;
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
  const pad = (hi - lo) * 0.25 || 1;
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
  for (const k of adj.keys()) if (!seen.has(k) && adj.get(k).length === 1) lines.push(walk(k));
  for (const k of adj.keys()) {
    if (seen.has(k)) continue;
    const line = walk(k);
    if ((adj.get(line[line.length - 1]) || []).includes(k)) line.push(k);
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

function dedupe(points, eps = 1e-4, key = (p) => p) {
  const out = [];
  for (const p of points) if (!out.some((q) => norm(key(p).map((v, i) => v - key(q)[i])) < eps)) out.push(p);
  return out;
}

function eig2(H) {
  // Eigenvalues of a symmetric 2×2 matrix.
  const [[a, b], [, d]] = H;
  const m = (a + d) / 2, r = Math.hypot((a - d) / 2, b);
  return [m - r, m + r];
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
    margin: { l: 46, r: 12, t: 8, b: 40 },
    xaxis: axis2d(), yaxis: axis2d(),
    showlegend: true, legend: { orientation: "h", y: -0.12, font: { size: 11 } },
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
      aspectmode: "manual", aspectratio: { x: 1, y: 1, z: 0.75 }, camera: { eye: { x: 1.5, y: -1.5, z: 1.05 } }, ...scene,
    },
    ...extra,
  });
}

const PLOT_CFG = { responsive: true, displaylogo: false, modeBarButtonsToRemove: ["toImage", "sendDataToCloud", "select2d", "lasso2d", "autoScale2d"] };
function draw(div, traces, lay) { return Plotly.react(div, traces, lay, PLOT_CFG); }

function surface(g, extra = {}) {
  return {
    type: "surface", x: g.xs, y: g.ys, z: g.z, colorscale: seqScale(), showscale: false, opacity: 0.95,
    contours: { z: { show: true, usecolormap: true, project: { z: false }, width: 1 } },
    hovertemplate: "x=%{x:.3f}<br>y=%{y:.3f}<br>f=%{z:.4f}<extra></extra>",
    lighting: { ambient: 0.75, diffuse: 0.6, specular: 0.15, roughness: 0.9 },
    name: "f", ...extra,
  };
}
function flatSurface(xs, ys, fz, color, extra = {}) {
  // A one-color surface (tangent planes, Taylor polynomials).
  return {
    type: "surface", x: xs, y: ys, z: ys.map((y) => xs.map((x) => fz(x, y))),
    colorscale: [[0, color], [1, color]], showscale: false, opacity: 0.55, hoverinfo: "skip", ...extra,
  };
}
function contour2d(g, extra = {}) {
  return {
    type: "contour", x: g.xs, y: g.ys, z: g.z, colorscale: seqScale(), showscale: false, ncontours: 20,
    contours: { coloring: "heatmap", showlabels: true, labelfont: { size: 10, color: pal().ink } },
    line: { width: 0.6, color: pal().panel }, opacity: 0.85, name: "f", showlegend: false,
    hovertemplate: "x=%{x:.3f}<br>y=%{y:.3f}<br>f=%{z:.4f}<extra></extra>",
    ...extra,
  };
}
function arrow2d(p, v, color, text = "") {
  return {
    x: p[0] + v[0], y: p[1] + v[1], ax: p[0], ay: p[1], xref: "x", yref: "y", axref: "x", ayref: "y",
    showarrow: true, arrowhead: 2, arrowsize: 1.2, arrowwidth: 2.6, arrowcolor: color, text,
    font: { color, size: 13 }, standoff: 0, startstandoff: 0,
  };
}
function marker(p, color, name, extra = {}) {
  const is3 = p.length === 3;
  return {
    type: is3 ? "scatter3d" : "scatter", mode: "markers", x: [p[0]], y: [p[1]], ...(is3 ? { z: [p[2]] } : {}),
    marker: { color, size: is3 ? 6 : 12, line: { color: pal().panel, width: 2 } }, name, ...extra,
  };
}

/* ---------- controls ---------- */

function field(label, input, extra = null) {
  return el("label", { class: "vt-field" }, math(el("span", { class: "vt-label", text: label })), input, extra);
}

function formulaInput({ label, value = "", vars = ["x", "y"], placeholder = "" }, onChange) {
  // Text input for a formula: KaTeX preview, parse errors in place, onChange(fn) when it parses.
  const input = el("input", { type: "text", value, spellcheck: "false", autocomplete: "off", placeholder });
  const prev = el("div", { class: "vt-preview" });
  const err = el("div", { class: "vt-error" });
  const node = el("label", { class: "vt-field vt-formula" }, math(el("span", { class: "vt-label", text: label })), input, prev, err);
  let fn = null;
  const parse = (fire) => {
    try {
      fn = new Fn(input.value, vars);
      prev.replaceChildren(tex(fn.node.toTex({ parenthesis: "auto", implicit: "hide" })));
      err.textContent = "";
      input.classList.remove("bad");
      if (fire) onChange(fn);
    } catch (e) {
      fn = null;
      err.textContent = e.message.replace(/^Error: /, "");
      input.classList.add("bad");
    }
  };
  let t = null;
  input.addEventListener("input", () => { clearTimeout(t); t = setTimeout(() => parse(true), 500); });
  input.addEventListener("keydown", (e) => { if (e.key === "Enter") { clearTimeout(t); parse(true); } });
  parse(false);
  return { node, input, get fn() { return fn; }, set(v) { input.value = v; parse(false); } };
}

function rangeInput(label, [a, b], onChange) {
  // "−2, 2" style interval.
  const input = el("input", { type: "text", value: `${a}, ${b}`, spellcheck: "false", class: "vt-range" });
  const read = () => {
    const v = input.value.split(/[,;]\s*|\s+/).filter(Boolean).map((s) => { try { return M.evaluate(s); } catch { return NaN; } });
    const ok = v.length === 2 && v.every(Number.isFinite) && v[0] < v[1];
    input.classList.toggle("bad", !ok);
    return ok ? v : null;
  };
  input.addEventListener("change", () => { const v = read(); if (v) onChange(v); });
  input.addEventListener("keydown", (e) => { if (e.key === "Enter") { const v = read(); if (v) onChange(v); } });
  return { node: field(label, input), set([x, y]) { input.value = `${+x.toFixed(4)}, ${+y.toFixed(4)}`; input.classList.remove("bad"); } };
}

function numberInput(label, value, onChange, { placeholder = "" } = {}) {
  const input = el("input", { type: "text", value: value ?? "", spellcheck: "false", class: "vt-num", placeholder });
  const read = () => {
    if (!input.value.trim()) return null;
    try { const v = M.evaluate(input.value); return Number.isFinite(v) ? v : NaN; } catch { return NaN; }
  };
  const fire = () => { const v = read(); input.classList.toggle("bad", Number.isNaN(v)); if (!Number.isNaN(v)) onChange(v); };
  input.addEventListener("change", fire);
  input.addEventListener("keydown", (e) => { if (e.key === "Enter") fire(); });
  return { node: field(label, input), set(v) { input.value = v ?? ""; input.classList.remove("bad"); } };
}

function slider({ label, min, max, step = 0.01, value, format = (v) => fmt(v, 2) }, onInput) {
  const out = el("output", { class: "vt-out" });
  const input = el("input", { type: "range", min, max, step, value });
  const sync = () => { out.textContent = format(+input.value); };
  input.addEventListener("input", () => { sync(); onInput(+input.value); });
  sync();
  const node = el("label", { class: "vt-field vt-slider" }, el("span", { class: "vt-label" }, math(el("span", { text: label })), out), input);
  return { node, input, set(v) { input.value = v; sync(); } };
}

function examples(presets, onPick) {
  // A compact <select> of worked examples (plain-text labels).
  const sel = el("select", { class: "vt-select" }, el("option", { value: "", text: "Exemples…" }),
    ...presets.map((p, i) => el("option", { value: String(i), text: p.label })));
  sel.addEventListener("change", () => { if (sel.value !== "") onPick(presets[+sel.value]); sel.value = ""; });
  return field("Exemple", sel);
}

function toggle(label, checked, onChange) {
  const input = el("input", { type: "checkbox" });
  input.checked = checked;
  input.addEventListener("change", () => onChange(input.checked));
  return { node: el("label", { class: "vt-check" }, input, math(el("span", { text: label }))), input };
}

function segmented(options, value, onChange) {
  // Buttons for a small choice (e.g. rectes / paràboles).
  const wrap = el("div", { class: "vt-seg", role: "group" });
  const set = (v) => wrap.querySelectorAll("button").forEach((b) => b.classList.toggle("on", b.dataset.v === v));
  for (const [v, label] of options) {
    const b = el("button", { type: "button", "data-v": v, text: label });
    b.addEventListener("click", () => { set(v); onChange(v); });
    wrap.append(b);
  }
  math(wrap); set(value);
  return { node: wrap, set };
}

function card(title, ...body) {
  return el("section", { class: "vt-card" }, math(el("h3", { text: title })), ...body);
}

function box() {
  // Live content with math and citation links; set() re-renders it.
  const node = el("div", { class: "vt-box" });
  return { node, set(...children) { node.replaceChildren(...children.filter(Boolean)); math(node); linkCitations(node, null); } };
}

function row(label, value) { return el("div", { class: "vt-kv" }, el("span", { class: "vt-k", text: label }), math(el("span", { class: "vt-v", text: value }))); }
function note(text, cls = "") { return math(el("p", { class: `vt-note ${cls}`, text })); }
function verdict(text, kind = "") { return math(el("div", { class: `vt-verdict ${kind}`, text })); }

function reveal(label, build) {
  // Results that would give an exercise away stay behind a click.
  const wrap = el("div", { class: "vt-reveal" });
  let open = false;
  const btn = el("button", { type: "button", class: "btn ghost vt-reveal-btn", text: label });
  const body = el("div");
  btn.addEventListener("click", () => { open = true; refresh(); });
  const refresh = () => {
    if (!open) { wrap.replaceChildren(btn); return; }
    body.replaceChildren(...[].concat(build()).filter(Boolean));
    math(body); linkCitations(body, null);
    wrap.replaceChildren(body);
  };
  refresh();
  return { node: wrap, refresh, get open() { return open; }, close() { open = false; refresh(); } };
}

function plotBox(title, cls = "") {
  const div = el("div", { class: "vt-plot" });
  return { node: el("figure", { class: `vt-figure ${cls}` }, title ? math(el("figcaption", { text: title })) : null, div), div };
}

/* ---------- views ---------- */

function purgePlots(root) {
  // Each 3D plot holds a WebGL context and browsers allow only a few: free them on every view change.
  if (!window.Plotly) return;
  root.querySelectorAll(".js-plotly-plot").forEach((d) => Plotly.purge(d));
}

function visualParams(part) {
  // "explorador?f=...&a=0,0" -> ["explorador", URLSearchParams]
  const [id, q = ""] = (part || "").split("?");
  return [id, new URLSearchParams(q)];
}

function visualLink(id, params) {
  const q = new URLSearchParams(Object.entries(params).filter(([, v]) => v != null && v !== "").map(([k, v]) => [k, Array.isArray(v) ? v.join(k === "g" ? ";" : ",") : String(v)]));
  return `#/visual/${id}${q.toString() ? `?${q}` : ""}`;
}

async function viewVisual(part) {
  show("visual");
  const root = $("#view-visual");
  purgePlots(root);
  const [id, params] = visualParams(part);
  const def = EINES.find((t) => t.id === id);
  if (!def) return viewVisualInici();
  crumbs([["Inici", "#/"], ["Visualitzador", "#/visual"], [def.titol, null]]);
  root.replaceChildren(el("p", { class: "muted center", text: "Carregant les eines de visualització…" }));
  await loadVisLibs();
  await getTeoria().then((t) => t.byKey || indexTeoria(t)).catch(() => null);

  const teoria = el("button", { type: "button", class: "btn ghost vt-teoria", text: "Teoria" });
  teoria.addEventListener("click", async () => {
    const items = await Promise.all(def.refs.map((r) => api(`/api/teoria/${r}`).catch(() => null)));
    theoryPopup(def.titol, items.filter(Boolean));
  });
  const ex = params.get("ex");
  const tabs = el("nav", { class: "vt-tabs" }, ...EINES.map((t) =>
    el("a", { href: `#/visual/${t.id}`, class: t.id === id ? "on" : "", text: t.titol })));
  const head = el("header", { class: "vt-head" },
    el("div", {},
      tabs,
      math(el("p", { class: "vt-sub", text: def.resum })),
      ex ? el("p", { class: "vt-from" }, el("span", { text: "Funcions llegides de l'enunciat de l'exercici " }), el("strong", { text: ex }),
        el("span", { text: ". Comprova que són correctes." })) : null),
    teoria);
  const body = el("div", { class: "vt-body" });
  root.replaceChildren(head, body);
  try {
    def.mount(body, params);
  } catch (err) {
    body.replaceChildren(verdict(`Error dibuixant: ${err.message}`, "bad"));
    console.error(err);
  }
}

function viewVisualInici() {
  crumbs([["Inici", "#/"], ["Visualitzador", null]]);
  const root = $("#view-visual");
  root.replaceChildren(
    el("section", { class: "hero left" },
      el("div", { class: "eyebrow", text: "Visualitzador" }),
      el("h2", { text: "Mira la funció abans de calcular" }),
      math(el("p", { class: "muted", text: "Tres eines per als exercicis. Escriu la funció o obre-la des d'un exercici amb el botó «Visualitza» de l'enunciat: les fórmules es llegeixen soles." }))),
    el("div", { class: "vt-home" }, ...EINES.map((t) =>
      el("a", { class: "mode vt-home-card", href: `#/visual/${t.id}` },
        el("span", { class: "mode-icon", text: t.icon }),
        el("h3", { text: t.titol }),
        math(el("p", { text: t.resum })),
        el("ul", { class: "vt-uses" }, ...t.usos.map((u) => math(el("li", { text: u })))),
        el("span", { class: "mode-cta", text: "Obre →" })))));
  math(root);
}

function visualitzaExercici(ex) {
  // "Visualitza" button for an exercise statement, or null if no function can be read from it.
  if (typeof extractVisual !== "function") return null;
  const r = extractVisual(`${ex.preambul || ""}\n${ex.enunciat || ""}`);
  let href = null;
  if (r.map) href = visualLink("canvis", { F1: r.map[0], F2: r.map[1], ex: ex.id });
  else if (r.f && r.a && !r.constraints.length) href = visualLink("punt", { f: r.f, a: r.a, fa: r.fa, ex: ex.id });
  else if (r.f) href = visualLink("explorador", { f: r.f, g: r.constraints, ex: ex.id });
  if (!href) return null;
  return el("a", { class: "hint-btn vt-open", href, target: "_blank", rel: "noopener", title: "Obre la funció de l'enunciat al visualitzador (pestanya nova)", text: "📈 Visualitza" });
}

// Re-draw with the new palette when the system switches between light and dark.
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
  if (location.hash.startsWith("#/visual/") && window.Plotly) viewVisual(location.hash.replace(/^#\/visual\//, ""));
});
