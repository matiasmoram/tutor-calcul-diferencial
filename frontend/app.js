"use strict";

const $ = (sel) => document.querySelector(sel);

const LABELS = {
  desorientacio: { en_cami: "en camí", dubte_puntual: "dubte puntual", encallat: "encallat", perdut: "perdut" },
  desorientacioClass: { en_cami: "ok", dubte_puntual: "accent", encallat: "warn", perdut: "bad" },
  intencio: {
    mostra_treball: "mostra treball", demana_pista: "demana pista", demana_solucio: "demana la solució",
    pregunta_conceptual: "pregunta conceptual", proposa_resultat: "proposa resultat",
    fora_de_tema: "fora de tema", frustracio: "frustració",
  },
  accio: {
    redirigir: "redirigir", tancar: "tancar", despres_de_tancar: "després de tancar", demanar_raonament: "demanar raonament", demanar_intent: "demanar un intent", mostrar_conclusio: "mostrar conclusió", demanar_justificacio: "demanar justificació",
    demanar_conclusio: "demanar conclusió", questionar_error: "qüestionar error",
    questionar_resultat: "qüestionar resultat", explicar_concepte: "explicar concepte",
    validar_i_avancar: "validar i avançar", pista: "pista", mostrar_pas: "mostrar pas",
  },
  estat: { no_iniciat: "no iniciat", en_curs: "en curs", completat: "completat", erroni: "erroni" },
};

const state = { session: null, sending: false, photo: null };

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k === "text") node.textContent = v;
    else node.setAttribute(k, v);
  }
  for (const c of children) if (c != null) node.append(c);
  return node;
}

function math(node) {
  if (window.renderMathInElement) {
    renderMathInElement(node, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false },
        { left: "\\(", right: "\\)", display: false },
      ],
      throwOnError: false,
    });
  }
  return node;
}

function tex(src, display = false) {
  const span = el("span");
  if (window.katex) katex.render(src, span, { throwOnError: false, displayMode: display });
  else span.textContent = src;
  return span;
}

// Professor key: open the app once with ?prof=<key> and it is remembered in this browser.
(() => {
  const k = new URLSearchParams(location.search).get("prof");
  try { if (k) localStorage.setItem("clauProfessor", k); } catch { /* private mode: key only for this load */ }
})();
function clauProfessor() {
  try { return localStorage.getItem("clauProfessor") || new URLSearchParams(location.search).get("prof") || ""; }
  catch { return new URLSearchParams(location.search).get("prof") || ""; }
}

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json", "X-Clau-Professor": clauProfessor() },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || `Error ${res.status}`);
  return data;
}

/* ---------- Views & routing ---------- */

const VIEWS = ["landing", "llistes", "llista", "exercici", "errades", "teoria", "professor", "visual", "afirmacions", "contraexemples"];
let PROFESSOR = false;  // set from /api/config: only professors get the panel, solutions and traces
const cache = { llistes: null, llista: {}, teoria: null };

/* ---------- Links to the course notes ---------- */

async function getTeoria() {
  cache.teoria ??= await api("/api/teoria");
  return cache.teoria;
}

// "Teorema 12 del Tema 3", "Definició 6 (Tema 2)", "Proposició 10 del tema 2"; tema optional (defaults to the exercise's).
const CITA = /\b(Definició|Teorema|Proposició|Lema|Corol·lari|Observació|Exemple|Exercici|Nota)\s+(\d+)(?:\s*\([a-z]\))?(?:\s*\((?:del\s+)?[Tt]ema\s+(\d)\)|\s+del\s+[Tt]ema\s+(\d))?/g;

function linkCitations(node, defaultTema) {
  // Turns citations of the notes inside rendered text into links that open the PDF at the item's page (new tab).
  const byKey = cache.teoria?.byKey;
  if (!byKey) return node;
  const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, {
    acceptNode: (t) => t.parentElement.closest(".katex, a") ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT,
  });
  const texts = [];
  while (walker.nextNode()) texts.push(walker.currentNode);
  for (const t of texts) {
    const s = t.nodeValue;
    CITA.lastIndex = 0;
    if (!CITA.test(s)) continue;
    CITA.lastIndex = 0;
    const frag = document.createDocumentFragment();
    let last = 0;
    for (const m of s.matchAll(CITA)) {
      const tema = Number(m[3] || m[4] || defaultTema);
      const item = byKey[`${m[1]} ${m[2]}|${tema}`];  // the type must match: "Teorema 17" is not "Proposició 17"
      if (!item) continue;
      frag.append(s.slice(last, m.index));
      frag.append(el("a", { class: "cita", href: item.pdf, target: "_blank", rel: "noopener",
        title: `${item.etiqueta}${item.nom ? " — " + item.nom : ""} · obre els apunts (pàg. ${item.pagina})`, text: m[0] }));
      last = m.index + m[0].length;
    }
    if (!last) continue;
    frag.append(s.slice(last));
    t.replaceWith(frag);
  }
  return node;
}

function indexTeoria(data) {
  data.byKey = {};
  // etiqueta = "Teorema 12 (Tema 3)" -> key "Teorema 12|3"
  for (const t of data.temes) for (const it of t.items) if (it.num != null) data.byKey[`${it.etiqueta.split(" (")[0]}|${it.tema}`] = it;
  return data;
}

async function viewTeoria() {
  show("teoria");
  crumbs([["Inici", "#/"], ["Teoria", null]]);
  const data = await getTeoria();
  const root = $("#view-teoria");
  const temes = data.temes.map((t) => {
    const seccions = new Map();
    for (const it of t.items) {
      if (!seccions.has(it.seccio)) seccions.set(it.seccio, []);
      seccions.get(it.seccio).push(it);
    }
    const titols = Object.fromEntries((t.seccions || []).map((s) => [String(s.id), s.titol]));
    const body = el("div", { class: "teoria-items" },
      ...[...seccions].map(([sec, items]) => el("div", { class: "teoria-seccio" },
        el("h4", { text: titols[sec] ? `${sec} ${titols[sec]}` : (sec || "") }),
        el("ul", {}, ...items.filter((it) => it.num != null).map((it) => el("li", {},
          el("a", { href: it.pdf, target: "_blank", rel: "noopener" },
            el("span", { class: "theory-label", text: it.etiqueta.replace(/ \(Tema \d\)$/, "") }),
            math(el("span", { class: "theory-name", text: it.nom ? ` — ${it.nom}` : "" })),
            el("span", { class: "small muted", text: ` · pàg. ${it.pagina}` }))))))));
    return el("details", { class: "teoria-tema" },
      el("summary", {}, el("strong", { text: `Tema ${t.tema}` }), math(el("span", { text: ` · ${t.titol}` }))),
      el("div", { class: "teoria-actions" },
        el("a", { class: "btn ghost", href: t.pdf, target: "_blank", rel: "noopener", text: "Obre els apunts (PDF) ↗" }),
        el("a", { class: "btn ghost", href: `#/exercicis/tema-${t.tema}`, text: "Problemes del tema →" })),
      body);
  });
  root.replaceChildren(
    el("section", { class: "hero left" },
      el("h2", { text: "Teoria del curs" }),
      el("p", { class: "muted", text: "Apunts de Càlcul Diferencial (FME-UPC). Cada definició, teorema o exemple obre el PDF a la seva pàgina. Les cites del tutor porten aquí mateix." }),
      el("a", { class: "btn ghost", href: data.problemes_pdf, target: "_blank", rel: "noopener", text: "Col·lecció de problemes (PDF) ↗" })),
    el("div", { class: "teoria-temes" }, ...temes));
}

// Two ways to practise the same exercise lists.
const MODES = {
  exercicis: {
    label: "Exercicis",
    title: "Exercicis amb tutor",
    intro: "Tria una llista. El tutor et guiarà amb preguntes, sense donar-te la solució.",
  },
  errades: {
    label: "Troba l'error",
    title: "Resolucions amb errors",
    intro: "Tria un exercici: et donarem una resolució amb errors amagats. Subratlla'ls i explica per què estan malament.",
  },
};

function show(view) {
  for (const v of VIEWS) $(`#view-${v}`).classList.toggle("hidden", v !== view);
  $("#toggle-wrap").classList.toggle("hidden", view !== "exercici" || !PROFESSOR);
  $("#view-exercici").classList.toggle("no-prof", !PROFESSOR || !$("#toggle-prof").checked);
  $(".nav-professor")?.classList.toggle("hidden", !PROFESSOR);
}

function crumbs(items) {
  const nav = $("#crumbs");
  nav.replaceChildren();
  items.forEach(([label, href], i) => {
    if (i) nav.append(el("span", { class: "sep", text: "›" }));
    nav.append(href ? el("a", { href, text: label }) : el("span", { class: "current", text: label }));
  });
}

function statement(ex, display = false, full = false) {
  // Pure-LaTeX statements render with KaTeX directly; prose statements carry $...$ math.
  // `full` prepends the problem's shared preamble (sub-parts only make sense with it).
  const own = ex.format === "latex" ? tex(ex.enunciat, display) : math(el("span", { text: ex.enunciat }));
  if (!full) return own;
  const hint = ex.indicacio && !ex.enunciat.includes(ex.indicacio)
    ? math(el("div", { class: "indicacio muted small", text: `Indicació: ${ex.indicacio}` }))
    : null;
  if (!ex.preambul) return hint ? el("div", { class: "statement-full" }, own, hint) : own;
  return el("div", { class: "statement-full" },
    math(el("div", { class: "preambul", text: ex.preambul })),
    el("div", { class: "apartat" }, ex.apartat ? el("span", { class: "apartat-label", text: `(${ex.apartat}) ` }) : null, own),
    hint);
}

function theoryCard(item, open = false) {
  // One item of the course notes: label + name, expandable to its statement (and proof, if any).
  const body = el("div", { class: "theory-body" }, math(el("div", { text: item.enunciat })));
  if (item.demostracio) {
    body.append(el("details", { class: "theory-proof" },
      el("summary", { text: "Demostració" }), math(el("div", { text: item.demostracio }))));
  }
  body.append(el("a", { class: "theory-src", href: item.pdf, target: "_blank", rel: "noopener",
    text: `Obre als apunts del Tema ${item.tema}${item.pagina ? `, pàg. ${item.pagina}` : ""} ↗` }));
  linkCitations(body, item.tema);
  const d = el("details", { class: "theory-card" },
    el("summary", {}, el("span", { class: "theory-label", text: item.etiqueta }),
      item.nom ? math(el("span", { class: "theory-name", text: ` — ${item.nom}` })) : null),
    body);
  if (open) d.open = true;
  return d;
}

function theoryPopup(title, items) {
  // Hint-style popup with items of the notes; closes with Esc, the × button or a click on the backdrop.
  let dlg = $("#theory-dialog");
  if (!dlg) {
    dlg = el("dialog", { id: "theory-dialog", class: "theory-dialog" });
    dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
    document.body.append(dlg);
  }
  const close = el("button", { type: "button", class: "dialog-close", "aria-label": "Tanca", text: "×" });
  close.addEventListener("click", () => dlg.close());
  dlg.replaceChildren(
    el("div", { class: "dialog-head" }, el("h3", { text: title }), close),
    el("div", { class: "dialog-body" }, ...items.map((it) => theoryCard(it, items.length === 1))));
  dlg.showModal();
}

function theoryButton(label, title, items, cls = "hint-btn") {
  const b = el("button", { type: "button", class: cls, text: label });
  b.addEventListener("click", () => theoryPopup(title, items));
  return b;
}

async function getLlistes() {
  cache.llistes ??= await api("/api/llistes");
  return cache.llistes;
}

async function getLlista(id) {
  cache.llista[id] ??= await api(`/api/llistes/${id}`);
  return cache.llista[id];
}

const TIPUS = { calcul: "Càlcul", teoric: "Teòric", mixt: "Càlcul i teoria" };

let landingRendered = false;

async function viewLanding() {
  show("landing");
  crumbs([]);
  if (!landingRendered) {
    math($("#view-landing"));
    $("#to-how").addEventListener("click", () => $("#how").scrollIntoView({ behavior: "smooth" }));
    landingRendered = true;
  }
  const [cfg, llistes] = await Promise.all([api("/api/config"), getLlistes()]);
  $("#fact-lists").textContent = llistes.length;
  $("#fact-problems").textContent = llistes.reduce((n, l) => n + l.n_exercicis, 0);
  const models = [...new Set(Object.values(cfg.stages).map((s) => s.model))].join(", ");
  $("#api-status").textContent = cfg.api_key
    ? `Model: ${cfg.provider} · ${models}`
    : `Falta la clau d'API (${cfg.provider}) al fitxer .env`;
}

async function viewLlistes(mode) {
  show("llistes");
  const m = MODES[mode];
  crumbs(mode === "errades"
    ? [["Inici", "#/"], [m.label, "#/errades"], ["Resolucions", null]]
    : [["Inici", "#/"], [m.label, null]]);
  $("#llistes-title").textContent = m.title;
  $("#llistes-intro").textContent = m.intro;
  const llistes = await getLlistes();
  $("#lists").replaceChildren(...llistes.map((l) =>
    el("a", { class: "list-card", href: `#/${mode}/${l.id}` },
      el("span", { class: "list-num", text: l.etiqueta }),
      el("div", { class: "list-body" },
        el("h3", { text: l.titol }),
        el("p", { class: "muted", text: l.descripcio }),
        el("div", {},
          el("span", { class: `badge ${l.tipus === "teoric" ? "warn" : "accent"}`, text: TIPUS[l.tipus] }),
          el("span", { class: "badge", text: `${l.n_problemes} problemes` }),
          el("span", { class: "badge", text: `${l.n_exercicis} exercicis` }))))));
}

async function viewLlista(mode, id) {
  show("llista");
  const m = MODES[mode];
  const l = await getLlista(id);
  crumbs(mode === "errades"
    ? [["Inici", "#/"], [m.label, "#/errades"], ["Resolucions", "#/errades/problemes"], [l.etiqueta, null]]
    : [["Inici", "#/"], [m.label, `#/${mode}`], [l.etiqueta, null]]);
  $("#llista-header").replaceChildren(
    el("div", { class: "eyebrow", text: `${m.label} · ${l.etiqueta} · ${TIPUS[l.tipus]}` }),
    el("h2", { text: l.titol }),
    el("p", { class: "muted", text: mode === "errades" ? m.intro : l.descripcio }));
  const byId = Object.fromEntries(l.exercicis.map((e) => [e.id, e]));
  const go = mode === "errades" ? "Troba l'error →" : "→";
  // "Find the error": mark the exercises with documents ready (they open instantly, without the API).
  const ready = mode === "errades" ? await api("/api/errades/disponibles").catch(() => ({})) : {};
  const link = (ex, label) => el("a", { class: `problem ${ex.format}`, href: `#/${mode}/${id}/${ex.id}` },
    el("span", { class: "problem-label", text: label }),
    el("span", { class: "problem-statement" }, statement(ex)),
    ready[ex.id] ? el("span", { class: "badge ok", title: "Hi ha resolucions preparades", text: "a punt" }) : null,
    el("span", { class: "problem-go", text: go }));
  // One block per problem of the collection: shared statement, then its sub-parts.
  $("#problems").replaceChildren(...l.problemes.map((p) => {
    const exs = p.exercicis.map((e) => byId[e]);
    if (exs.length === 1 && !exs[0].apartat) {
      return el("li", { class: "problem-group" }, link(exs[0], `Problema ${p.num}`),
        p.font ? el("div", { class: "problem-font muted small", text: p.font }) : null);
    }
    return el("li", { class: "problem-group" },
      el("div", { class: "problem-head" },
        el("span", { class: "problem-label", text: `Problema ${p.num}` }),
        p.preambul ? math(el("div", { class: "problem-preambul", text: p.preambul })) : null,
        p.font ? el("div", { class: "problem-font muted small", text: p.font }) : null),
      el("ol", { class: "problem-parts" }, ...exs.map((ex) => el("li", {}, link(ex, `(${ex.apartat})`)))));
  }));
}

async function viewExercici(llistaId, exId) {
  show("exercici");
  const l = await getLlista(llistaId);
  crumbs([["Inici", "#/"], ["Exercicis", "#/exercicis"], [l.etiqueta, `#/exercicis/${llistaId}`],
    [l.exercicis.find((e) => e.id === exId)?.etiqueta || exId, null]]);
  $("#back-to-list").href = `#/exercicis/${llistaId}`;
  $("#grup-titol").textContent = `${l.etiqueta} · ${l.titol}`;
  $("#exercise-list").replaceChildren(...l.exercicis.map((ex) =>
    el("li", {},
      el("a", { class: `side-ex ${ex.format}${ex.id === exId ? " active" : ""}`, href: `#/exercicis/${llistaId}/${ex.id}` },
        el("span", { class: "ex-label", text: ex.etiqueta }),
        el("span", { class: "ex-math" }, statement(ex))))));
  $("#exercise-list .active")?.scrollIntoView({ block: "center" });
  await startSession(exId);
}

async function startSession(id) {
  const [data] = await Promise.all([
    api("/api/sessions", { method: "POST", body: JSON.stringify({ exercici_id: id }) }),
    getTeoria().then((t) => t.byKey || indexTeoria(t)).catch(() => null),  // citations still render as text without it
  ]);
  state.session = { ...data, traces: [] };
  clearPhoto();
  const ex = data.exercici;
  $("#statement").replaceChildren(
    el("div", { class: "label", text: `${data.llista.etiqueta} · Problema ${ex.etiqueta}${ex.font ? ` · ${ex.font}` : ""}` }),
    el("div", { class: `statement-body ${ex.format}` }, statement(ex, true, true)),
    el("div", { class: "statement-tools" },
      data.teoria.length
        ? theoryButton(`💡 Teoria útil (${data.teoria.length})`, "Teoria útil per a aquest problema", data.teoria)
        : null,
      visualitzaExercici(ex)));
  $("#messages").replaceChildren(
    math(el("div", { class: "msg tutor", text: "Hola! Explica'm què has provat fins ara amb aquest problema i on t'has encallat. Si encara no has començat, digues-me què et sembla que caldria fer primer." })));
  renderProf();
  $("#input").focus();
}

let cfgLoaded = false;

const FLAG_LABELS = { fallbacks: "fallbacks", rebutjos_guardia: "esborranys rebutjats", bucles: "bucles",
  mostrar_pas: "passos mostrats", frustracio: "frustració" };

async function viewProfessor() {
  show("professor");
  crumbs([["Inici", "#/"], ["Professorat", null]]);
  const root = $("#view-professor");
  if (!PROFESSOR) {
    root.replaceChildren(el("p", { class: "muted", text: "Aquesta pàgina és només per al professorat (obre l'app amb ?prof=<clau>)." }));
    return;
  }
  const sessions = await api("/api/professor/sessions");
  const rows = sessions.map((s) => el("tr", {},
    el("td", {}, el("a", { href: `#/professor/${s.id}`, text: new Date(s.darrer * 1000).toLocaleString("ca") })),
    el("td", { text: s.exercici }),
    el("td", { text: String(s.torns) }),
    el("td", { text: s.tancat ? "sí" : "no" }),
    el("td", {}, ...Object.keys(FLAG_LABELS).filter((k) => s[k] > 0)
      .map((k) => badge(`${FLAG_LABELS[k]}: ${s[k]}`, k === "frustracio" || k === "bucles" || k === "fallbacks" ? "bad" : "warn")))));
  root.replaceChildren(
    el("section", { class: "hero left" },
      el("h2", { text: "Revisió de converses" }),
      el("p", { class: "muted", text: "Sessions anònimes, de la més recent a la més antiga. Les marques indiquen què convé revisar." })),
    sessions.length
      ? el("table", { class: "prof-table" },
          el("thead", {}, el("tr", {}, ...["Darrer missatge", "Exercici", "Torns", "Resolt", "Marques"].map((h) => el("th", { text: h })))),
          el("tbody", {}, ...rows))
      : el("p", { class: "muted", text: "Encara no hi ha converses." }));
}

async function viewProfessorSessio(id) {
  show("professor");
  crumbs([["Inici", "#/"], ["Professorat", "#/professor"], [id.slice(0, 8), null]]);
  const torns = await api(`/api/professor/sessions/${id}`);
  const root = $("#view-professor");
  root.replaceChildren(
    el("section", { class: "hero left" }, el("h2", { text: `Sessió ${id.slice(0, 8)} · ${torns[0]?.exercici || ""}` })),
    el("div", { class: "prof-transcript" }, ...torns.map((t) => {
      const p = t.trace.pla;
      return el("div", { class: "prof-turn" },
        math(el("div", { class: "msg alumne", text: t.alumne })),
        math(el("div", { class: "msg tutor", text: t.tutor })),
        el("div", { class: "small muted" },
          badge(LABELS.accio[p.accio] || p.accio, "accent"),
          p.pas_objectiu ? badge(`pas ${p.pas_objectiu}`) : null,
          p.nivell_pista ? badge(`pista ${p.nivell_pista}`) : null,
          p.moviment ? badge(p.moviment) : null,
          t.trace.fallback ? badge("fallback", "bad") : null,
          t.trace.intents.length > 1 ? badge(`${t.trace.intents.length - 1} rebutjats`, "warn") : null,
          el("span", { text: ` ${p.motiu}` })));
    })));
}

async function route() {
  let parts = location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
  // Old links: #/problemes and #/llista/<id>/<ex>.
  if (parts[0] === "problemes") parts = ["exercicis"];
  if (parts[0] === "llista") parts = ["exercicis", ...parts.slice(1)];
  const [mode, llista, ex] = parts;
  try {
    if (!cfgLoaded) {
      const cfg = await api("/api/config");
      PROFESSOR = cfg.panell_professor;
      cfgLoaded = true;
    }
    if (mode === "teoria") await viewTeoria();
    else if (mode === "visual") await viewVisual(llista);
    else if (mode === "afirmacions") await (llista ? viewAfirmacions(llista) : viewAfirmacionsInici());
    else if (mode === "contraexemples") await (llista ? viewContraexemple(llista) : viewContraexemplesInici());
    else if (mode === "professor") await (llista ? viewProfessorSessio(llista) : viewProfessor());
    else if (mode === "errades" && !llista) await viewErradesInici();
    else if (mode === "errades" && llista === "teoria") await (ex ? viewErradesTeoria(ex) : viewErradesTeoriaLlista());
    else if (mode === "errades" && llista === "problemes") await viewLlistes("errades");
    else if (mode in MODES && ex) await (mode === "errades" ? viewErrades(llista, ex) : viewExercici(llista, ex));
    else if (mode in MODES && llista) await viewLlista(mode, llista);
    else if (mode in MODES) await viewLlistes(mode);
    else await viewLanding();
  } catch (err) {
    show("landing");
    $("#api-status").textContent = err.message;
  }
  window.scrollTo(0, 0);
}

/* ---------- Chat ---------- */

function addMessage(rol, text, extra) {
  const node = el("div", { class: `msg ${rol}`, text });
  math(node);
  if (extra) node.append(extra);
  $("#messages").append(node);
  node.scrollIntoView({ behavior: "smooth", block: "end" });
  return node;
}

async function send(text) {
  // Everything below belongs to the session that was open when the message was sent: a reply that
  // arrives after the student has switched exercise must not land in the new chat.
  const sess = state.session;
  if (!sess || sess.sending || !text.trim()) return;
  sess.sending = true;
  $("#send").disabled = true;
  const photo = state.photo;
  const bubble = addMessage("alumne", text);
  if (photo) bubble.prepend(el("img", { class: "msg-photo", src: photo.dataUrl, alt: "Foto de la llibreta" }));
  $("#input").value = "";
  $("#preview").replaceChildren();
  clearPhoto();
  const pending = addMessage("thinking", "El tutor està pensant… (diagnosi → pla → redacció → guardià)");
  try {
    const data = await api(`/api/sessions/${sess.session_id}/missatges`, {
      method: "POST",
      body: JSON.stringify({ text, origen: photo ? "foto" : "text" }),
    });
    if (state.session !== sess) return;
    pending.remove();
    const tag = data.trace.fallback
      ? el("span", { class: "fallback-tag", text: "Missatge de seguretat: cap esborrany ha passat el guardià." })
      : null;
    const node = addMessage("tutor", data.missatge, tag);
    linkCitations(node, sess.exercici.tema);
    if (data.referencies.length) {
      node.append(el("div", { class: "msg-refs" }, ...data.referencies.map((it) =>
        theoryButton(`📖 ${it.etiqueta}`, it.nom || it.etiqueta, [it], "ref-chip"))));
    }
    sess.traces.push(data.trace);
    renderProf();
  } catch (err) {
    if (state.session !== sess) return;
    pending.remove();
    addMessage("error", err.message);
  } finally {
    sess.sending = false;
    if (state.session === sess) {
      $("#send").disabled = false;
      $("#input").focus();
    }
  }
}

$("#composer").addEventListener("submit", (e) => {
  e.preventDefault();
  send($("#input").value);
});
$("#input").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    send($("#input").value);
  }
});
$("#input").addEventListener("input", () => {
  const v = $("#input").value;
  const preview = $("#preview");
  if (v.includes("$")) {
    preview.textContent = v;
    math(preview);
  } else preview.replaceChildren();
});
/* ---------- Photo of the notebook ---------- */

const MAX_SIDE = 1800;

function loadImage(file) {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => { URL.revokeObjectURL(url); resolve(img); };
    img.onerror = () => { URL.revokeObjectURL(url); reject(new Error("No s'ha pogut llegir la imatge.")); };
    img.src = url;
  });
}

async function shrink(file) {
  // Phone photos are 4-12 MB; handwriting stays legible at ~1800 px and the upload stays small.
  const img = await loadImage(file);
  const scale = Math.min(1, MAX_SIDE / Math.max(img.naturalWidth, img.naturalHeight));
  const canvas = document.createElement("canvas");
  canvas.width = Math.round(img.naturalWidth * scale);
  canvas.height = Math.round(img.naturalHeight * scale);
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = "#fff";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL("image/jpeg", 0.85);
}

function clearPhoto() {
  state.photo = null;
  $("#attachment").replaceChildren();
  $("#attachment").classList.add("hidden");
}

function renderAttachment(dataUrl, status, cls = "") {
  const box = $("#attachment");
  box.classList.remove("hidden");
  const remove = el("button", { type: "button", class: "attach-remove", title: "Treu la foto", "aria-label": "Treu la foto", text: "×" });
  remove.addEventListener("click", clearPhoto);
  box.replaceChildren(
    el("img", { src: dataUrl, alt: "Foto adjunta" }),
    el("div", { class: `attach-status ${cls}` }, ...status),
    remove);
}

async function attachPhoto(file) {
  const sess = state.session;  // a transcription that arrives after switching exercise is dropped
  if (!sess || !file) return;
  if (!file.type.startsWith("image/")) {
    addMessage("error", "Només es poden adjuntar imatges (JPG, PNG, WebP).");
    return;
  }
  let dataUrl;
  try {
    dataUrl = await shrink(file);
  } catch (err) {
    addMessage("error", err.message);
    return;
  }
  state.photo = null;
  renderAttachment(dataUrl, [el("strong", { text: "Transcrivint la foto…" }),
    el("span", { class: "muted", text: "Llegint la teva llibreta" })], "busy");
  $("#attach").disabled = true;
  try {
    const t = await api(`/api/sessions/${sess.session_id}/transcripcio`, {
      method: "POST",
      body: JSON.stringify({ imatge: dataUrl }),
    });
    if (state.session !== sess) return;
    if (t.contingut !== "treball_matematic" || !t.transcripcio) {
      renderAttachment(dataUrl, [el("strong", { text: "No hi he trobat treball matemàtic." }),
        el("span", { class: "muted", text: "Prova amb una foto més propera i ben il·luminada." })], "bad");
      return;
    }
    state.photo = { dataUrl, transcripcio: t };
    const input = $("#input");
    input.value = input.value.trim() ? `${input.value.trim()}\n\n${t.transcripcio}` : t.transcripcio;
    input.dispatchEvent(new Event("input"));
    const lines = [el("strong", { text: "Revisa la transcripció abans d'enviar" }),
      el("span", { class: "muted", text: "L'he posada a la caixa de text: corregeix el que no s'hagi llegit bé." })];
    if (t.llegibilitat !== "bona") {
      lines.push(el("span", { class: "warn-text",
        text: `Llegibilitat ${t.llegibilitat === "parcial" ? "parcial" : "dolenta"}${t.dubtes.length ? ": " + t.dubtes.join("; ") : ""}` }));
    }
    renderAttachment(dataUrl, lines, t.llegibilitat === "bona" ? "ok" : "warn");
    input.focus();
  } catch (err) {
    renderAttachment(dataUrl, [el("strong", { text: "No s'ha pogut transcriure" }),
      el("span", { class: "muted", text: err.message })], "bad");
  } finally {
    $("#attach").disabled = false;
  }
}

$("#attach").addEventListener("click", () => $("#photo-input").click());
$("#photo-input").addEventListener("change", (e) => {
  attachPhoto(e.target.files[0]);
  e.target.value = "";
});
$("#input").addEventListener("paste", (e) => {
  const file = [...(e.clipboardData?.files || [])].find((f) => f.type.startsWith("image/"));
  if (file) {
    e.preventDefault();
    attachPhoto(file);
  }
});
$("#composer").addEventListener("dragover", (e) => {
  e.preventDefault();
  $("#composer").classList.add("dragging");
});
$("#composer").addEventListener("dragleave", () => $("#composer").classList.remove("dragging"));
$("#composer").addEventListener("drop", (e) => {
  e.preventDefault();
  $("#composer").classList.remove("dragging");
  attachPhoto([...e.dataTransfer.files].find((f) => f.type.startsWith("image/")));
});

$("#toggle-prof").addEventListener("change", (e) => {
  $("#view-exercici").classList.toggle("no-prof", !e.target.checked);
});

/* ---------- Professor panel ---------- */

function badge(text, cls = "") {
  return el("span", { class: `badge ${cls}`, text });
}

function meter(level) {
  const m = el("div", { class: `meter ${level >= 4 ? "max" : level >= 3 ? "hot" : ""}`, title: `Nivell de pista ${level}/4` });
  for (let i = 1; i <= 4; i++) m.append(el("span", { class: i <= level ? "on" : "" }));
  return m;
}

function kv(pairs) {
  const dl = el("dl", { class: "kv" });
  for (const [k, v] of pairs) {
    if (v == null || v === "") continue;
    dl.append(el("dt", { text: k }), typeof v === "string" ? math(el("dd", { text: v })) : el("dd", {}, v));
  }
  return dl;
}

function renderSummary() {
  const s = state.session;
  const last = s.traces.at(-1);
  const completats = last ? last.estat.completats : [];
  const nivells = last ? last.estat.nivell_per_pas : {};
  const estats = last ? Object.fromEntries(last.diagnosi.estat_passos.map((e) => [e.pas, e.estat])) : {};

  const steps = el("ul", { class: "steps" });
  for (const p of s.passos) {
    const st = completats.includes(p.id) ? "completat" : estats[p.id] || "no_iniciat";
    steps.append(el("li", {},
      el("span", { class: `dot ${st}`, title: LABELS.estat[st] }),
      math(el("span", { text: p.titol })),
      el("span", { class: "lvl", text: nivells[p.id] ? `pista ${nivells[p.id]}` : "" })));
  }
  const card = el("div", { class: "card" },
    el("h3", { text: "Estat de l'alumne" }), steps,
    kv([["Resultat", s.resultat], ["Nota", s.nota_professor]]));
  if (s.teoria_fitxa.length) {
    const ul = el("ul", { class: "theory-list" });
    for (const t of s.teoria_fitxa) {
      ul.append(el("li", {},
        el("strong", { text: t.etiqueta }), math(el("span", { text: t.nom ? ` — ${t.nom}` : "" })),
        el("span", { class: "small muted", text: t.on.length ? ` · ${t.on.join(", ")}` : "" }),
        t.reservada ? badge("reservada: resol l'exercici", "warn") : null));
    }
    card.append(el("div", { class: "section-title", text: "Teoria citada per la fitxa" }), ul);
  }
  if (last) {
    const d = last.diagnosi;
    card.append(el("div", { style: "margin-top:10px" },
      badge(LABELS.desorientacio[d.nivell_desorientacio], LABELS.desorientacioClass[d.nivell_desorientacio]),
      badge(LABELS.intencio[d.intencio]),
      badge(`acció: ${LABELS.accio[last.pla.accio]}`, "accent")));
  }
  return card;
}

function renderAttempt(a, i) {
  if (!a.missatge) {
    return el("div", { class: "attempt rejected" },
      el("div", { class: "section-title", text: `Esborrany ${i + 1}: error` }),
      el("div", { text: a.error }));
  }
  const ok = !a.determinista.length && a.llm && a.llm.veredicte === "ok";
  const node = el("div", { class: `attempt ${ok ? "ok" : "rejected"}` },
    el("div", { class: "section-title", text: `Esborrany ${i + 1}: ${ok ? "acceptat" : "rebutjat"}` }),
    math(el("div", { class: "draft", text: a.missatge })));
  const problems = [...a.determinista.map((p) => `[regla] ${p}`)];
  if (a.llm && a.llm.veredicte !== "ok") {
    problems.push(...a.llm.infraccions.map((p) => `[guardià] ${p}`));
    if (a.llm.explicacio) problems.push(`[guardià] ${a.llm.explicacio}`);
  }
  if (problems.length) {
    const ul = el("ul");
    problems.forEach((p) => ul.append(el("li", { text: p })));
    node.append(ul);
  }
  return node;
}

function renderTrace(t, open) {
  const d = t.diagnosi;
  const p = t.pla;
  const errors = d.errors_detectats.length
    ? el("span", {}, ...d.errors_detectats.map((e) => badge(e, "bad")))
    : "cap";
  const body = el("div", { class: "body" },
    t.origen === "foto" ? badge("Missatge transcrit d'una foto", "accent") : null,
    el("div", { class: "section-title", text: "1 · Diagnosi (sortida estructurada)" }),
    kv([
      ["Desorientació", badge(LABELS.desorientacio[d.nivell_desorientacio], LABELS.desorientacioClass[d.nivell_desorientacio])],
      ["Intenció", LABELS.intencio[d.intencio]],
      ["Pas actual (LLM)", d.pas_actual],
      ["Errors", errors],
      ["Error altre", d.error_altre],
      ["Resultat", `${d.resultat_proposat}${d.resultat_justificat ? " · justificat" : ""}`],
      ["Resum", d.resum_alumne],
      ["Evidència", d.evidencia ? `«${d.evidencia}»` : ""],
    ]),
    el("div", { class: "section-title", text: "2 · Pla (política determinista)" }),
    kv([
      ["Acció", badge(LABELS.accio[p.accio], "accent")],
      ["Pas objectiu", p.pas_objectiu || "—"],
      ["Nivell pista", el("div", {}, meter(p.nivell_pista), el("span", { class: "small muted", text: `${p.nivell_pista}/4` }))],
      ["Motiu", p.motiu],
      ["Regex vetades", String(p.regex_prohibides.length)],
      ["Teoria permesa", (t.teoria_permesa || []).join(", ") || "cap"],
    ]),
    el("div", { class: "section-title", text: "3 · Contingut que veu el redactor" }),
    el("pre", { class: "block", text: t.contingut_permes }),
    el("div", { class: "section-title", text: "4 · Redacció i guardià" }),
    ...t.intents.map(renderAttempt),
    t.fallback ? badge("Fallback: missatge segur predefinit", "warn") : null,
    el("div", { class: "calls", text:
      t.crides.map((c) => `${c.stage} ${(c.latency_ms / 1000).toFixed(1)}s · ${c.input_tokens}${c.cached_tokens ? ` (${c.cached_tokens} cache)` : ""}→${c.output_tokens} tok`).join("  |  ")
      + `  ·  total ${(t.latencia_ms / 1000).toFixed(1)}s` }));

  const rejected = t.intents.filter((a) => !(a.missatge && !a.determinista.length && a.llm && a.llm.veredicte === "ok")).length;
  const summary = el("summary", {},
    el("span", { class: "n", text: `Torn ${t.torn}` }),
    badge(LABELS.desorientacio[d.nivell_desorientacio], LABELS.desorientacioClass[d.nivell_desorientacio]),
    badge(LABELS.accio[p.accio], "accent"),
    p.nivell_pista ? badge(`pista ${p.nivell_pista}`) : null,
    rejected ? badge(`${rejected} rebutjat${rejected > 1 ? "s" : ""}`, "bad") : null);
  const det = el("details", { class: "turn" }, summary, body);
  if (open) det.open = true;
  return det;
}

function renderProf() {
  const s = state.session;
  if (!s || !PROFESSOR) return;
  $("#prof-summary").replaceChildren(renderSummary());
  const traces = [...s.traces].reverse();
  $("#prof-traces").replaceChildren(...traces.map((t, i) => renderTrace(t, i === 0)));
}

window.addEventListener("hashchange", route);
window.addEventListener("load", route);
