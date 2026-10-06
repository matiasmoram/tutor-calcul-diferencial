"use strict";

/* "Troba l'error": a document with hidden errors. Two activities share this view:
   - problema: a worked solution of an exercise ("resolució dolenta");
   - teoria: a result of the notes (statement + proof) with errors in the statement and in the proof.
   The student highlights spans on the document, comments why they're wrong, and submits for correction.
   Shares el(), math(), tex(), api(), statement(), crumbs(), show(), theoryCard() with app.js. */

const DIFICULTATS = [
  { id: "facil", label: "Fàcil", n: 1 },
  { id: "normal", label: "Normal", n: 2 },
  { id: "dificil", label: "Difícil", n: 3 },
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

const E = {
  font: "problema", llista: null, ex: null, item: null, disp: {}, dificultat: "normal", sessionId: null, sol: null,
  anotacions: [], actiu: null, resultat: null, revelats: new Set(), pistes: new Set(), seq: 0,
};

/* ---------- offsets: backend counts code points, JS strings count UTF-16 units ---------- */

const cpToU16 = (s, cp) => { let i = 0; for (let k = 0; k < cp && i < s.length; k++) i += s.codePointAt(i) > 0xffff ? 2 : 1; return i; };
const u16ToCp = (s, i) => Array.from(s.slice(0, i)).length;

/* ---------- choosing an activity ---------- */

function viewErradesInici() {
  show("errades");
  crumbs([["Inici", "#/"], ["Troba l'error", null]]);
  const card = (href, icon, title, text) => el("a", { class: "mode", href },
    el("span", { class: "mode-icon", text: icon }), el("h3", { text: title }), math(el("p", { text })),
    el("span", { class: "mode-cta", text: "Entrar →" }));
  $("#view-errades").replaceChildren(
    el("section", { class: "hero left" },
      el("h2", { text: "Troba l'error" }),
      el("p", { class: "muted", text: "Un document amb errors amagats, verificat per IA. Subratlla'ls sobre el text, explica per què estan malament i envia la correcció." })),
    el("div", { class: "modes two" },
      card("#/errades/teoria", "∀", "Teoremes i demostracions",
        "Un teorema, proposició, lema o corol·lari dels apunts amb errors: una hipòtesi que falta, una conclusió massa forta, un quantificador canviat, un pas de la demostració que no se segueix."),
      card("#/errades/problemes", "≠", "Resolucions de problemes",
        "La resolució d'un problema de la col·lecció, feta per un alumne no gaire fi: una desigualtat girada, un teorema aplicat sense les hipòtesis, un càlcul mal fet.")));
}

let erTeoria = null;

async function getErradesTeoria() {
  erTeoria ??= await api("/api/errades/teoria");
  return erTeoria;
}

function readyDots(disp) {
  return el("span", { class: "ready-dots", title: "Documents preparats per dificultat" },
    ...DIFICULTATS.map((d) => el("span", { class: disp?.[d.id] ? "on" : "", title: `${d.label}: ${disp?.[d.id] ? "a punt" : "es generarà"}` })));
}

async function viewErradesTeoriaLlista() {
  show("errades");
  crumbs([["Inici", "#/"], ["Troba l'error", "#/errades"], ["Teoremes", null]]);
  erTeoria = null;  // availability changes as documents are generated
  const data = await getErradesTeoria();
  $("#view-errades").replaceChildren(
    el("section", { class: "hero left" },
      el("div", { class: "eyebrow", text: "Troba l'error · Teoria" }),
      el("h2", { text: "Teoremes i demostracions amb errors" }),
      el("p", { class: "muted", text: "Tria un resultat dels apunts. El reescriurem amb errors a l'enunciat i a la demostració; tu els has de trobar. Els punts indiquen les dificultats que ja estan preparades (fàcil · normal · difícil)." })),
    el("div", { class: "teoria-temes" }, ...data.temes.filter((t) => t.items.length).map((t, i) => {
      const d = el("details", { class: "teoria-tema" },
        el("summary", {}, el("strong", { text: `Tema ${t.tema}` }), math(el("span", { text: ` · ${t.titol}` })),
          el("span", { class: "small muted", text: ` · ${t.items.length} resultats` })),
        el("ul", { class: "er-items" }, ...t.items.map((it) => el("li", {},
          el("a", { class: "er-item", href: `#/errades/teoria/${it.id}` },
            el("span", { class: "theory-label", text: it.etiqueta.replace(/ \(Tema \d\)$/, "") }),
            math(el("span", { class: "theory-name", text: it.nom || "" })),
            readyDots(it.disponibles))))));
      if (i === 0) d.open = true;
      return d;
    })));
}

/* ---------- entry points ---------- */

async function viewErrades(llistaId, exId) {
  show("errades");
  const l = await getLlista(llistaId);
  const ex = l.exercicis.find((e) => e.id === exId);
  if (!ex) throw new Error("Exercici desconegut");
  crumbs([["Inici", "#/"], ["Troba l'error", "#/errades"], ["Resolucions", "#/errades/problemes"],
    [l.etiqueta, `#/errades/${llistaId}`], [ex.etiqueta, null]]);
  const disp = await api("/api/errades/disponibles").catch(() => ({}));
  Object.assign(E, { font: "problema", llista: l, ex, item: null, disp: disp[ex.id] || {} });
  E.dificultat = triaDificultat(E.disp);
  renderShell();
  await carregar(false);
}

async function viewErradesTeoria(itemId) {
  show("errades");
  const data = await getErradesTeoria();
  const item = data.temes.flatMap((t) => t.items).find((it) => it.id === itemId);
  if (!item) throw new Error("Resultat dels apunts desconegut");
  crumbs([["Inici", "#/"], ["Troba l'error", "#/errades"], ["Teoremes", "#/errades/teoria"],
    [item.etiqueta.replace(/ \(Tema \d\)$/, ` · T${item.tema}`), null]]);
  Object.assign(E, { font: "teoria", llista: null, ex: null, item, disp: item.disponibles || {} });
  E.dificultat = triaDificultat(E.disp);
  renderShell();
  await carregar(false);
}

function triaDificultat(disp) {
  // Keep the student's choice when it is ready; otherwise open a ready one (no wait, no API call).
  if (disp[E.dificultat]) return E.dificultat;
  return ["normal", "facil", "dificil"].find((d) => disp[d]) || E.dificultat;
}

function renderShell() {
  const root = $("#view-errades");
  const teoria = E.font === "teoria";
  const chips = el("div", { class: "diff-chips", role: "radiogroup", "aria-label": "Dificultat" },
    ...DIFICULTATS.map((d) => {
      const b = el("button", { type: "button", class: `chip${d.id === E.dificultat ? " on" : ""}`, role: "radio",
        "aria-checked": String(d.id === E.dificultat), "data-dif": d.id,
        title: E.disp[d.id] ? "Preparat: s'obre a l'instant" : "Encara no n'hi ha cap de preparat: es generarà (cal l'API)" },
        el("span", { text: d.label }), el("small", { text: `${d.n} error${d.n > 1 ? "s" : ""}${E.disp[d.id] ? "" : " · nou"}` }));
      b.addEventListener("click", () => {
        if (E.dificultat === d.id) return;
        E.dificultat = d.id;
        root.querySelectorAll(".chip").forEach((c) => {
          c.classList.toggle("on", c.dataset.dif === d.id);
          c.setAttribute("aria-checked", String(c.dataset.dif === d.id));
        });
        carregar(false);
      });
      return b;
    }));
  const nova = el("button", { type: "button", class: "btn ghost small-btn", id: "er-nova", text: teoria ? "↻ Una altra versió" : "↻ Una altra resolució" });
  // With more than one ready document, "another" picks a different one; otherwise it generates a new one.
  nova.addEventListener("click", () => carregar((E.disp[E.dificultat] || 0) <= 1));

  const eyebrow = teoria
    ? `Troba l'error · Teoria · Tema ${E.item.tema}`
    : `Troba l'error · ${E.llista.etiqueta} · ${E.ex.etiqueta}`;
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
        el("h2", { text: teoria ? "Aquest enunciat i la seva demostració tenen errors. Troba'ls." : "Aquesta resolució té errors. Troba'ls." }),
        el("p", { class: "muted", text: "Selecciona amb el ratolí el tros que està malament, marca'l i explica per què. Quan acabis, envia la correcció." })),
      el("div", { class: "er-controls" }, chips, nova)),
    context,
    el("div", { class: "er-bar", id: "er-bar" }),
    el("div", { class: "er-workspace", id: "er-workspace" },
      el("div", { class: "er-paper-wrap", id: "er-paper-wrap" },
        el("article", { class: "er-paper", id: "er-paper" }),
        el("button", { type: "button", class: "er-mark hidden", id: "er-mark" }, el("span", { text: "✎" }), " Marca com a error")),
      el("aside", { class: "er-rail", id: "er-rail", "aria-label": "Comentaris" })),
    el("section", { class: "er-original hidden", id: "er-original" }));

  $("#er-mark").addEventListener("mousedown", (e) => e.preventDefault()); // keep the selection alive
  $("#er-mark").addEventListener("click", crearAnotacio);
  $("#er-paper").addEventListener("mouseup", () => setTimeout(onSelection, 0));
  $("#er-paper").addEventListener("keyup", (e) => { if (e.shiftKey) onSelection(); });
  document.addEventListener("selectionchange", () => {
    const sel = getSelection();
    if (!sel || sel.isCollapsed) $("#er-mark")?.classList.add("hidden");
  });
}

/* ---------- loading ---------- */

async function carregar(nova) {
  const anterior = E.sol?.id || null;
  Object.assign(E, { sessionId: null, sol: null, anotacions: [], actiu: null, resultat: null, revelats: new Set(), pistes: new Set() });
  const steps = LOADING_STEPS[E.font];
  const paper = $("#er-paper");
  paper.classList.add("loading");
  paper.replaceChildren(
    el("div", { class: "er-loading" },
      el("div", { class: "er-loading-step", id: "er-step", text: E.disp[E.dificultat] && !nova ? "Obrint el document…" : steps[0] }),
      ...[92, 78, 88, 64, 95, 70, 84, 58].map((w) => el("div", { class: "skeleton", style: `width:${w}%` }))));
  $("#er-rail").replaceChildren();
  $("#er-bar").replaceChildren();
  $("#er-original").classList.add("hidden");
  $("#er-nova").disabled = true;
  let k = 0;
  const ticker = setInterval(() => {
    k = Math.min(k + 1, steps.length - 1);
    const step = $("#er-step");
    if (step) step.textContent = steps[k];
  }, 9000);
  try {
    const font = E.font === "teoria" ? { teoria_id: E.item.id } : { exercici_id: E.ex.id };
    const data = await api("/api/errades/sessions", {
      method: "POST",
      body: JSON.stringify({ ...font, dificultat: E.dificultat, nova, excepte: anterior }),
    });
    E.sessionId = data.session_id;
    E.sol = data.solucio;
    if (data.generada_ara) E.disp[E.dificultat] = (E.disp[E.dificultat] || 0) + 1;
    renderPaper();
    renderBar();
    renderRail();
  } catch (err) {
    const ready = DIFICULTATS.filter((d) => E.disp[d.id]).map((d) => d.label);
    paper.replaceChildren(el("div", { class: "er-error" },
      el("strong", { text: "No s'ha pogut preparar el document" }), el("p", { class: "muted", text: err.message }),
      ready.length ? el("p", { class: "muted", text: `Hi ha documents preparats per a: ${ready.join(", ")}.` }) : null));
  } finally {
    clearInterval(ticker);
    paper.classList.remove("loading");
    $("#er-nova").disabled = false;
  }
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

function renderPaper() {
  const paper = $("#er-paper");
  const nEn = E.sol.n_enunciat || 0;
  const frags = E.sol.fragments.map((text, i) => {
    const p = el("p", { class: "frag", "data-frag": String(i + 1) },
      el("span", { class: "frag-num", "aria-hidden": "true", text: String(i + 1) }));
    const body = el("span", { class: "frag-body" });
    for (const t of tokenize(text)) {
      const span = el("span", { class: `tok${t.math ? " m" : ""}${t.ws ? " ws" : ""}`, "data-s": String(t.s), "data-e": String(t.e) });
      if (t.math) span.append(tex(t.t.slice(1, -1)));
      else span.textContent = t.t;
      body.append(span);
    }
    p.append(body);
    return p;
  });
  if (nEn) {
    // Theory: the statement first, then the proof (headings sit outside the fragments, so they can't be selected).
    frags.splice(nEn, 0, el("h4", { class: "er-sec", text: "Demostració" }));
    frags.unshift(el("h4", { class: "er-sec", text: "Enunciat" }));
  }
  paper.replaceChildren(...frags);
  paintHighlights();
}

function paintHighlights() {
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
  if (E.resultat) {
    for (const err of E.resultat.errors) {
      const text = E.sol.fragments[err.fragment - 1];
      const found = E.resultat.anotacions.some((a) => a.error === err.id);
      if (found || E.revelats.has(err.id)) {
        mark(err.fragment, cpToU16(text, err.inici), cpToU16(text, err.fi), `err-real ${found ? "err-found" : "err-missed"}`);
      }
    }
  }
  for (const a of E.anotacions) {
    const text = E.sol.fragments[a.fragment - 1];
    let cls = "hl";
    if (E.resultat) {
      const r = E.resultat.anotacions.find((x) => x.id === a.id);
      cls += r ? (r.error === "cap" ? " hl-wrong" : r.explicacio === "correcta" ? " hl-right" : " hl-partial") : "";
    }
    if (E.actiu === a.id) cls += " active";
    mark(a.fragment, a.s16, a.e16, cls, a.id);
  }
  paper.querySelectorAll(".tok[data-ann]").forEach((t) => {
    t.onclick = () => activar(t.dataset.ann);
  });
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
  if (!btn || E.resultat || !E.sol) return;
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
  const text = E.sol.fragments[pendingSel.fragment - 1];
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
  const bar = $("#er-bar");
  bar.replaceChildren(el("div", { class: "er-progress" }, el("span", { class: "spinner" }),
    el("span", { text: "Corregint les teves anotacions…" })));
  try {
    E.resultat = await api(`/api/errades/sessions/${E.sessionId}/correccio`, {
      method: "POST",
      body: JSON.stringify({
        anotacions: E.anotacions.map((a) => {
          const text = E.sol.fragments[a.fragment - 1];
          return { id: a.id, fragment: a.fragment, inici: u16ToCp(text, a.s16), fi: u16ToCp(text, a.e16), comentari: a.comentari };
        }),
      }),
    });
    E.actiu = null;
    paintHighlights();
    renderRail();
    renderBar();
    renderOriginal();
    $("#view-errades").scrollTo({ top: 0, behavior: "smooth" });
  } catch (err) {
    renderBar();
    bar.append(el("span", { class: "warn-text", text: err.message }));
  }
}

function renderOriginal() {
  // Theory: after the correction, the item as the notes state and prove it.
  const box = $("#er-original");
  const orig = E.resultat?.original;
  if (!box || !orig) return;
  box.replaceChildren(el("h3", { text: "Compara amb els apunts" }), theoryCard(orig, true));
  box.classList.remove("hidden");
}

function renderScore() {
  const r = E.resultat;
  const R = 26, C = 2 * Math.PI * R;
  const ring = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  ring.setAttribute("viewBox", "0 0 64 64");
  ring.setAttribute("class", "score-ring");
  ring.innerHTML = `<circle cx="32" cy="32" r="${R}" class="track"/>
    <circle cx="32" cy="32" r="${R}" class="value" stroke-dasharray="${(C * r.nota) / 100} ${C}" transform="rotate(-90 32 32)"/>
    <text x="32" y="37" text-anchor="middle">${r.nota}</text>`;
  const again = el("button", { type: "button", class: "btn primary", text: E.font === "teoria" ? "Una altra versió" : "Una altra resolució" });
  again.addEventListener("click", () => carregar((E.disp[E.dificultat] || 0) <= 1));
  $("#er-bar").replaceChildren(
    el("div", { class: "er-score" }, ring,
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
  const cards = E.resultat ? railResultats() : railAnotacions();
  rail.replaceChildren(...cards);
  if (!cards.length) {
    rail.append(el("div", { class: "rail-empty" },
      el("span", { class: "rail-empty-icon", text: "✎" }),
      el("p", { text: "Selecciona un tros del text que creguis que està malament i prem «Marca com a error»." })));
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

function railResultats() {
  const r = E.resultat;
  const cards = [];
  for (const [k, err] of r.errors.entries()) {
    const matches = r.anotacions.filter((a) => a.error === err.id);
    const best = matches.sort((x, y) => y.punts - x.punts)[0];
    const mine = best && E.anotacions.find((a) => a.id === best.id);
    const found = !!best;
    const card = el("div", { class: `note result ${found ? "found" : "missed"}`, "data-frag": String(err.fragment), "data-card": `err-${err.id}` });
    const status = found
      ? el("span", { class: `pill ${best.explicacio === "correcta" ? "ok" : "warn"}`,
          text: best.explicacio === "correcta" ? "Trobat i ben explicat" : best.explicacio === "parcial" ? "Trobat · explicació parcial" : "Trobat · falta el perquè" })
      : el("span", { class: "pill bad", text: "No trobat" });
    card.append(el("div", { class: "note-head" },
      el("span", { class: "note-tag", text: `Error ${k + 1} · ${TIPUS_ERROR[err.tipus] || err.tipus}` }), status));

    if (found || E.revelats.has(err.id)) {
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
    const mine = E.anotacions.find((x) => x.id === a.id);
    cards.push(el("div", { class: "note result false", "data-frag": String(mine.fragment), "data-card": a.id },
      el("div", { class: "note-head" }, el("span", { class: "note-tag", text: `La teva marca · paràgraf ${mine.fragment}` }),
        el("span", { class: "pill neutral", text: "Aquí no hi havia error" })),
      quote(mine.cita),
      a.feedback ? math(el("p", { class: "note-feedback", text: a.feedback })) : null));
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
