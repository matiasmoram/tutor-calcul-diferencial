"use strict";

/* "Construeix el contraexemple": the student writes f(x,y) off the origin and f(0,0), plus a certificate for each
   property that needs one (paths, a radial bound, a direction). Every verdict comes from sympy on the server; no
   model is called. Shares el(), math(), api(), crumbs(), show() with app.js and visualLink() with visual.js. */

const CE_DIFICULTATS = { facil: "Fàcil", normal: "Normal", dificil: "Difícil" };
const CE_ESTATS = {
  ok: ["ok", "Demostrat"],
  plausible: ["warn", "Plausible"],
  falla: ["bad", "No es compleix"],
  indeterminat: ["neutral", "No demostrat"],
};
const CE_SINTAXI = "Sintaxi: multiplicació explícita (2*x, x*y), potències x**2 o x^2, Abs(x), sqrt, cbrt (arrel cúbica real), sin, cos, exp, log. Variables: x, y; als camins t; a la fita r.";

const CE = { reptes: null, repte: null, entrada: null, resultat: null, enviant: false };

async function getCeReptes() {
  CE.reptes ??= await api("/api/contraexemples");
  return CE.reptes;
}

/* ---------- list ---------- */

async function viewContraexemplesInici() {
  show("contraexemples");
  crumbs([["Inici", "#/"], ["Contraexemples", null]]);
  const reptes = await getCeReptes();
  const temes = [...new Set(reptes.map((r) => r.tema))].sort();
  const stage = (n, title, text, tag, cls) => el("li", {},
    el("span", { class: "step-num", text: String(n) }), el("h4", { text: title }), math(el("p", { text })),
    el("span", { class: `tag ${cls}`, text: tag }));
  $("#view-contraexemples").replaceChildren(
    el("section", { class: "hero left" },
      el("div", { class: "eyebrow", text: "Construeix el contraexemple" }),
      el("h2", { text: "Fabrica la funció que trenca la intuïció" }),
      math(el("p", { class: "muted", text: "Cada repte demana una funció amb unes propietats a l'origen que semblen incompatibles: parcials sense continuïtat, totes les rectes d'acord però sense límit… Escriu-la, dona el certificat que ho demostra i el codi ho comprova amb sympy. Cap model de llenguatge: el veredicte és càlcul." }))),
    el("ol", { class: "pipeline cf-pipeline" },
      stage(1, "Construeix", "Escrius $f(x,y)$ fora de l'origen i el valor $f(0,0)$.", "Tu", "llm"),
      stage(2, "Certifica", "Per a «no existeix» dones camins; per a «és contínua» o «és diferenciable», una fita $G(r)\\to0$.", "Tu", "llm"),
      stage(3, "Comprovació", "Derivades i límits per camins: límits d'una variable, exactes. Fites: $G(r)\\to0$ exacte i la desigualtat mostrejada.", "CAS · sympy", "rule"),
      stage(4, "Veredicte", "Demostrat, plausible (mostreig), no es compleix o indeterminat, propietat per propietat.", "Regles", "rule")),
    ...temes.map((t) => el("section", { class: "teoria-tema ce-tema" },
      el("h3", { text: `Tema ${t}` }),
      el("ul", { class: "er-items" }, ...reptes.filter((r) => r.tema === t).map((r) => el("li", {},
        el("a", { class: "er-item ce-item", href: `#/contraexemples/${r.id}` },
          math(el("span", { class: "theory-name", text: r.titol })),
          el("span", { class: "pill neutral", text: CE_DIFICULTATS[r.dificultat] || r.dificultat }))))))));
}

/* ---------- a challenge ---------- */

function ceDraftKey(id) { return `ce:${id}`; }
function ceSaveDraft() {
  try { localStorage.setItem(ceDraftKey(CE.repte.id), JSON.stringify(CE.entrada)); } catch { /* storage unavailable */ }
}
function ceLoadDraft(id) {
  try { return JSON.parse(localStorage.getItem(ceDraftKey(id)) || "null"); } catch { return null; }
}

function ceCert(prop) {
  CE.entrada.certificats[prop] ??= { camins: [{ x: "", y: "" }, { x: "", y: "" }], fita: "", direccio: { u: "", w: "" }, parcial: "x" };
  return CE.entrada.certificats[prop];
}

async function viewContraexemple(id) {
  show("contraexemples");
  const [repte] = await Promise.all([
    api(`/api/contraexemples/${id}`),
    getTeoria().then((t) => t.byKey || indexTeoria(t)).catch(() => null),  // citations still render as text without it
  ]);
  crumbs([["Inici", "#/"], ["Contraexemples", "#/contraexemples"], [repte.titol.replace(/\$/g, ""), null]]);
  CE.repte = repte;
  CE.resultat = null;
  CE.entrada = ceLoadDraft(id) || { funcio: "", valor: "0", certificats: {} };
  ceRender();
}

function ceInput(label, value, onInput, attrs = {}) {
  const input = el("input", { type: "text", class: "ce-input", spellcheck: "false", autocomplete: "off", value, ...attrs });
  input.addEventListener("input", () => { onInput(input.value); ceSaveDraft(); });
  return el("label", { class: "ce-field" }, math(el("span", { class: "ce-label", text: label })), input);
}

function cePaths(cert, n) {
  return el("div", { class: "ce-paths" }, ...cert.camins.slice(0, n).map((p, i) => el("div", { class: "ce-row" },
    el("span", { class: "ce-row-label", text: i ? "Camí 2 (cal si pel camí 1 hi ha límit)" : "Camí 1" }),
    ceInput("$x(t) =$", p.x, (v) => { p.x = v; }, { placeholder: "t" }),
    ceInput("$y(t) =$", p.y, (v) => { p.y = v; }, { placeholder: i ? "0" : "t" }))));
}

function ceCertificate(prop) {
  if (prop.certificat === "cap") return el("p", { class: "small muted", text: "No cal certificat: ho calcula el codi." });
  const cert = ceCert(prop.id);
  const body = el("div", { class: "ce-cert" }, math(el("p", { class: "small muted", text: prop.ajuda })));
  if (prop.certificat === "camins" || prop.certificat === "camins_opcionals") body.append(cePaths(cert, 2));
  else if (prop.certificat === "fita") body.append(ceInput("$G(r) =$", cert.fita, (v) => { cert.fita = v; }, { placeholder: "r" }));
  else if (prop.certificat === "direccio") {
    body.append(el("div", { class: "ce-row" },
      ceInput("$v = ($", cert.direccio.u, (v) => { cert.direccio.u = v; }, { placeholder: "1", class: "ce-input short" }),
      ceInput("$,$", cert.direccio.w, (v) => { cert.direccio.w = v; }, { placeholder: "1", class: "ce-input short" }),
      math(el("span", { text: "$)$" }))));
  } else if (prop.certificat === "parcial_cami") {
    const select = el("select", { class: "ce-input mid" },
      ...["x", "y"].map((v) => el("option", { value: v, text: `∂f/∂${v}` })));
    select.value = cert.parcial;
    select.addEventListener("change", () => { cert.parcial = select.value; ceSaveDraft(); });
    body.append(el("label", { class: "ce-field" }, el("span", { class: "ce-label", text: "Derivada parcial" }), select), cePaths(cert, 2));
  }
  return body;
}

function ceNotes(r, node) {
  // Citations of the notes in a text become links to the PDF page (app.js).
  return linkCitations(node, r.tema);
}

function ceTheoryChips(items, prefix = "") {
  if (!items?.length) return null;
  return el("div", { class: "ce-teoria" },
    prefix ? el("span", { class: "small muted", text: prefix }) : null,
    ...items.map((it) => theoryButton(`📖 ${it.etiqueta}`, it.nom || it.etiqueta, [it], "ref-chip")));
}

function ceVerdict(v, prop) {
  if (!v) return null;
  const [cls, label] = CE_ESTATS[v.estat] || CE_ESTATS.indeterminat;
  return el("div", { class: `ce-verdict ${v.estat}` },
    el("span", { class: `pill ${cls}`, text: label,
      title: v.estat === "plausible" ? "Comprovat en milers de punts o direccions, però no demostrat" : "" }),
    ceNotes(CE.repte, math(el("span", { class: "ce-detail", text: v.detall }))),
    ["ok", "plausible"].includes(v.estat) ? null : ceTheoryChips(prop.teoria, "Repassa:"),
    v.calculs.length ? el("details", { class: "ce-calculs" },
      el("summary", { text: "Càlculs" }),
      ...v.calculs.map((c) => math(el("div", { text: `$${c}$` })))) : null);
}

function ceVisualLink() {
  const f = CE.entrada.funcio.trim();
  if (!f || typeof visualLink !== "function") return null;
  const mathjs = f.replace(/\*\*/g, "^").replace(/\bAbs\(/g, "abs(");
  const valor = Number(CE.entrada.valor);
  return el("a", { class: "btn ghost small-btn", target: "_blank", rel: "noopener",
    href: visualLink("punt", { f: mathjs, a: "0,0", fa: Number.isFinite(valor) ? valor : null }), text: "📈 Visualitza" });
}

function ceRender() {
  const r = CE.repte;
  const res = CE.resultat;
  const funcio = el("div", { class: "ce-funcio" },
    ceInput("$f(x,y) =$", CE.entrada.funcio, (v) => { CE.entrada.funcio = v; }, { placeholder: "x*y/(x**2+y**2)", class: "ce-input wide" }),
    el("span", { class: "small muted", text: "si (x,y) ≠ (0,0)" }),
    ceInput("$f(0,0) =$", CE.entrada.valor, (v) => { CE.entrada.valor = v; }, { placeholder: "0", class: "ce-input short" }));
  const props = r.propietats.map((p, i) => el("article", {
    class: `cf-card ce-prop${res ? (["ok", "plausible"].includes(res.veredictes[i]?.estat) ? " right" : " wrong") : ""}` },
  el("div", { class: "cf-card-head" },
    el("span", { class: "cf-num", text: String(i + 1) }),
    math(el("span", { class: "ce-prop-label", text: p.etiqueta })),
    ceTheoryChips(p.teoria)),
  ceCertificate(p),
  ceVerdict(res?.veredictes[i], p)));

  const comprova = el("button", { type: "button", class: "btn primary", id: "ce-comprova", text: "Comprova" });
  comprova.addEventListener("click", ceComprova);
  const pista = el("details", { class: "cf-solution ce-pista" }, el("summary", { text: "Pista" }),
    ceNotes(r, math(el("p", { text: r.pista }))));

  // replaceChildren() would turn a null into the text "null".
  $("#view-contraexemples").replaceChildren(...[
    el("header", { class: "er-head" },
      el("div", { class: "er-title" },
        el("div", { class: "eyebrow", text: `Construeix el contraexemple · Tema ${r.tema} · ${CE_DIFICULTATS[r.dificultat] || ""}` }),
        math(el("h2", { text: r.titol })),
        ceNotes(r, math(el("p", { class: "ce-enunciat", text: r.enunciat }))),
        ceTheoryChips(r.teoria, "Als apunts:"))),
    el("section", { class: "cf-card ce-form" },
      funcio,
      el("p", { class: "small muted", text: CE_SINTAXI }),
      el("div", { class: "ce-actions" }, comprova, ceVisualLink(), el("span", { class: "small muted", id: "ce-status" }))),
    el("div", { class: "cf-list" }, ...props),
    res ? ceResum(res) : null,
    pista,
    ceExemple(res?.exemple || r.exemple, !!res?.superat)].filter(Boolean));
}

function ceResum(res) {
  const text = res.superat
    ? (res.rigoros ? "Repte superat: totes les propietats estan demostrades."
      : "Repte superat, però alguna propietat és «plausible»: el codi l'ha comprovada en milers de punts o direccions, "
        + "però no l'ha demostrada. Per demostrar una fita, escriu f en polars i fita el factor angular per una constant.")
    : "Encara no. «No es compleix»: la propietat és falsa per a la teva f. «No demostrat»: potser és certa, però el "
      + "certificat no ho prova (o falta).";
  return el("div", { class: `ce-resum ${res.superat ? "ok" : "bad"}`, text });
}

function ceExemple(ex, superat) {
  if (!ex) return null;
  const certs = Object.entries(ex.certificats || {}).map(([prop, c]) => {
    const parts = [];
    (c.camins || []).forEach((p, i) => parts.push(`camí ${i + 1}: (${p.x}, ${p.y})`));
    if (c.fita) parts.push(`G(r) = ${c.fita}`);
    if (c.direccio) parts.push(`v = (${c.direccio.u}, ${c.direccio.w})`);
    if (c.parcial) parts.push(`∂f/∂${c.parcial}`);
    const label = CE.repte.propietats.find((pp) => pp.id === prop)?.etiqueta || prop;
    return el("li", {}, math(el("span", { text: `${label}: ` })), el("code", { text: parts.join(" · ") }));
  });
  return el("details", { class: "cf-solution ce-exemple", ...(superat ? { open: "" } : {}) },
    el("summary", { text: superat ? "Un exemple de l'autor (per comparar)" : "Exemple de l'autor (professorat)" }),
    el("p", {}, el("code", { text: `f(x,y) = ${ex.funcio}` }), el("span", { text: "  ·  " }), el("code", { text: `f(0,0) = ${ex.valor}` })),
    certs.length ? el("ul", { class: "small" }, ...certs) : null,
    ceNotes(CE.repte, math(el("p", { class: "cf-res", text: ex.explicacio }))),
    ceTheoryChips(ex.teoria_reservada, "Als apunts, un exemple com aquest:"));
}

async function ceComprova() {
  if (CE.enviant) return;
  const r = CE.repte;
  const certificats = {};
  for (const p of r.propietats) {
    if (p.certificat === "cap") continue;
    const c = ceCert(p.id);
    const camins = c.camins.filter((cm) => cm.x.trim() || cm.y.trim());
    const cert = {};
    if (["camins", "camins_opcionals", "parcial_cami"].includes(p.certificat) && camins.length) cert.camins = camins;
    if (p.certificat === "parcial_cami") cert.parcial = c.parcial;
    if (p.certificat === "fita" && c.fita.trim()) cert.fita = c.fita;
    if (p.certificat === "direccio" && (c.direccio.u.trim() || c.direccio.w.trim())) cert.direccio = c.direccio;
    certificats[p.id] = cert;
  }
  CE.enviant = true;
  $("#ce-comprova").disabled = true;
  $("#ce-status").textContent = "Comprovant amb sympy…";
  try {
    CE.resultat = await api(`/api/contraexemples/${r.id}/comprova`, {
      method: "POST",
      body: JSON.stringify({ funcio: CE.entrada.funcio, valor: CE.entrada.valor || "0", certificats }),
    });
    ceRender();
  } catch (err) {
    $("#ce-status").textContent = err.message;
  } finally {
    CE.enviant = false;
    const b = $("#ce-comprova");
    if (b) b.disabled = false;
  }
}
