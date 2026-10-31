"use strict";

/* "Troba l'error": a document with hidden errors. Two activities share this view:
   - problema: a worked solution of an exercise ("resolució dolenta");
   - teoria: a result of the notes (statement + proof) with errors in the statement and in the proof.
   And two layouts (`format`):
   - sencer: the whole document at once; the student highlights spans, comments why they're wrong, and submits once;
   - per_parts ("Pas a pas"): the document split into parts, some of them with exactly one error each. The student
     reviews one flawed part at a time (earlier parts shown correct, later ones only by title), submits it and sees
     its correction before moving on.
   Shares el(), math(), tex(), api(), statement(), crumbs(), show(), theoryCard() and the difficulty, ready-dot and
   score helpers with app.js. */

const ERRORS_PER_DIFICULTAT = { facil: 1, normal: 2, dificil: 3 };
// Pas a pas: parts to review = min(errors, parts of the document), and a document has at least 2 parts.
const PARTS_PER_DIFICULTAT = { facil: "1 part", normal: "2 parts", dificil: "fins a 3 parts" };
const FORMATS = [
  { id: "per_parts", label: "Pas a pas", desc: "Revisa la resolució part per part; després de cada part en veus la correcció." },
  { id: "sencer", label: "Document sencer", desc: "Tota la resolució de cop, com quan repasses un examen; la correcció arriba al final." },
];
const TIPUS_ERROR = {
  calcul: "Càlcul", logica: "Lògica", hipotesi: "Hipòtesi", teorema_mal_aplicat: "Teorema mal aplicat",
  conclusio: "Conclusió", desigualtat: "Desigualtat", quantificador: "Quantificador", implicacio: "Implicació",
  pas_injustificat: "Pas injustificat", cas_oblidat: "Cas oblidat", definicio: "Definició",
};
const LOADING_STEPS = {
  problema: [
    "Escrivint una resolució amb errors amagats…",
    "Un segon model la revisa sense saber on són els errors…",
    "Comprovant que cada error és real i que no n'hi ha cap més…",
    "Gairebé a punt…",
  ],
  teoria: [
    "Reescrivint l'enunciat i la demostració amb errors amagats…",
    "Un segon model la compara amb els apunts sense saber on són els errors…",
    "Comprovant que cada error és real i que no n'hi ha cap més…",
    "Gairebé a punt…",
  ],
};
const LOADING_STEPS_PARTS = {
  problema: [
    "Escrivint la resolució correcta, part per part…",
    "Un segon model la comprova pas a pas…",
    "Amagant un error a cada part triada…",
    "Comprovant a cegues que cada part té exactament un error…",
    "Gairebé a punt…",
  ],
  teoria: [
    "Reescrivint l'enunciat i la demostració per parts a partir dels apunts…",
    "Un segon model la compara amb els apunts…",
    "Amagant un error a cada part triada…",
    "Comprovant a cegues que cada part té exactament un error…",
    "Gairebé a punt…",
  ],
};

const E = {
  font: "problema", llista: null, ex: null, item: null, dificultat: "normal", sessionId: null, sol: null,
  format: "per_parts", dispFmt: { per_parts: {}, sencer: {} }, disp: {}, avis: null,
  pp: null,  // Pas a pas: the parts seen so far, their results and hints, the part under review
  anotacions: [], actiu: null, resultat: null, revelats: new Set(), pistes: new Set(), seq: 0,
  req: 0, busy: false,  // req numbers each document load: only the latest one may touch the page
};

/* ---------- offsets: backend counts code points, JS strings count UTF-16 units ---------- */

const cpToU16 = (s, cp) => { let i = 0; for (let k = 0; k < cp && i < s.length; k++) i += s.codePointAt(i) > 0xffff ? 2 : 1; return i; };
const u16ToCp = (s, i) => Array.from(s.slice(0, i)).length;

/* ---------- layouts ---------- */

// The layout of the document on screen comes from the server's answer, not from the request.
const perParts = () => E.sol?.format === "per_parts";

function textFrag(n) {
  // Text of the markable fragment n (document-wide numbering): in Pas a pas, only the part under review.
  if (!perParts()) return E.sol.fragments[n - 1];
  const a = E.pp.actual;
  return a.fragments[n - a.primer_fragment];
}

const FORMAT_KEY = "errades.format";

function formatGuardat() {
  try {
    const f = localStorage.getItem(FORMAT_KEY);
    return FORMATS.some((x) => x.id === f) ? f : "per_parts";
  } catch { return "per_parts"; }
}

function guardaFormat(f) {
  try { localStorage.setItem(FORMAT_KEY, f); } catch { /* storage unavailable: the choice lasts this page */ }
}

const nomFormat = (id) => FORMATS.find((f) => f.id === id).label;
const altreFormat = (id) => (id === "per_parts" ? "sencer" : "per_parts");
const teDocuments = (f) => Object.values(E.dispFmt[f] || {}).some(Boolean);
const aquestaFont = () => (E.font === "teoria" ? "Aquest resultat" : "Aquest exercici");

async function disponiblesPerFormat(perFormat) {
  // {format: {difficulty: n}} for this source; a layout the server can't list counts as none ready.
  const all = await Promise.all(FORMATS.map((f) => perFormat(f.id)));
  return Object.fromEntries(FORMATS.map((f, i) => [f.id, all[i] || {}]));
}

function triaFormat() {
  // The remembered layout, unless this source has none ready in it, nothing may be generated and the other layout
  // has some: then the other one, with a notice. The remembered choice only changes on an explicit click.
  const pref = formatGuardat();
  const altre = altreFormat(pref);
  E.format = pref;
  E.avis = null;
  if (!teDocuments(pref) && !POT_GENERAR && teDocuments(altre)) {
    E.format = altre;
    E.avis = `${aquestaFont()} encara no té cap document «${nomFormat(pref)}» preparat: s'obre com a «${nomFormat(altre)}».`;
  }
  E.disp = E.dispFmt[E.format];
  E.dificultat = triaDificultat(E.disp, E.dificultat);
}

function canviaFormat(f) {
  guardaFormat(f);
  E.format = f;
  E.avis = null;
  E.disp = E.dispFmt[f];
  E.dificultat = triaDificultat(E.disp, E.dificultat);
  renderShell();
  carregar(false);
}

function layoutToggle(current, dispFor, onPick) {
  const wrap = el("div", { class: "diff-chips er-formats", role: "radiogroup", "aria-label": "Format" });
  for (const f of FORMATS) {
    const disp = dispFor?.(f.id);
    const b = el("button", { type: "button", class: `chip${f.id === current ? " on" : ""}`, role: "radio",
      "aria-checked": String(f.id === current), "data-format": f.id, title: f.desc },
      el("span", { text: f.label }),
      disp ? readyDots(disp, `${f.label}: documents preparats per dificultat`) : null);
    b.addEventListener("click", () => {
      if (f.id === current || E.busy) return;
      onPick(f.id);
    });
    wrap.append(b);
  }
  return wrap;
}

/* ---------- choosing an activity ---------- */

function viewErradesInici() {
  show("errades");
  crumbs([["Inici", "#/"], ["Troba l'error", null]]);
  const card = (href, icon, title, text) => el("a", { class: "mode", href },
    el("span", { class: "mode-icon", text: icon }), el("h3", { text: title }), math(el("p", { text })),
    el("span", { class: "mode-cta", text: "Entrar →" }));
  $("#view-errades").replaceChildren(
    el("section", { class: "hero left" },
      el("div", { class: "eyebrow", text: "Troba l'error" }),
      el("h2", { text: "Tria què vols revisar" }),
      el("p", { class: "muted", text: "Un resultat dels apunts o la resolució d'un problema amb errors amagats. Marca'ls sobre el text, explica per què són incorrectes i compara amb la correcció." })),
    el("div", { class: "modes two" },
      card("#/errades/teoria", "∀", "Teoremes i demostracions",
        "Un teorema, proposició, lema o corol·lari dels apunts amb errors: una hipòtesi que falta, una conclusió massa forta, un quantificador canviat, un pas de la demostració que no se segueix."),
      card("#/errades/problemes", "≠", "Resolucions de problemes",
        "La resolució d'un problema de la col·lecció, feta per un alumne no gaire fi: una desigualtat girada, un teorema aplicat sense les hipòtesis, un càlcul mal fet.")));
}

let erTeoria = {};  // format -> /api/errades/teoria

async function getErradesTeoria(format) {
  erTeoria[format] ??= await api(`/api/errades/teoria?format=${format}`);
  return erTeoria[format];
}

async function viewErradesTeoriaLlista(fresh = true) {
  show("errades");
  crumbs([["Inici", "#/"], ["Troba l'error", "#/errades"], ["Teoremes", null]]);
  if (fresh) erTeoria = {};  // availability changes as documents are generated
  const hash = location.hash;
  const format = formatGuardat();
  $("#view-errades").replaceChildren(carregant());
  const data = await getErradesTeoria(format);
  if (location.hash !== hash) return;
  const formats = layoutToggle(format, null, (f) => {
    guardaFormat(f);
    viewErradesTeoriaLlista(false).catch(viewError);
  });
  $("#view-errades").replaceChildren(
    el("section", { class: "hero left" },
      el("div", { class: "eyebrow", text: "Troba l'error · Teoria" }),
      el("h2", { text: "Teoremes i demostracions amb errors" }),
      el("p", { class: "muted", text: "Tria un resultat dels apunts. El reescriurem amb errors a l'enunciat i a la demostració; tu els has de trobar. Els punts indiquen les dificultats que ja estan preparades en el format triat (fàcil · normal · difícil)." }),
      el("div", { class: "er-formats-row" }, formats,
        el("span", { class: "muted small", text: FORMATS.find((f) => f.id === format).desc }))),
    el("div", { class: "teoria-temes" }, ...data.temes.filter((t) => t.items.length).map((t, i) => {
      const d = el("details", { class: "teoria-tema" },
        el("summary", {}, el("strong", { text: `Tema ${t.tema}` }), math(el("span", { text: ` · ${t.titol}` })),
          el("span", { class: "small muted", text: ` · ${t.items.length} resultats` })),
        el("ul", { class: "er-items" }, ...t.items.map((it) => el("li", {},
          el("a", { class: "er-item", href: `#/errades/teoria/${it.id}` },
            el("span", { class: "theory-label", text: etiquetaCurta(it.etiqueta) }),
            math(el("span", { class: "theory-name", text: it.nom || "" })),
            readyDots(it.disponibles, `Documents «${nomFormat(format)}» preparats per dificultat`))))));
      if (i === 0) d.open = true;
      return d;
    })));
}

/* ---------- entry points ---------- */

async function viewErrades(llistaId, exId) {
  show("errades");
  $("#view-errades").replaceChildren(carregant());
  const l = await getLlista(llistaId);
  const ex = l.exercicis.find((e) => e.id === exId);
  if (!ex) throw new Error("Exercici desconegut");
  crumbs([["Inici", "#/"], ["Troba l'error", "#/errades"], ["Resolucions", "#/errades/problemes"],
    [l.etiqueta, `#/errades/${llistaId}`], [ex.etiqueta, null]]);
  const dispFmt = await disponiblesPerFormat((f) =>
    api(`/api/errades/disponibles?format=${f}`).then((d) => d[ex.id]).catch(() => ({})));
  Object.assign(E, { font: "problema", llista: l, ex, item: null, dispFmt });
  triaFormat();
  renderShell();
  await carregar(false);
}

async function viewErradesTeoria(itemId) {
  show("errades");
  $("#view-errades").replaceChildren(carregant());
  const troba = (data) => data.temes.flatMap((t) => t.items).find((it) => it.id === itemId);
  const item = troba(await getErradesTeoria("sencer"));
  if (!item) throw new Error("Resultat dels apunts desconegut");
  crumbs([["Inici", "#/"], ["Troba l'error", "#/errades"], ["Teoremes", "#/errades/teoria"],
    [etiquetaCurta(item.etiqueta, ` · T${item.tema}`), null]]);
  const dispFmt = await disponiblesPerFormat((f) => (f === "sencer"
    ? item.disponibles
    : getErradesTeoria(f).then((d) => troba(d)?.disponibles).catch(() => ({}))));
  Object.assign(E, { font: "teoria", llista: null, ex: null, item, dispFmt });
  triaFormat();
  renderShell();
  await carregar(false);
}

function renderShell() {
  const root = $("#view-errades");
  const teoria = E.font === "teoria";
  const parts = E.format === "per_parts";
  const chips = difficultyChips({
    current: E.dificultat,
    disp: E.disp,
    sub: (d) => parts
      ? PARTS_PER_DIFICULTAT[d.id]
      : `${ERRORS_PER_DIFICULTAT[d.id]} error${ERRORS_PER_DIFICULTAT[d.id] > 1 ? "s" : ""}`,
    isBusy: () => E.busy,
    onPick: (id) => { E.dificultat = id; carregar(false); },
  });
  const formats = layoutToggle(E.format, (f) => E.dispFmt[f], canviaFormat);
  const nova = el("button", { type: "button", class: "btn ghost small-btn", id: "er-nova", text: teoria ? "↻ Una altra versió" : "↻ Una altra resolució" });
  nova.addEventListener("click", unAltre);

  const eyebrow = teoria
    ? `Troba l'error · Teoria · Tema ${E.item.tema}`
    : `Troba l'error · ${E.llista.etiqueta} · ${E.ex.etiqueta}`;
  const titol = parts
    ? (teoria ? "Aquest enunciat i la seva demostració tenen errors. Revisa'ls part per part." : "Aquesta resolució té errors. Revisa-la part per part.")
    : (teoria ? "Aquest enunciat i la seva demostració tenen errors. Troba'ls." : "Aquesta resolució té errors. Troba'ls.");
  const ajuda = parts
    ? "Cada part marcada té exactament un error: selecciona el tros que està malament, marca'l i explica per què. En enviar la part en veuràs la correcció."
    : "Selecciona amb el ratolí el tros que està malament, marca'l i explica per què. Quan acabis, envia la correcció.";
  const context = teoria
    ? el("section", { class: "er-statement" },
        el("span", { class: "er-statement-label", text: "Resultat" }),
        el("div", { class: "statement-body text" },
          el("strong", { text: E.item.etiqueta }), E.item.nom ? math(el("span", { text: ` — ${E.item.nom}` })) : null,
          el("div", { class: "muted small", text: "Reescrit a partir dels apunts. Hi ha almenys un error a l'enunciat; si n'hi ha més d'un, també a la demostració. En acabar veuràs l'original dels apunts." })))
    : el("section", { class: "er-statement" },
        el("span", { class: "er-statement-label", text: "Enunciat" }),
        el("div", { class: `statement-body ${E.ex.format}` }, statement(E.ex, E.ex.format === "latex", true)));

  root.replaceChildren(
    el("header", { class: "er-head" },
      el("div", { class: "er-title" },
        el("div", { class: "eyebrow", text: eyebrow }),
        el("h2", { text: titol }),
        el("p", { class: "muted", text: `${FORMATS.find((f) => f.id === E.format).desc} ${ajuda}` })),
      el("div", { class: "er-controls" }, formats, chips, nova)),
    ...(E.avis ? [el("p", { class: "er-avis", role: "status", text: E.avis })] : []),
    context,
    el("nav", { class: "er-roadmap", id: "er-roadmap", "aria-label": "Parts de la resolució" }),
    el("div", { class: "er-bar", id: "er-bar" }),
    el("div", { class: "er-workspace", id: "er-workspace" },
      el("div", { class: "er-paper-wrap", id: "er-paper-wrap" },
        el("article", { class: "er-paper", id: "er-paper" }),
        el("button", { type: "button", class: "er-mark hidden", id: "er-mark" }, el("span", { text: "✎" }), " Marca com a error")),
      el("aside", { class: "er-rail", id: "er-rail", "aria-label": "Comentaris" })),
    el("section", { class: "er-original hidden", id: "er-original" }));

  // Keep the selection alive (pointerdown also covers touch, where mousedown arrives too late).
  $("#er-mark").addEventListener("mousedown", (e) => e.preventDefault());
  $("#er-mark").addEventListener("pointerdown", (e) => e.preventDefault());
  $("#er-mark").addEventListener("click", crearAnotacio);
  $("#er-paper").addEventListener("pointerup", () => setTimeout(onSelection, 0));
  $("#er-paper").addEventListener("touchend", () => setTimeout(onSelection, 0));
  $("#er-paper").addEventListener("keyup", (e) => { if (e.shiftKey) onSelection(); });
}

// Phones select by long-press and drag handles: no mouseup/keyup, only selectionchange (debounced: it fires
// on every handle move). Registered once, not per document.
let selTimer = null;
document.addEventListener("selectionchange", () => {
  clearTimeout(selTimer);
  selTimer = setTimeout(onSelection, 250);
});

function erBusy(on) {
  // While a document loads or a correction runs: no other paid call can be fired from the page.
  E.busy = on;
  document.querySelectorAll("#view-errades .er-controls button").forEach((b) => { b.disabled = on; });
}

function erStale(req, hash) {
  // A response that is not for the latest load, or arrives after the student left this page, is dropped.
  return req !== E.req || location.hash !== hash;
}

function unAltre() {
  // With more than one ready document, "another" picks a different one (no API cost);
  // otherwise generating a new one needs an explicit click.
  if ((E.disp[E.dificultat] || 0) > 1) carregar(false);
  else oferirGenerar(true);
}

/* ---------- loading ---------- */

function resetDoc() {
  Object.assign(E, { sessionId: null, sol: null, pp: null, anotacions: [], actiu: null, resultat: null, revelats: new Set(), pistes: new Set() });
  $("#er-rail").replaceChildren();
  $("#er-bar").replaceChildren();
  $("#er-bar").classList.remove("final");
  $("#er-roadmap").replaceChildren();
  $("#er-original").classList.add("hidden");
}

function oferirGenerar(altre = false) {
  // Generating a document is a paid, minutes-long call: it only starts on an explicit click.
  E.req++;  // a load still in flight for another difficulty must not replace this
  erBusy(false);
  resetDoc();
  const paper = $("#er-paper");
  paper.classList.remove("loading");
  const other = altreFormat(E.format);
  if (!POT_GENERAR && !teDocuments(E.format) && teDocuments(other)) {
    // Nothing at all in this layout and nothing may be generated: offer the layout that has documents.
    const obre = el("button", { type: "button", class: "btn primary", text: `Obre-ho com a «${nomFormat(other)}»` });
    obre.addEventListener("click", () => canviaFormat(other));
    paper.replaceChildren(el("div", { class: "er-generate" },
      el("strong", { text: `${aquestaFont()} encara no té cap document «${nomFormat(E.format)}» preparat.` }),
      el("p", { class: "muted", text: `En format «${nomFormat(other)}» sí que n'hi ha.` }),
      obre));
    return;
  }
  const ready = DIFICULTATS.filter((d) => E.disp[d.id]).map((d) => d.label);
  const gen = el("button", { type: "button", class: "btn primary", text: "Genera'n un de nou (pot trigar uns minuts)" });
  gen.addEventListener("click", () => carregar(true));
  paper.replaceChildren(el("div", { class: "er-generate" },
    el("strong", { text: altre ? "No n'hi ha cap altre de preparat en aquesta dificultat." : "Encara no hi ha cap document preparat en aquesta dificultat." }),
    POT_GENERAR ? el("p", { class: "muted", text: "Se'n pot generar un de nou: un model l'escriu i un altre el verifica." }) : null,
    ready.length ? el("p", { class: "muted", text: `Hi ha documents preparats per a: ${ready.join(", ")}.` }) : null,
    POT_GENERAR ? gen : el("p", { class: "muted", text: "Prova una altra dificultat, o demana al professorat que en prepari un." })));
}

async function carregar(nova) {
  // nova=false only opens a ready document; with none ready, the student chooses whether to generate one.
  if (!nova && !E.disp[E.dificultat]) return oferirGenerar();
  const req = ++E.req;
  const hash = location.hash;
  const anterior = E.sol?.id || null;
  resetDoc();
  const steps = (E.format === "per_parts" ? LOADING_STEPS_PARTS : LOADING_STEPS)[E.font];
  const paper = $("#er-paper");
  paper.classList.add("loading");
  paper.replaceChildren(
    el("div", { class: "er-loading" },
      el("div", { class: "er-loading-step", id: "er-step", text: nova ? steps[0] : "Obrint el document…" }),
      ...[92, 78, 88, 64, 95, 70, 84, 58].map((w) => el("div", { class: "skeleton", style: `width:${w}%` }))));
  erBusy(true);
  let k = 0;
  const ticker = setInterval(() => {
    k = Math.min(k + 1, steps.length - 1);
    const step = $("#er-step");
    if (step && nova) step.textContent = steps[k];
  }, 9000);
  try {
    const font = E.font === "teoria" ? { teoria_id: E.item.id } : { exercici_id: E.ex.id };
    const data = await api("/api/errades/sessions", {
      method: "POST",
      body: JSON.stringify({ ...font, dificultat: E.dificultat, format: E.format, nova, excepte: anterior }),
    });
    if (erStale(req, hash)) return;
    E.sessionId = data.session_id;
    E.sol = data.solucio;
    if (data.generada_ara) E.disp[E.dificultat] = (E.disp[E.dificultat] || 0) + 1;
    if (perParts()) iniciPerParts();
    renderDoc();
  } catch (err) {
    if (erStale(req, hash)) return;
    const ready = DIFICULTATS.filter((d) => E.disp[d.id]).map((d) => d.label);
    // 403/409: the server refuses to generate (not allowed, or one already being generated): its message, as is.
    const refusal = err.status === 403 || err.status === 409;
    paper.replaceChildren(el("div", { class: "er-error" },
      el("strong", { text: refusal ? err.message : "No s'ha pogut preparar el document" }),
      refusal ? null : el("p", { class: "muted", text: err.message }),
      ready.length ? el("p", { class: "muted", text: `Hi ha documents preparats per a: ${ready.join(", ")}.` }) : null));
  } finally {
    clearInterval(ticker);
    if (req === E.req) {
      paper.classList.remove("loading");
      erBusy(false);
    }
  }
}

function renderDoc() {
  renderPaper();
  renderRoadmap();
  renderBar();
  renderRail();
}

/* ---------- the document ---------- */

function tokenize(text) {
  // Math chunks stay atomic so a selection never splits a formula.
  const out = [];
  const re = /(\$[^$]+\$)|(\s+)|([^\s$]+)/g;
  let m;
  while ((m = re.exec(text))) out.push({ s: m.index, e: m.index + m[0].length, t: m[0], math: !!m[1], ws: !!m[2] });
  return out;
}

function fragNode(text, n, markable) {
  // A markable fragment is split into tokens the student can select; the others are plain text.
  const p = el("p", { class: "frag", "data-frag": String(n) },
    el("span", { class: "frag-num", "aria-hidden": "true", text: String(n) }));
  if (!markable) {
    p.append(math(el("span", { class: "frag-body", text })));
    return p;
  }
  const body = el("span", { class: "frag-body" });
  for (const t of tokenize(text)) {
    const span = el("span", { class: `tok${t.math ? " m" : ""}${t.ws ? " ws" : ""}`, "data-s": String(t.s), "data-e": String(t.e) });
    if (t.math) span.append(tex(t.t.slice(1, -1)));
    else span.textContent = t.t;
    body.append(span);
  }
  p.append(body);
  return p;
}

function renderPaper() {
  if (perParts()) return renderParts();
  const paper = $("#er-paper");
  const nEn = E.sol.n_enunciat || 0;
  const frags = E.sol.fragments.map((text, i) => fragNode(text, i + 1, true));
  if (nEn) {
    // Theory: the statement first, then the proof (headings sit outside the fragments, so they can't be selected).
    frags.splice(nEn, 0, el("h4", { class: "er-sec", text: "Demostració" }));
    frags.unshift(el("h4", { class: "er-sec", text: "Enunciat" }));
  }
  paper.replaceChildren(...frags);
  paintHighlights();
}

// In Pas a pas a graded part always shows its error; in the whole document only the ones the student asks for.
const revelat = (id) => perParts() || E.revelats.has(id);

function paintHighlights(r = E.resultat) {
  const paper = $("#er-paper");
  paper.querySelectorAll(".tok").forEach((t) => {
    t.className = t.className.replace(/\s?(hl|hl-\S+|active|err-\S+)/g, "");
    delete t.dataset.ann;
  });
  const mark = (frag, s, e, cls, annId) => {
    paper.querySelectorAll(`.frag[data-frag="${frag}"] .tok`).forEach((t) => {
      if (+t.dataset.s < e && +t.dataset.e > s) {
        t.classList.add(...cls.split(" "));
        if (annId && !t.dataset.ann) t.dataset.ann = annId;
      }
    });
  };
  // Revealed/found real errors (after correction) go underneath the student's highlights.
  if (r) {
    for (const err of r.errors) {
      const text = textFrag(err.fragment);
      const found = r.anotacions.some((a) => a.error === err.id);
      if (found || revelat(err.id)) {
        mark(err.fragment, cpToU16(text, err.inici), cpToU16(text, err.fi), `err-real ${found ? "err-found" : "err-missed"}`);
      }
    }
  }
  for (const a of E.anotacions) {
    let cls = "hl";
    if (r) {
      const x = r.anotacions.find((y) => y.id === a.id);
      cls += x ? (x.error === "cap" ? " hl-wrong" : x.explicacio === "correcta" ? " hl-right" : " hl-partial") : "";
    }
    if (E.actiu === a.id) cls += " active";
    mark(a.fragment, a.s16, a.e16, cls, a.id);
  }
  paper.querySelectorAll(".tok[data-ann]").forEach((t) => {
    t.onclick = () => activar(t.dataset.ann);
  });
}

/* ---------- Pas a pas: one flawed part at a time ---------- */

function iniciPerParts() {
  E.pp = {
    textos: new Map(),  // part -> its correct fragments, as they become visible
    fets: new Map(),    // part -> { r: its grading, anotacions: the marks it graded }
    pistes: new Map(),  // part -> hint text
    actual: E.sol.actual,  // { part, primer_fragment, fragments (with its error), anteriors }; null at the end
    final: null,
  };
  absorbeix(E.sol.actual.anteriors);
}

function absorbeix(parts) {
  // [{part, fragments}]; the final resolution may also come as one list of fragments per part, in order.
  (parts || []).forEach((p, i) => {
    if (Array.isArray(p)) E.pp.textos.set(i + 1, p);
    else E.pp.textos.set(p.part, p.fragments);
  });
}

function estatPart(r) {
  // [pill class, short label, sentence] of a graded part, from its best match with the part's error.
  const best = r.anotacions.filter((a) => a.error !== "cap").sort((x, y) => y.punts - x.punts)[0];
  if (!best) return ["bad", "No trobat", "no has trobat l'error"];
  if (best.explicacio === "correcta") return ["ok", "Trobat", "has trobat l'error i l'has explicat bé"];
  return ["warn", "Parcial", "has trobat l'error, però l'explicació no és del tot correcta"];
}

function pillEstat(r) {
  const [cls, label] = estatPart(r);
  return el("span", { class: `pill ${cls}`, text: label });
}

function liniaCorreccio(err) {
  // A part already reviewed: what it said, struck through, and the correction.
  return el("div", { class: "er-fixline" },
    math(el("del", { class: "er-fix-wrong", text: err.cita })),
    el("span", { class: "er-fix-arrow", "aria-hidden": "true", text: "→" }),
    math(el("span", { class: "er-fix-right", text: err.correccio })));
}

function renderParts() {
  const paper = $("#er-paper");
  const pp = E.pp;
  const actual = pp.actual ? pp.actual.part : Infinity;  // the final screen shows every part
  let n = 1;  // document-wide number of the next fragment
  paper.replaceChildren(...E.sol.parts.map((p) => {
    const fet = pp.fets.get(p.part);
    const head = el("h4", { class: "er-part-head" },
      el("span", { class: "er-part-num", text: `Part ${p.part}` }),
      math(el("span", { class: "er-part-title", text: p.titol })));
    const sec = el("section", { class: "er-part", "data-part": String(p.part) }, head);
    if (p.part === actual) {
      sec.classList.add("current");
      head.append(E.resultat ? pillEstat(E.resultat) : el("span", { class: "pill warn", text: "Hi ha un error en aquesta part" }));
      const pista = pp.pistes.get(p.part);
      if (pista) sec.append(math(el("p", { class: "note-hint er-part-hint", text: `Pista: ${pista}` })));
      pp.actual.fragments.forEach((t, i) => sec.append(fragNode(t, pp.actual.primer_fragment + i, true)));
      n = pp.actual.primer_fragment + pp.actual.fragments.length;
    } else if (p.part < actual && pp.textos.has(p.part)) {
      sec.classList.add(fet ? "done" : "clean");
      if (fet) head.append(pillEstat(fet.r));
      const frags = pp.textos.get(p.part);
      frags.forEach((t, i) => sec.append(fragNode(t, n + i, false)));
      n += frags.length;
      if (fet) sec.append(...fet.r.errors.map(liniaCorreccio));
    } else {
      // Later parts are correct and would give the error away: only their titles until the student gets there.
      sec.classList.add("later");
      if (p.revisar) head.append(el("span", { class: "pill neutral", text: "a revisar" }));
      sec.append(el("p", { class: "er-part-hidden", text: "Es mostra quan hi arribis." }));
    }
    return sec;
  }));
  paintHighlights();
}

function renderRoadmap() {
  const nav = $("#er-roadmap");
  if (!perParts()) return nav.replaceChildren();
  const k = E.sol.n_errors;
  const actual = E.pp.actual?.part;
  nav.replaceChildren(
    el("p", { class: "er-roadmap-intro", text: k === 1 ? "Revisaràs 1 part; té exactament un error." : `Revisaràs ${k} parts; cadascuna té exactament un error.` }),
    el("ol", { class: "er-roadmap-list" }, ...E.sol.parts.map((p) => {
      const fet = E.pp.fets.get(p.part);
      let pill = null;
      if (fet) pill = pillEstat(fet.r);
      else if (p.part === actual) pill = el("span", { class: "pill warn", text: "ara" });
      else if (p.revisar) pill = el("span", { class: "pill neutral", text: "a revisar" });
      const b = el("button", { type: "button", class: `er-step${p.revisar ? " flawed" : ""}${p.part === actual ? " current" : ""}` },
        el("span", { class: "er-step-num", text: String(p.part) }),
        math(el("span", { class: "er-step-title", text: p.titol })),
        pill);
      if (p.part === actual) b.setAttribute("aria-current", "step");
      b.addEventListener("click", () => $(`#er-paper .er-part[data-part="${p.part}"]`)?.scrollIntoView({ behavior: "smooth", block: "start" }));
      return el("li", {}, b);
    })));
}

function renderBarParts() {
  const bar = $("#er-bar");
  const pp = E.pp;
  bar.classList.toggle("final", !pp.actual);
  if (!pp.actual) return renderFinal();
  if (E.resultat) return renderScorePart();
  const part = pp.actual.part;
  const revisar = E.sol.parts.filter((p) => p.revisar);
  const idx = revisar.findIndex((p) => p.part === part) + 1;
  const marcats = E.anotacions.length;
  const sense = E.anotacions.filter((a) => !a.comentari.trim()).length;
  const ambPista = pp.pistes.has(part);
  const actions = el("div", { class: "er-actions" });
  if (!ambPista) {
    const pista = el("button", { type: "button", class: "btn ghost small-btn", text: "Pista" });
    pista.addEventListener("click", demanaPista);
    actions.append(el("span", { class: "er-hint-cost muted small", text: "Si la demanes, la nota d'aquesta part baixa un 15 %." }), pista);
  }
  // With nothing marked the student can still move on: the part is graded as not found and shown corrected.
  const submit = el("button", { type: "button", class: marcats ? "btn primary" : "btn ghost", text: marcats ? "Envia aquesta part" : "No el trobo: mostra'l" });
  submit.addEventListener("click", enviarPart);
  actions.append(submit);
  bar.replaceChildren(
    el("div", { class: "er-progress" },
      el("span", {}, "Part ", el("strong", { text: String(part) }), ` · revisió ${idx} de ${revisar.length} · `,
        el("strong", { text: String(marcats) }), ` marcat${marcats === 1 ? "" : "s"}`),
      sense ? el("span", { class: "warn-text", text: ` · ${sense} sense explicació` }) : null,
      ambPista ? el("span", { class: "muted", text: " · amb pista" }) : null),
    actions);
}

function renderScorePart() {
  const r = E.resultat;
  const [, , frase] = estatPart(r);
  const seguir = el("button", { type: "button", class: "btn primary", text: r.seguent ? "Continua amb la part següent →" : "Mostra el resultat final →" });
  seguir.addEventListener("click", continuar);
  $("#er-bar").replaceChildren(
    el("div", { class: "er-score" }, scoreRing(r.nota),
      el("div", {},
        el("strong", { text: `Part ${r.part}: ${frase}` }),
        E.pp.pistes.has(r.part) ? el("span", { class: "muted", text: " · amb pista" }) : null,
        r.falsos_positius ? el("span", { class: "muted", text: ` · ${r.falsos_positius} marca${r.falsos_positius > 1 ? "des" : "da"} en passos correctes` }) : null,
        r.resum ? math(el("p", { class: "muted", text: r.resum })) : null)),
    seguir);
}

function renderFinal() {
  const f = E.pp.final;
  const again = el("button", { type: "button", class: "btn primary", text: E.font === "teoria" ? "Una altra versió" : "Una altra resolució" });
  again.addEventListener("click", unAltre);
  const tutor = E.font === "problema"
    ? el("a", { class: "btn ghost", href: `#/exercicis/${E.llista.id}/${E.ex.id}`, text: "Resol-lo amb el tutor →" })
    : null;
  $("#er-bar").replaceChildren(
    el("div", { class: "er-score" }, scoreRing(f.nota),
      el("div", {},
        el("strong", { text: `Has trobat ${f.trobats} de ${f.total} error${f.total > 1 ? "s" : ""}` }),
        f.falsos_positius ? el("span", { class: "muted", text: ` · ${f.falsos_positius} marca${f.falsos_positius > 1 ? "des" : "da"} en passos correctes` }) : null,
        el("ul", { class: "er-part-chips", "aria-label": "Nota de cada part" }, ...f.parts.map((fp) => {
          const fet = E.pp.fets.get(fp.part);
          const [cls, label] = fet ? estatPart(fet.r) : ["neutral", "Corregida"];
          return el("li", { class: "er-part-chip" },
            el("span", { text: `Part ${fp.part}` }),
            el("span", { class: `pill ${cls}`, text: label }),
            fp.pista ? el("span", { class: "pill neutral", text: "pista" }) : null,
            el("span", { class: "er-part-chip-nota", text: String(fp.nota) }));
        })))),
    el("div", { class: "er-actions" }, again, tutor));
}

function payloadAnotacions() {
  return E.anotacions.map((a) => {
    const text = textFrag(a.fragment);
    return { id: a.id, fragment: a.fragment, inici: u16ToCp(text, a.s16), fi: u16ToCp(text, a.e16), comentari: a.comentari };
  });
}

async function demanaPista() {
  if (E.busy || !E.sessionId || !E.pp?.actual) return;
  const req = E.req;
  const hash = location.hash;
  const part = E.pp.actual.part;
  const bar = $("#er-bar");
  bar.replaceChildren(el("div", { class: "er-progress" }, el("span", { class: "spinner" }),
    el("span", { text: "Demanant una pista…" })));
  erBusy(true);
  try {
    const { pista } = await api(`/api/errades/sessions/${E.sessionId}/parts/${part}/pista`, { method: "POST" });
    if (erStale(req, hash)) return;
    E.pp.pistes.set(part, pista);
    renderPaper();
    renderBar();
    renderRail();
  } catch (err) {
    if (erStale(req, hash)) return;
    renderBar();
    bar.append(el("span", { class: "warn-text", text: err.message }));
  } finally {
    if (req === E.req) erBusy(false);
  }
}

async function enviarPart() {
  if (E.busy || !E.sessionId || !E.pp?.actual) return;
  const req = E.req;
  const hash = location.hash;
  const part = E.pp.actual.part;
  const bar = $("#er-bar");
  bar.replaceChildren(el("div", { class: "er-progress" }, el("span", { class: "spinner" }),
    el("span", { text: "Corregint aquesta part…" })));
  erBusy(true);
  try {
    const r = await api(`/api/errades/sessions/${E.sessionId}/parts/${part}/correccio`, {
      method: "POST",
      body: JSON.stringify({ anotacions: payloadAnotacions() }),
    });
    if (erStale(req, hash)) return;
    E.resultat = r;
    E.actiu = null;
    E.pp.fets.set(part, { r, anotacions: E.anotacions });
    if (r.correcte) E.pp.textos.set(part, r.correcte);
    E.pp.final = r.final;
    renderDoc();
  } catch (err) {
    if (erStale(req, hash)) return;
    renderBar();
    bar.append(el("span", { class: "warn-text", text: err.message }));
  } finally {
    if (req === E.req) erBusy(false);
  }
}

function continuar() {
  const r = E.resultat;
  if (E.busy || !r) return;
  const pp = E.pp;
  if (r.seguent) {
    absorbeix(r.seguent.anteriors);
    pp.actual = r.seguent;
  } else if (r.final) {
    absorbeix(r.final.resolucio);
    pp.actual = null;
  } else return;
  Object.assign(E, { anotacions: [], actiu: null, resultat: null });
  renderDoc();
  if (pp.actual) {
    $("#er-paper .er-part.current")?.scrollIntoView({ behavior: "smooth", block: "start" });
  } else {
    renderOriginal(pp.final.original);
    $("#view-errades").scrollTo({ top: 0, behavior: "smooth" });
  }
}

/* ---------- selecting and annotating ---------- */

let pendingSel = null;

function tokOf(container, offset, isEnd) {
  // A boundary can sit inside a text node (normal drag) or between elements (triple click, keyboard).
  let node = container;
  if (node?.nodeType === 1 && !node.closest(".tok")) {
    node = node.childNodes[isEnd ? offset - 1 : offset] ?? node;
    if (node?.nodeType === 1 && !node.classList.contains("tok")) {
      node = isEnd ? node.querySelector(".tok:last-of-type") ?? node : node.querySelector(".tok") ?? node;
    }
  }
  const elNode = node?.nodeType === 3 ? node.parentElement : node;
  return elNode?.closest?.(".tok");
}

function onSelection() {
  const btn = $("#er-mark");
  if (!btn) return;
  if (E.resultat || !E.sol || E.busy) { btn.classList.add("hidden"); return; }
  const sel = getSelection();
  if (!sel || sel.isCollapsed || !sel.rangeCount) { btn.classList.add("hidden"); return; }
  const range = sel.getRangeAt(0);
  const paper = $("#er-paper");
  if (!paper.contains(range.commonAncestorContainer)) { btn.classList.add("hidden"); return; }

  let a = tokOf(range.startContainer, range.startOffset, false);
  let b = tokOf(range.endContainer, range.endOffset, true);
  const fragA = (a || range.startContainer.parentElement)?.closest?.(".frag");
  if (!fragA) { btn.classList.add("hidden"); return; }
  const toks = [...fragA.querySelectorAll(".tok")];
  // Only tokenized fragments take marks (in Pas a pas, the part under review).
  if (!toks.length) { btn.classList.add("hidden"); return; }
  a ??= toks[0];
  // A selection running into the next paragraph is clipped to the first one.
  if (!b || b.closest(".frag") !== fragA) b = toks[toks.length - 1];
  let i = toks.indexOf(a), j = toks.indexOf(b);
  if (i > j) [i, j] = [j, i];
  while (i <= j && toks[i].classList.contains("ws")) i++;
  while (j >= i && toks[j].classList.contains("ws")) j--;
  if (i > j) { btn.classList.add("hidden"); return; }

  pendingSel = { fragment: +fragA.dataset.frag, s16: +toks[i].dataset.s, e16: +toks[j].dataset.e };
  const rect = range.getBoundingClientRect();
  const wrap = $("#er-paper-wrap").getBoundingClientRect();
  btn.style.left = `${Math.max(8, Math.min(rect.left - wrap.left + rect.width / 2 - 80, wrap.width - 180))}px`;
  btn.style.top = `${rect.top - wrap.top - 46}px`;
  btn.classList.remove("hidden");
}

function crearAnotacio() {
  if (!pendingSel) return;
  const text = textFrag(pendingSel.fragment);
  const a = {
    id: `a${++E.seq}`,
    ...pendingSel,
    cita: text.slice(pendingSel.s16, pendingSel.e16),
    comentari: "",
  };
  E.anotacions.push(a);
  pendingSel = null;
  getSelection().removeAllRanges();
  $("#er-mark").classList.add("hidden");
  E.actiu = a.id;
  paintHighlights();
  renderRail();
  renderBar();
  $(`#er-rail [data-card="${a.id}"] textarea`)?.focus();
}

function esborrar(id) {
  E.anotacions = E.anotacions.filter((a) => a.id !== id);
  if (E.actiu === id) E.actiu = null;
  paintHighlights();
  renderRail();
  renderBar();
}

function activar(id) {
  E.actiu = id;
  paintHighlights();
  document.querySelectorAll("#er-rail .note").forEach((n) => n.classList.toggle("active", n.dataset.card === id));
}

/* ---------- toolbar ---------- */

function renderBar() {
  const bar = $("#er-bar");
  if (!E.sol) return bar.replaceChildren();
  if (perParts()) return renderBarParts();
  if (E.resultat) return renderScore();
  const n = E.sol.n_errors;
  const marcats = E.anotacions.length;
  const sense = E.anotacions.filter((a) => !a.comentari.trim()).length;
  const dots = el("div", { class: "er-dots", "aria-label": `${marcats} marcats de ${n} errors` },
    ...Array.from({ length: n }, (_, i) => el("span", { class: i < marcats ? "on" : "" })));
  const submit = el("button", { type: "button", class: "btn primary", text: "Envia la correcció" });
  submit.disabled = marcats === 0;
  submit.addEventListener("click", enviar);
  bar.replaceChildren(
    el("div", { class: "er-progress" }, dots,
      el("span", {}, el("strong", { text: `${marcats}` }), ` marcat${marcats === 1 ? "" : "s"} · hi ha `,
        el("strong", { text: `${n}` }), ` error${n > 1 ? "s" : ""} amagat${n > 1 ? "s" : ""}`),
      sense ? el("span", { class: "warn-text", text: ` · ${sense} sense explicació` }) : null),
    submit);
}

async function enviar() {
  if (E.busy || !E.sessionId) return;
  const req = E.req;
  const hash = location.hash;
  const bar = $("#er-bar");
  bar.replaceChildren(el("div", { class: "er-progress" }, el("span", { class: "spinner" }),
    el("span", { text: "Corregint les teves anotacions…" })));
  erBusy(true);
  try {
    const resultat = await api(`/api/errades/sessions/${E.sessionId}/correccio`, {
      method: "POST",
      body: JSON.stringify({ anotacions: payloadAnotacions() }),
    });
    if (erStale(req, hash)) return;
    E.resultat = resultat;
    E.actiu = null;
    paintHighlights();
    renderRail();
    renderBar();
    renderOriginal(resultat.original);
    $("#view-errades").scrollTo({ top: 0, behavior: "smooth" });
  } catch (err) {
    if (erStale(req, hash)) return;
    renderBar();
    bar.append(el("span", { class: "warn-text", text: err.message }));
  } finally {
    if (req === E.req) erBusy(false);
  }
}

function renderOriginal(orig) {
  // Theory: after the correction, the item as the notes state and prove it.
  const box = $("#er-original");
  if (!box || !orig) return;
  box.replaceChildren(el("h3", { text: "Compara amb els apunts" }), theoryCard(orig, true));
  box.classList.remove("hidden");
}

function renderScore() {
  const r = E.resultat;
  const again = el("button", { type: "button", class: "btn primary", text: E.font === "teoria" ? "Una altra versió" : "Una altra resolució" });
  again.addEventListener("click", unAltre);
  $("#er-bar").replaceChildren(
    el("div", { class: "er-score" }, scoreRing(r.nota),
      el("div", {},
        el("strong", { text: `Has trobat ${r.trobats} de ${r.total} error${r.total > 1 ? "s" : ""}` }),
        r.falsos_positius ? el("span", { class: "muted", text: ` · ${r.falsos_positius} marca${r.falsos_positius > 1 ? "des" : "da"} en passos correctes` }) : null,
        r.resum ? math(el("p", { class: "muted", text: r.resum })) : null)),
    again);
}

/* ---------- comment rail ---------- */

function quote(text) {
  return math(el("blockquote", { class: "note-quote", text }));
}

function renderRail() {
  const rail = $("#er-rail");
  if (!E.sol) return rail.replaceChildren();
  let cards;
  if (perParts() && !E.pp.actual) cards = [...E.pp.fets.values()].flatMap((f) => railResultats(f.r, f.anotacions));
  else cards = E.resultat ? railResultats() : railAnotacions();
  rail.replaceChildren(...cards);
  if (!cards.length) {
    rail.append(el("div", { class: "rail-empty" },
      el("span", { class: "rail-empty-icon", text: "✎" }),
      el("p", { text: perParts() && E.pp.actual
        ? `Selecciona el tros de la part ${E.pp.actual.part} que creguis que està malament i prem «Marca com a error».`
        : "Selecciona un tros del text que creguis que està malament i prem «Marca com a error»." })));
  }
  requestAnimationFrame(alignRail);
}

function railAnotacions() {
  return E.anotacions.map((a, k) => {
    const ta = el("textarea", { rows: "3", placeholder: "Per què està malament? Què hauria de dir?" });
    ta.value = a.comentari;
    ta.addEventListener("input", () => { a.comentari = ta.value; renderBar(); });
    ta.addEventListener("focus", () => activar(a.id));
    const del = el("button", { type: "button", class: "note-del", title: "Esborra", "aria-label": "Esborra l'anotació", text: "×" });
    del.addEventListener("click", () => esborrar(a.id));
    const card = el("div", { class: `note${E.actiu === a.id ? " active" : ""}`, "data-card": a.id, "data-frag": String(a.fragment) },
      el("div", { class: "note-head" }, el("span", { class: "note-tag", text: `Marca ${k + 1} · paràgraf ${a.fragment}` }), del),
      quote(a.cita), ta);
    card.addEventListener("mouseenter", () => activar(a.id));
    return card;
  });
}

function railResultats(r = E.resultat, anotacions = E.anotacions) {
  const cards = [];
  for (const [k, err] of r.errors.entries()) {
    const matches = r.anotacions.filter((a) => a.error === err.id);
    const best = matches.sort((x, y) => y.punts - x.punts)[0];
    const mine = best && anotacions.find((a) => a.id === best.id);
    const found = !!best;
    const card = el("div", { class: `note result ${found ? "found" : "missed"}`, "data-frag": String(err.fragment), "data-card": `err-${err.id}` });
    const status = found
      ? el("span", { class: `pill ${best.explicacio === "correcta" ? "ok" : "warn"}`,
          text: best.explicacio === "correcta" ? "Trobat i ben explicat" : best.explicacio === "parcial" ? "Trobat · explicació parcial" : "Trobat · falta el perquè" })
      : el("span", { class: "pill bad", text: "No trobat" });
    card.append(el("div", { class: "note-head" },
      el("span", { class: "note-tag", text: `${perParts() ? `Part ${r.part}` : `Error ${k + 1}`} · ${TIPUS_ERROR[err.tipus] || err.tipus}` }), status));

    if (found || revelat(err.id)) {
      card.append(quote(err.cita),
        math(el("p", { class: "note-text", text: err.explicacio })),
        el("div", { class: "note-fix" }, el("span", { text: "Correcció" }), math(el("p", { text: err.correccio }))));
      if (mine && mine.comentari.trim()) {
        card.append(el("div", { class: "note-student" },
          el("span", { text: "El teu comentari" }), math(el("p", { text: mine.comentari })),
          best.feedback ? math(el("p", { class: "note-feedback", text: best.feedback })) : null));
      } else if (best?.feedback) {
        card.append(math(el("p", { class: "note-feedback", text: best.feedback })));
      }
    } else {
      card.append(el("p", { class: "note-text muted", text: `És al paràgraf ${err.fragment}.` }));
      if (E.pistes.has(err.id)) card.append(math(el("p", { class: "note-hint", text: err.pista })));
      const actions = el("div", { class: "note-actions" });
      if (!E.pistes.has(err.id)) {
        const hint = el("button", { type: "button", class: "btn ghost small-btn", text: "Dona'm una pista" });
        hint.addEventListener("click", () => { E.pistes.add(err.id); renderRail(); });
        actions.append(hint);
      }
      const reveal = el("button", { type: "button", class: "btn ghost small-btn", text: "Mostra l'error" });
      reveal.addEventListener("click", () => { E.revelats.add(err.id); paintHighlights(); renderRail(); });
      actions.append(reveal);
      card.append(actions);
    }
    cards.push(card);
  }
  for (const a of r.anotacions.filter((x) => x.error === "cap")) {
    // A stored grading can carry ids that are not this page's marks (e.g. graded from another tab): show the
    // server's verdict without the local quote instead of failing.
    const mine = anotacions.find((x) => x.id === a.id);
    const card = el("div", { class: "note result false", "data-card": a.id },
      el("div", { class: "note-head" }, el("span", { class: "note-tag", text: mine ? `La teva marca · paràgraf ${mine.fragment}` : "Una marca teva" }),
        el("span", { class: "pill neutral", text: "Aquí no hi havia error" })),
      mine ? quote(mine.cita) : null,
      a.feedback ? math(el("p", { class: "note-feedback", text: a.feedback })) : null);
    if (mine) card.dataset.frag = String(mine.fragment);
    cards.push(card);
  }
  return cards;
}

function alignRail() {
  // Desktop: each card sits next to its paragraph, pushed down to avoid overlaps (like doc comments).
  const rail = $("#er-rail");
  const paper = $("#er-paper");
  if (!rail || !paper) return;
  const cards = [...rail.querySelectorAll(".note")];
  if (getComputedStyle(rail).position !== "relative" || window.innerWidth < 1000) {
    cards.forEach((c) => { c.style.top = ""; });
    rail.style.minHeight = "";
    return;
  }
  const base = paper.getBoundingClientRect().top;
  const items = cards.map((c) => {
    const ann = E.anotacions.find((a) => a.id === c.dataset.card);
    const target = (ann && paper.querySelector(`.tok[data-ann="${ann.id}"]`)) || paper.querySelector(`.frag[data-frag="${c.dataset.frag}"]`);
    return { c, want: target ? target.getBoundingClientRect().top - base - 8 : 0 };
  }).sort((x, y) => x.want - y.want);
  let y = 0;
  for (const it of items) {
    const top = Math.max(it.want, y);
    it.c.style.top = `${top}px`;
    y = top + it.c.offsetHeight + 12;
  }
  rail.style.minHeight = `${y}px`;
}

window.addEventListener("resize", () => requestAnimationFrame(alignRail));
