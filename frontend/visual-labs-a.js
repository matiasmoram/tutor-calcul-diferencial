"use strict";

/* Labs for temes 1–3: norms, fixed point, graphs and level sets, limits along paths,
   directional derivative and gradient, differentiability. Uses the helpers in visual.js. */

/* ---------- Tema 1: unit balls of the p-norms ---------- */

lab({
  id: "normes", tema: 1, seccio: "Espais normats", icon: "‖·‖",
  titol: "Boles de les normes p",
  resum: "Com canvia la bola unitat $\\{\\|x\\|_p\\le 1\\}$ amb $p$, i per què totes les normes de $\\mathbb{R}^n$ són equivalents.",
  idea: "Cada norma té la seva bola unitat. Per a $p=1$ és un rombe, per a $p=2$ un cercle, i quan $p\\to\\infty$ s'acosta al quadrat de $\\|\\cdot\\|_\\infty$. L'equivalència de normes (Teorema 33 del Tema 2) diu que sempre hi ha constants amb $c\\,\\|x\\|_\\infty\\le\\|x\\|_p\\le C\\,\\|x\\|_\\infty$: la bola d'una norma queda encaixada entre dues boles escalades de l'altra.",
  refs: ["T1.3", "T1.4", "T1.11", "T2.32", "T2.33"],
  mount({ side, main }) {
    const c = pal();
    const S = { p: 3, px: 0.6, py: 0.45, enc: true };
    const fig = plotBox("Esferes unitat $\\{\\|x\\|=1\\}$ a $\\mathbb{R}^2$");
    const out = readout();
    const pn = (x, y, p) => (p === Infinity ? Math.max(Math.abs(x), Math.abs(y)) : (Math.abs(x) ** p + Math.abs(y) ** p) ** (1 / p));
    const sphere = (p) => {
      const t = linspace(0, 2 * Math.PI, 361);
      return { x: t.map((s) => Math.cos(s) / pn(Math.cos(s), Math.sin(s), p)), y: t.map((s) => Math.sin(s) / pn(Math.cos(s), Math.sin(s), p)) };
    };
    const square = (r) => ({ x: [r, -r, -r, r, r], y: [r, r, -r, -r, r] });
    const render = () => {
      const p = S.p >= 20 ? Infinity : S.p;
      const C = p === Infinity ? 1 : 2 ** (1 / p);
      const traces = [
        { ...sphere(1), mode: "lines", name: "‖·‖₁", line: { color: c.muted, width: 1.4, dash: "dot" } },
        { ...sphere(2), mode: "lines", name: "‖·‖₂", line: { color: c.muted, width: 1.4, dash: "dash" } },
        { ...square(1), mode: "lines", name: "‖·‖∞", line: { color: c.muted, width: 1.4 } },
        { ...sphere(p), mode: "lines", name: p === Infinity ? "‖·‖∞ (p→∞)" : `‖·‖_p, p=${fmt(p, 2)}`, line: { color: c.accent, width: 3 }, fill: "toself", fillcolor: c.accent + "22" },
      ];
      if (S.enc) {
        traces.push({ ...square(1 / C), mode: "lines", name: `‖x‖∞ = 1/${fmt(C, 3)}`, line: { color: c.warn, width: 2 } });
      }
      traces.push(marker([S.px, S.py], c.bad, "x"));
      draw(fig.div, traces, layout2d({ xaxis: axis2d({ range: [-1.6, 1.6], scaleanchor: "y" }), yaxis: axis2d({ range: [-1.35, 1.35] }) }));
      const x = [S.px, S.py];
      out.set(
        el("div", { text: `$x=${vfmt(x, 2)}$` }),
        el("div", { text: `$\\|x\\|_1=${fmt(pn(...x, 1))}$, $\\|x\\|_2=${fmt(pn(...x, 2))}$, $\\|x\\|_\\infty=${fmt(pn(...x, Infinity))}$` }),
        el("div", { text: `$\\|x\\|_p=${fmt(pn(...x, p))}$` }),
        el("p", { class: "small", text: `Equivalència amb $\\|\\cdot\\|_\\infty$: $\\|x\\|_\\infty\\le\\|x\\|_p\\le 2^{1/p}\\|x\\|_\\infty$, aquí $2^{1/p}=${fmt(C)}$. Per això la bola de $\\|\\cdot\\|_p$ conté el quadrat taronja i està continguda al quadrat gris.` }),
        para("Fixa't: les boles són diferents però defineixen els mateixos oberts, i per tant els mateixos límits i les mateixes funcions contínues.", "small muted"));
    };
    side.append(
      slider({ label: "$p$ (a la dreta del tot, $p=\\infty$)", min: 1, max: 20, step: 0.05, value: S.p, format: (v) => (v >= 20 ? "∞" : fmt(v, 2)) }, (v) => { S.p = v; render(); }).node,
      slider({ label: "Punt $x_1$", min: -1.3, max: 1.3, value: S.px }, (v) => { S.px = v; render(); }).node,
      slider({ label: "Punt $x_2$", min: -1.3, max: 1.3, value: S.py }, (v) => { S.py = v; render(); }).node,
      toggle("Mostra l'encaixament entre normes", S.enc, (v) => { S.enc = v; render(); }).node,
      out.node);
    main.append(fig.node);
    render();
  },
});

/* ---------- Tema 2: fixed point of a contraction (cobweb) ---------- */

lab({
  id: "punt-fix", tema: 2, seccio: "Teorema del punt fix", icon: "↺",
  titol: "Punt fix i contraccions",
  resum: "Iteracions $x_{n+1}=g(x_n)$ en diagrama de teranyina: si $g$ és contractiva convergeixen al punt fix, i a velocitat $k^n$.",
  idea: "Si $g$ és contractiva amb constant $k<1$ en un espai complet, té un únic punt fix i les iteracions hi convergeixen des de qualsevol punt inicial (Teorema 31 del Tema 2), amb $|x_n-x^*|\\le k^n|x_0-x^*|$. Prova un exemple on $|g'|>1$ i mira què passa.",
  refs: ["T2.30", "T2.31", "T2.26"],
  mount({ side, main }) {
    const c = pal();
    const presets = [
      { tex: "\\cos x", src: "cos(x)", a: 0, b: 1.6, x0: 0.1 },
      { tex: "\\tfrac{x}{2}+1", src: "x/2 + 1", a: 0, b: 4, x0: 0.2 },
      { tex: "\\sqrt{x+2}", src: "sqrt(x + 2)", a: 0, b: 3, x0: 0.1 },
      { tex: "2.8\\,x(1-x)", src: "2.8*x*(1 - x)", a: 0, b: 1, x0: 0.15 },
      { tex: "3.5\\,x(1-x)", src: "3.5*x*(1 - x)", a: 0, b: 1, x0: 0.15 },
    ];
    const S = { ...presets[0], n: 12 };
    const fx = formulaField({ label: "$g(x)=$", value: S.src, vars: ["x"] }, () => render());
    const sx0 = slider({ label: "Punt inicial $x_0$", min: S.a, max: S.b, value: S.x0 }, (v) => { S.x0 = v; render(); });
    const sn = slider({ label: "Iteracions $n$", min: 1, max: 60, step: 1, value: S.n, format: (v) => String(v) }, (v) => { S.n = v; render(); });
    const figA = plotBox("Diagrama de teranyina: $y=g(x)$ i $y=x$");
    const figB = plotBox("Distància $|x_n-x^*|$ (escala log)");
    const out = readout();
    const render = () => {
      const g = fx.fn; if (!g) return;
      const xs = linspace(S.a, S.b, 300);
      const it = [S.x0];
      for (let i = 0; i < S.n; i++) it.push(g.f(it[i]));
      const web = { x: [it[0]], y: [S.a] };
      for (let i = 0; i < S.n; i++) { web.x.push(it[i], it[i + 1]); web.y.push(it[i + 1], it[i + 1]); }
      // Fixed point: Newton on g(x) - x from the last iterate, then a sweep if that fails.
      let xs_ = newton(([x]) => [g.f(x) - x], [it[it.length - 1]]);
      if (!xs_) for (const s of linspace(S.a, S.b, 30)) { xs_ = newton(([x]) => [g.f(x) - x], [s]); if (xs_) break; }
      const xstar = xs_?.[0];
      const k = Math.max(...xs.map((x) => Math.abs(g.d("x").f(x))).filter(Number.isFinite));
      draw(figA.div, [
        { x: xs, y: xs, mode: "lines", name: "y = x", line: { color: c.muted, width: 1.4, dash: "dash" } },
        { x: xs, y: xs.map((x) => g.f(x)), mode: "lines", name: "y = g(x)", line: { color: c.accent, width: 2.6 } },
        { ...web, mode: "lines", name: "iteracions", line: { color: c.bad, width: 1.4 } },
        { x: it.slice(0, -1), y: it.slice(1), mode: "markers", name: "(xₙ, xₙ₊₁)", marker: { color: c.bad, size: 6 }, showlegend: false },
        ...(xstar != null ? [marker([xstar, xstar], c.ok, "punt fix x*")] : []),
      ], layout2d({ xaxis: axis2d({ range: [S.a, S.b] }), yaxis: axis2d({ scaleanchor: "x" }) }));
      const dist = it.map((x) => Math.abs(x - xstar));
      draw(figB.div, [
        { x: it.map((_, i) => i), y: dist, mode: "lines+markers", name: "|xₙ − x*|", line: { color: c.bad, width: 2 }, marker: { size: 6 } },
        ...(k < 1 ? [{ x: it.map((_, i) => i), y: it.map((_, i) => dist[0] * k ** i), mode: "lines", name: `kⁿ·|x₀ − x*|, k=${fmt(k)}`, line: { color: c.muted, dash: "dash", width: 1.5 } }] : []),
      ], layout2d({ yaxis: axis2d({ type: "log", exponentformat: "power" }), xaxis: axis2d({ title: { text: "n" } }) }));
      const last = it[it.length - 1];
      out.set(
        el("div", { text: `$x_{${S.n}}=${fmt(last, 6)}$` }),
        xstar != null ? el("div", { text: `$x^*\\approx${fmt(xstar, 6)}$, $g'(x^*)=${fmt(g.d("x").f(xstar))}$` }) : null,
        el("div", { text: `$k=\\max_{[${fmt(S.a, 2)},${fmt(S.b, 2)}]}|g'|\\approx${fmt(k)}$` }),
        k < 1
          ? verdict("Contractiva a l'interval (k < 1): convergència garantida des de qualsevol x₀.", "ok")
          : verdict("No és contractiva a tot l'interval (k ≥ 1): el teorema no garanteix res. Pot convergir (si |g'(x*)| < 1 a prop del punt fix), oscil·lar o divergir.", "warn"));
    };
    side.append(
      chips("Exemples", presets, (p) => { Object.assign(S, p); fx.set(p.src); sx0.set(p.x0, { min: p.a, max: p.b }); render(); }),
      fx.node, sx0.node, sn.node, out.node);
    main.append(el("div", { class: "vl-row" }, figA.node, figB.node));
    render();
  },
});

/* ---------- Tema 2: graph and level sets ---------- */

const SURF_PRESETS = [
  { tex: "x^2+y^2", src: "x^2 + y^2", R: 2 },
  { tex: "x^2-y^2", src: "x^2 - y^2", R: 2 },
  { tex: "xy\\,e^{-(x^2+y^2)/2}", src: "x*y*exp(-(x^2 + y^2)/2)", R: 3 },
  { tex: "\\sin x\\cos y", src: "sin(x)*cos(y)", R: 4 },
  { tex: "x^3-3xy^2", src: "x^3 - 3*x*y^2", R: 1.5, title: "Sella de mico" },
  { tex: "\\tfrac{xy(x^2-y^2)}{x^2+y^2}", src: "x*y*(x^2 - y^2)/(x^2 + y^2)", R: 1, title: "Derivades creuades diferents (Exemple 5 del Tema 5)" },
];

lab({
  id: "grafica", tema: 2, seccio: "Conjunts de nivell i gràfica", icon: "▲",
  titol: "Gràfica i corbes de nivell",
  resum: "La superfície $z=f(x,y)$ i els seus conjunts de nivell $C_k(f)$, en 3D i com a mapa topogràfic.",
  idea: "El conjunt de nivell $C_k(f)=\\{x: f(x)=k\\}$ (Definició 4 del Tema 2) és el tall de la gràfica amb el pla horitzontal $z=k$, projectat al pla $xy$. Mou $k$ i compara la corba vermella a les dues vistes.",
  refs: ["T2.3", "T2.4", "T2.5"],
  mount({ side, main }) {
    const c = pal();
    const S = { R: 2, k: 1, plane: true };
    const ff = formulaField({ label: "$f(x,y)=$", value: SURF_PRESETS[0].src }, () => { fit(); render(); });
    const sR = slider({ label: "Finestra $[-R,R]^2$", min: 0.5, max: 6, step: 0.1, value: S.R }, (v) => { S.R = v; fit(); render(); });
    const sk = slider({ label: "Nivell $k$", min: -1, max: 1, value: S.k }, (v) => { S.k = v; render(); });
    const fig3 = plotBox("Gràfica $z=f(x,y)$");
    const fig2 = plotBox("Corbes de nivell");
    const out = readout();
    let g = null;
    const fit = () => {
      if (!ff.fn) return;
      g = clipGrid(grid(ff.fn.f, [-S.R, S.R], [-S.R, S.R], 81));
      const vals = g.z.flat().filter((v) => v != null);
      const lo = Math.min(...vals), hi = Math.max(...vals);
      S.k = clamp(S.k, lo, hi);
      sk.set(S.k, { min: lo, max: hi });
      sk.input.step = (hi - lo) / 400 || 0.01;
    };
    const render = () => {
      if (!g) return;
      const lines = contourLines(g, S.k);
      const lvl = joinLines(lines);
      draw(fig3.div, [
        surface(g, { name: "f" }),
        ...(S.plane ? [flatSurface([-S.R, S.R], [-S.R, S.R], () => S.k, c.warn, { opacity: 0.25 })] : []),
        { type: "scatter3d", mode: "lines", ...joinLines(lines, S.k), name: `f = ${fmt(S.k, 2)}`, line: { color: c.bad, width: 7 } },
        { type: "scatter3d", mode: "lines", ...joinLines(lines, g.range[0]), name: "projecció", line: { color: c.bad, width: 3, dash: "dash" }, showlegend: false },
      ], layout3d({}, { zaxis: axis3d("z", { range: g.range }) }));
      draw(fig2.div, [
        contour2d(g),
        { ...lvl, mode: "lines", name: `C_k, k=${fmt(S.k, 2)}`, line: { color: c.bad, width: 3.5 } },
      ], layout2d({ xaxis: axis2d({ scaleanchor: "y" }), yaxis: axis2d() }));
      out.set(
        el("div", { text: `$C_{${fmt(S.k, 2)}}(f)$: ${lines.length ? `${lines.length} ${lines.length === 1 ? "component" : "components"} a la finestra` : "buit a la finestra"}` }),
        para("Les corbes de nivell són més juntes on la superfície és més costeruda (gradient gran).", "small muted"));
    };
    side.append(
      chips("Exemples", SURF_PRESETS, (p) => { ff.set(p.src); S.R = p.R; sR.set(p.R); fit(); render(); }),
      ff.node, sR.node, sk.node,
      toggle("Pla $z=k$", S.plane, (v) => { S.plane = v; render(); }).node,
      out.node);
    main.append(el("div", { class: "vl-row" }, fig3.node, fig2.node));
    fit(); render();
  },
});

/* ---------- Tema 2: limits along paths ---------- */

lab({
  id: "limits", tema: 2, seccio: "Límit d'una funció en un punt", icon: "→",
  titol: "Límits per camins",
  resum: "Acosta't a l'origen per rectes $y=mx$ o paràboles $y=mx^2$: si dos camins donen límits diferents, el límit no existeix.",
  idea: "Si el límit existeix, tots els camins cap al punt donen el mateix valor (Proposició 10 del Tema 2). Per tant, dos camins amb límits diferents demostren que no existeix. Però que tots els camins provats coincideixin només dona un candidat: cal fitar $|f-L|$ en tota una bola. El gràfic de baix ho fa numèricament.",
  refs: ["T2.6", "T2.10", "T2.11", "T2.13"],
  mount({ side, main }) {
    const c = pal();
    const presets = [
      { tex: "\\tfrac{xy}{x^2+y^2}", src: "x*y/(x^2 + y^2)", cami: "recta" },
      { tex: "\\tfrac{x^2y}{x^4+y^2}", src: "x^2*y/(x^4 + y^2)", cami: "parabola", title: "Totes les rectes donen 0, però les paràboles no" },
      { tex: "\\tfrac{x^2-y^2}{x^2+y^2}", src: "(x^2 - y^2)/(x^2 + y^2)", cami: "recta" },
      { tex: "\\tfrac{x^3}{x^2+y^2}", src: "x^3/(x^2 + y^2)", cami: "recta", title: "El límit existeix i val 0" },
      { tex: "\\tfrac{\\sin(x^2+y^2)}{x^2+y^2}", src: "sin(x^2 + y^2)/(x^2 + y^2)", cami: "recta" },
    ];
    const S = { m: 1, cami: "recta" };
    const FAMILY = [-2, -1, -0.5, 0, 0.5, 1, 2];
    const ff = formulaField({ label: "$f(x,y)=$", value: presets[0].src }, () => render());
    const sm = slider({ label: "Paràmetre $m$ del camí", min: -3, max: 3, value: S.m }, (v) => { S.m = v; render(); });
    const camiSel = el("div", { class: "vl-seg" });
    const camins = { recta: ["$y=mx$", (t, m) => [t, m * t]], parabola: ["$y=mx^2$", (t, m) => [t, m * t * t]] };
    const setCami = (k) => { S.cami = k; camiSel.querySelectorAll("button").forEach((b) => b.classList.toggle("on", b.dataset.k === k)); };
    for (const [k, [label]] of Object.entries(camins)) {
      const b = el("button", { type: "button", "data-k": k, text: label });
      b.addEventListener("click", () => { setCami(k); render(); });
      camiSel.append(b);
    }
    math(camiSel); setCami("recta");
    const fig3 = plotBox("Gràfica a prop de l'origen i el camí");
    const figP = plotBox("$t\\mapsto f(\\gamma_m(t))$ per a diversos $m$");
    const figB = plotBox("$\\sup_{\\|(x,y)\\|=r}|f(x,y)-L|$ quan $r\\to0$");
    const out = readout();
    const limAlong = (f, m) => {
      const [x, y] = camins[S.cami][1](1e-6, m);
      return f(x, y);
    };
    const render = () => {
      const fn = ff.fn; if (!fn) return;
      const f = fn.f, gam = camins[S.cami][1];
      const g = clipGrid(grid(f, [-1, 1], [-1, 1], 80), [-3, 3]);  // even n: the origin is not a grid node
      const ts = linspace(-1, 1, 400).filter((t) => Math.abs(t) > 1e-9);
      const path = ts.map((t) => gam(t, S.m));
      const L = limAlong(f, S.m);
      draw(fig3.div, [
        surface(g, { opacity: 0.85 }),
        { type: "scatter3d", mode: "lines", x: path.map((p) => p[0]), y: path.map((p) => p[1]), z: path.map((p) => f(...p)),
          name: "f sobre el camí", line: { color: c.bad, width: 7 } },
        marker([0, 0, L], c.bad, `límit pel camí ≈ ${fmt(L)}`),
      ], layout3d({}, { zaxis: axis3d("z", { range: [-1.5, 1.5] }), xaxis: axis3d("x", { range: [-1, 1] }), yaxis: axis3d("y", { range: [-1, 1] }) }));
      const tPos = linspace(1e-3, 1, 200);
      const fam = FAMILY.map((m) => ({ m, L: limAlong(f, m) }));
      draw(figP.div, [
        ...fam.map(({ m }) => ({ x: tPos, y: tPos.map((t) => f(...gam(t, m))), mode: "lines", name: `m=${m}`, line: { color: c.muted, width: 1 }, opacity: 0.6, showlegend: false })),
        { x: tPos, y: tPos.map((t) => f(...gam(t, S.m))), mode: "lines", name: `m=${fmt(S.m, 2)}`, line: { color: c.bad, width: 3 } },
        { x: fam.map(() => 0), y: fam.map((p) => p.L), mode: "markers", name: "límits per t→0", marker: { color: c.accent, size: 9, symbol: "diamond" },
          text: fam.map((p) => `m=${p.m}`), hovertemplate: "%{text}: %{y:.4f}<extra></extra>" },
      ], layout2d({ xaxis: axis2d({ title: { text: "t" } }), yaxis: axis2d({ range: [-1.5, 1.5] }) }));
      const rs = linspace(-5, -0.3, 40).map((e) => 10 ** e);
      const angles = linspace(0, 2 * Math.PI, 721);
      const sup = rs.map((r) => Math.max(...angles.map((a) => Math.abs(f(r * Math.cos(a), r * Math.sin(a)) - L)).filter(Number.isFinite)));
      draw(figB.div, [
        { x: rs, y: sup.map((v) => Math.max(v, 1e-16)), mode: "lines+markers", name: `L = ${fmt(L)}`, line: { color: c.accent, width: 2 }, marker: { size: 5 } },
      ], layout2d({ xaxis: axis2d({ type: "log", title: { text: "r" }, exponentformat: "power" }), yaxis: axis2d({ type: "log", exponentformat: "power" }), showlegend: true }));
      const distinct = Math.max(...fam.map((p) => p.L)) - Math.min(...fam.map((p) => p.L));
      const goesToZero = sup[0] < 1e-3;
      out.set(
        el("div", { text: `Límit pel camí ${camins[S.cami][0]} amb $m=${fmt(S.m, 2)}$: $\\approx ${fmt(L, 4)}$` }),
        distinct > 1e-3
          ? verdict("Camins diferents donen límits diferents: el límit a l'origen no existeix (Proposició 10 del Tema 2).", "bad")
          : goesToZero
            ? verdict(`Tots els camins donen ${fmt(L, 4)} i el suprem a la circumferència de radi r tendeix a 0: el límit existeix (numèricament).`, "ok")
            : verdict("Totes aquestes rectes/paràboles coincideixen, però el suprem sobre circumferències no tendeix a 0: hi ha camins dolents que no hem provat.", "warn"),
        para("Els camins només poden refutar l'existència del límit; per demostrar-la cal una fita que no depengui de la direcció.", "small muted"));
    };
    side.append(
      chips("Exemples", presets, (p) => { ff.set(p.src); setCami(p.cami); render(); }),
      ff.node, el("div", { class: "vl-group" }, el("span", { class: "vl-label", text: "Família de camins" }), camiSel), sm.node, out.node);
    main.append(el("div", { class: "vl-row" }, fig3.node, figP.node), figB.node);
    render();
  },
});

/* ---------- Tema 3: directional derivative and gradient ---------- */

lab({
  id: "gradient", tema: 3, seccio: "Derivada direccional", icon: "∇",
  titol: "Derivada direccional i gradient",
  resum: "Talla la superfície en la direcció $u$: el pendent és $D_uf(a)=\\nabla f(a)\\cdot u$, màxim en la direcció del gradient.",
  idea: "Si $f$ és diferenciable, $D_uf(a)=\\nabla f(a)\\cdot u$ (Proposició 9 del Tema 3). Com a funció de l'angle és $\\|\\nabla f(a)\\|\\cos\\theta$: màxima quan $u$ apunta com el gradient i nul·la quan $u$ és tangent a la corba de nivell (Proposició 13 del Tema 3).",
  refs: ["T3.1", "T3.2", "T3.9", "T3.10", "T3.13"],
  mount({ side, main }) {
    const c = pal();
    const S = { a: 0.8, b: 0.5, th: 0.6, R: 2 };
    const ff = formulaField({ label: "$f(x,y)=$", value: "x^2 + 2*y^2 - x*y" }, () => render());
    const sa = slider({ label: "$a_1$", min: -1.8, max: 1.8, value: S.a }, (v) => { S.a = v; render(); });
    const sb = slider({ label: "$a_2$", min: -1.8, max: 1.8, value: S.b }, (v) => { S.b = v; render(); });
    const sth = slider({ label: "Direcció $\\theta$ de $u=(\\cos\\theta,\\sin\\theta)$", min: 0, max: 2 * Math.PI, value: S.th, format: (v) => `${Math.round(v * 180 / Math.PI)}°` }, (v) => { S.th = v; render(); });
    const fig3 = plotBox("Tall de la gràfica en la direcció $u$");
    const fig2 = plotBox("Mapa de nivell: $\\nabla f(a)$ i $u$");
    const figD = plotBox("$D_uf(a)$ en funció de $\\theta$");
    const out = readout();
    const render = () => {
      const fn = ff.fn; if (!fn) return;
      const a = [S.a, S.b], fa = fn.f(...a), gr = fn.grad(...a), u = [Math.cos(S.th), Math.sin(S.th)];
      const Du = dot(gr, u), ng = norm(gr);
      const g = clipGrid(grid(fn.f, [-S.R, S.R], [-S.R, S.R], 61));
      const ts = linspace(-S.R * 1.5, S.R * 1.5, 200).filter((t) => Math.abs(a[0] + t * u[0]) <= S.R && Math.abs(a[1] + t * u[1]) <= S.R);
      const P = 0.6;
      draw(fig3.div, [
        surface(g, { opacity: 0.8 }),
        flatSurface(linspace(a[0] - P, a[0] + P, 2), linspace(a[1] - P, a[1] + P, 2), (x, y) => fa + gr[0] * (x - a[0]) + gr[1] * (y - a[1]), c.warn, { opacity: 0.45, name: "pla tangent" }),
        { type: "scatter3d", mode: "lines", x: ts.map((t) => a[0] + t * u[0]), y: ts.map((t) => a[1] + t * u[1]), z: ts.map((t) => fn.f(a[0] + t * u[0], a[1] + t * u[1])),
          name: "t ↦ f(a + t u)", line: { color: c.accent, width: 7 } },
        { type: "scatter3d", mode: "lines", x: [-1, 1].map((t) => a[0] + t * u[0]), y: [-1, 1].map((t) => a[1] + t * u[1]), z: [-1, 1].map((t) => fa + t * Du),
          name: `recta tangent, pendent ${fmt(Du)}`, line: { color: c.bad, width: 6 } },
        marker([...a, fa], c.bad, "(a, f(a))"),
      ], layout3d({}, { zaxis: axis3d("z", { range: g.range }) }));
      const k = 0.5 / Math.max(ng, 1e-9);
      draw(fig2.div, [
        contour2d(g),
        { ...joinLines(contourLines(g, fa)), mode: "lines", name: "corba de nivell per a", line: { color: c.ink, width: 2, dash: "dot" } },
        marker(a, c.bad, "a"),
        { x: [null], y: [null], mode: "lines", name: "∇f(a) (escalat)", line: { color: c.ok, width: 3 } },
        { x: [null], y: [null], mode: "lines", name: "u", line: { color: c.accent, width: 3 } },
      ], layout2d({
        xaxis: axis2d({ scaleanchor: "y", range: [-S.R, S.R] }), yaxis: axis2d({ range: [-S.R, S.R] }),
        annotations: [arrow2d(a, gr.map((v) => v * k), c.ok, ""), arrow2d(a, u.map((v) => v * 0.5), c.accent, "")],
      }));
      const ths = linspace(0, 2 * Math.PI, 241);
      const phi = Math.atan2(gr[1], gr[0]);
      draw(figD.div, [
        { x: ths.map((t) => t * 180 / Math.PI), y: ths.map((t) => dot(gr, [Math.cos(t), Math.sin(t)])), mode: "lines", name: "‖∇f(a)‖ cos(θ − φ)", line: { color: c.accent, width: 2.5 } },
        marker([S.th * 180 / Math.PI, Du], c.bad, "θ actual"),
        marker([((phi + 2 * Math.PI) % (2 * Math.PI)) * 180 / Math.PI, ng], c.ok, "màxim: direcció del gradient", { marker: { color: c.ok, size: 10, symbol: "triangle-up" } }),
      ], layout2d({ xaxis: axis2d({ title: { text: "θ (graus)" }, dtick: 90 }), showlegend: true }));
      const tq = 1e-3, quot = (fn.f(a[0] + tq * u[0], a[1] + tq * u[1]) - fa) / tq;
      const gt = [fn.tex(["x"]), fn.tex(["y"])];
      out.set(
        gt[0] && gt[1] ? el("div", { text: `$\\nabla f=\\left(${gt[0]},\\ ${gt[1]}\\right)$` }) : null,
        el("div", { text: `$a=${vfmt(a, 2)}$, $f(a)=${fmt(fa)}$` }),
        el("div", { text: `$\\nabla f(a)=${vfmt(gr)}$, $\\|\\nabla f(a)\\|=${fmt(ng)}$` }),
        el("div", { text: `$D_uf(a)=\\nabla f(a)\\cdot u=${fmt(Du)}$` }),
        el("div", { class: "small muted", text: `Per la definició: $\\frac{f(a+tu)-f(a)}{t}\\big|_{t=10^{-3}}=${fmt(quot, 4)}$` }),
        Math.abs(Du) < 0.02 * Math.max(ng, 1e-9) ? verdict("u és tangent a la corba de nivell: la derivada direccional és 0.", "ok") : null);
    };
    side.append(
      chips("Exemples", SURF_PRESETS.slice(0, 4), (p) => { ff.set(p.src); S.R = p.R; render(); }, ff.fn?.src),
      ff.node, sa.node, sb.node, sth.node, out.node);
    main.append(el("div", { class: "vl-row" }, fig3.node, fig2.node), figD.node);
    render();
  },
});

/* ---------- Tema 3: differentiability (tangent plane, zoom, remainder) ---------- */

lab({
  id: "diferenciabilitat", tema: 3, seccio: "Funció diferenciable", icon: "≈",
  titol: "Pla tangent i diferenciabilitat",
  resum: "Fes zoom a un punt: si $f$ és diferenciable, la superfície s'aplana fins confondre's amb el pla tangent. Contraexemples clàssics inclosos.",
  idea: "$f$ és diferenciable a $a$ si $\\frac{f(a+h)-f(a)-\\nabla f(a)\\cdot h}{\\|h\\|}\\to0$ (Definició 8 del Tema 3). Aquí es calcula $E(r)=\\sup_{\\|h\\|=r}\\frac{|f(a+h)-f(a)-\\nabla f(a)\\cdot h|}{r}$: tendeix a 0 només si $f$ és diferenciable. Tenir parcials, o fins i tot totes les direccionals, no n'hi ha prou (Observació 16 del Tema 3, Observació 17 del Tema 3).",
  refs: ["T3.8", "T3.9", "T3.12", "T3.15", "T3.16", "T3.17", "T3.18", "T3.19"],
  mount({ side, main }) {
    const c = pal();
    const presets = [
      { tex: "x^2+y^2,\\ a=(1,2)", src: "x^2 + y^2", a: [1, 2], f0: null, title: "Exemple 12 del Tema 3" },
      { tex: "\\sqrt{|xy|}", src: "sqrt(abs(x*y))", a: [0, 0], f0: 0, title: "Parcials nul·les, no diferenciable" },
      { tex: "\\tfrac{x^2y}{x^2+y^2}", src: "x^2*y/(x^2 + y^2)", a: [0, 0], f0: 0, title: "Totes les direccionals existeixen, no diferenciable" },
      { tex: "|x|+|y|", src: "abs(x) + abs(y)", a: [0, 0], f0: 0, title: "Contínua, sense parcials" },
      { tex: "r^2\\sin\\tfrac1r", src: "(x^2 + y^2)*sin(1/sqrt(x^2 + y^2))", a: [0, 0], f0: 0, title: "Diferenciable amb parcials no contínues" },
    ];
    const S = { p: presets[0], z: 0 };
    const ff = formulaField({ label: "$f(x,y)=$", value: S.p.src }, () => { S.p = { ...S.p, src: ff.fn.src, f0: null }; render(); });
    const sz = slider({ label: "Zoom: radi $\\rho=10^{s}$", min: -4, max: 0, step: 0.05, value: S.z, format: (v) => `10^${fmt(v, 2)}` }, (v) => { S.z = v; render(); });
    const fig3 = plotBox("$f$ i el pla candidat a prop de $a$");
    const figE = plotBox("$E(r)$: error relatiu del pla (escala log)");
    const out = readout();
    const render = () => {
      const fn = ff.fn; if (!fn) return;
      const a = S.p.a, fa = S.p.f0 ?? fn.f(...a);
      const F = (x, y) => (Math.abs(x - a[0]) < 1e-15 && Math.abs(y - a[1]) < 1e-15 ? fa : fn.f(x, y));
      // One-sided difference quotients: the partial exists only if both sides agree.
      const part = (i) => {
        const h = 1e-6, e = i ? [0, h] : [h, 0];
        const fwd = (F(a[0] + e[0], a[1] + e[1]) - fa) / h, bwd = (fa - F(a[0] - e[0], a[1] - e[1])) / h;
        return Math.abs(fwd - bwd) < 1e-3 * Math.max(1, Math.abs(fwd)) ? (fwd + bwd) / 2 : NaN;
      };
      const gr = [part(0), part(1)];
      const hasGrad = gr.every(Number.isFinite);
      const L = (x, y) => fa + gr[0] * (x - a[0]) + gr[1] * (y - a[1]);
      const rho = 10 ** S.z;
      const g = grid(F, [a[0] - rho, a[0] + rho], [a[1] - rho, a[1] + rho], 60);
      draw(fig3.div, [
        surface(g, { opacity: 0.9 }),
        ...(hasGrad ? [flatSurface(linspace(a[0] - rho, a[0] + rho, 2), linspace(a[1] - rho, a[1] + rho, 2), L, c.warn, { opacity: 0.5, name: "pla candidat" })] : []),
        marker([...a, fa], c.bad, "(a, f(a))"),
      ], layout3d({ uirevision: S.p.tex }, { zaxis: axis3d("z", { autorange: true }), xaxis: axis3d("x", { autorange: true }), yaxis: axis3d("y", { autorange: true }) }));
      const rs = linspace(-6, 0, 49).map((e) => 10 ** e);
      const angles = linspace(0, 2 * Math.PI, 721);
      const E = hasGrad ? rs.map((r) => Math.max(...angles.map((t) => {
        const x = a[0] + r * Math.cos(t), y = a[1] + r * Math.sin(t);
        return Math.abs(F(x, y) - L(x, y)) / r;
      }).filter(Number.isFinite))) : [];
      draw(figE.div, hasGrad ? [
        { x: rs, y: E.map((v) => Math.max(v, 1e-16)), mode: "lines+markers", name: "E(r)", line: { color: c.accent, width: 2 }, marker: { size: 5 } },
        { x: [rho, rho], y: [1e-12, 10], mode: "lines", name: "radi del zoom", line: { color: c.muted, dash: "dot", width: 1 } },
      ] : [], layout2d({ xaxis: axis2d({ type: "log", title: { text: "r" }, exponentformat: "power" }), yaxis: axis2d({ type: "log", exponentformat: "power" }),
        annotations: hasGrad ? [] : [{ text: "Sense gradient no hi ha pla candidat", showarrow: false, xref: "paper", yref: "paper", x: 0.5, y: 0.5, font: { color: c.muted } }] }));
      const small = hasGrad && E[2] < 1e-3;
      const dirs = linspace(0, Math.PI, 7).map((t) => {
        const h = 1e-6, u = [Math.cos(t), Math.sin(t)];
        return (F(a[0] + h * u[0], a[1] + h * u[1]) - fa) / h;
      });
      out.set(
        el("div", { text: `$a=${vfmt(a, 2)}$, $f(a)=${fmt(fa)}$` }),
        el("div", { text: `$\\partial_xf(a)=${hasGrad ? fmt(gr[0]) : Number.isFinite(gr[0]) ? fmt(gr[0]) : "\\nexists"}$, $\\partial_yf(a)=${Number.isFinite(gr[1]) ? fmt(gr[1]) : "\\nexists"}$` }),
        hasGrad ? el("div", { class: "small muted", text: `Linealitat de les direccionals: si fos diferenciable, $D_uf(a)=\\nabla f(a)\\cdot u$. Per a $\\theta=60°$: quocient $${fmt(dirs[2], 4)}$ vs $\\nabla f(a)\\cdot u=${fmt(dot(gr, [Math.cos(Math.PI / 3), Math.sin(Math.PI / 3)]), 4)}$.` }) : null,
        !hasGrad
          ? verdict("Alguna derivada parcial no existeix: f no és diferenciable a a.", "bad")
          : small
            ? verdict("E(r) → 0: el pla tangent aproxima f millor que linealment. Diferenciable (numèricament).", "ok")
            : verdict(`E(r) no tendeix a 0 (≈ ${fmt(E[2], 3)} per r = 10⁻⁵): les parcials existeixen però el pla no és tangent. No diferenciable.`, "bad"),
        para("Fes zoom: en un punt diferenciable la superfície i el pla es confonen; en un contraexemple la forma es repeteix a totes les escales.", "small muted"));
    };
    side.append(
      chips("Exemples", presets, (p) => { S.p = p; ff.set(p.src); render(); }),
      ff.node, sz.node, out.node);
    main.append(el("div", { class: "vl-row" }, fig3.node, figE.node));
    render();
  },
});
