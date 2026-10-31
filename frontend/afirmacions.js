"use strict";

/* "Cert o fals": a quiz of statements about one tema (or centred on one result of the notes).
   The student decides true / false and justifies: a proof, or a counterexample. Statements are generated
   and verified server-side (blind solver + audit + sympy checks); grading is LLM + sympy + code.
   Shares el(), math(), api(), crumbs(), show(), theoryButton() and the difficulty, ready-dot, pipeline and score
   helpers with app.js. */

const CF_LOADING = [
  "Escrivint afirmacions i les seves resolucions…",
  "Comprovant els contraexemples amb sympy…",
  "Un segon model les resol a cegues, sense saber si són certes o falses…",
  "Un revisor comprova cada demostració i cada contraexemple…",
  "Substituint les afirmacions que no han passat la verificació…",
  "Gairebé a punt…",
];
const CF_JUST = {
  correcta: ["ok", "Justificació correcta"],
  parcial: ["warn", "Justificació parcial"],
  incorrecta: ["bad", "Justificació incorrecta"],
  absent: ["neutral", "Sense justificació"],
};

const CF = {
  fonts: null, font: null, item: null, dificultat: "normal", disp: {}, sessionId: null, q: null,
  respostes: {}, pistes: {}, resultat: null,
  req: 0, busy: false,  // req numbers each quiz load: only the latest one may touch the page
};

async function getCfFonts(fresh = false) {
  if (fresh || !CF.fonts) CF.fonts = await api("/api/afirmacions/fonts");
  return CF.fonts;
}

function cfDots(disp) {
  return readyDots(disp, "Qüestionaris preparats per dificultat");
}

const cfTeQuestionaris = (disp) => Object.values(disp || {}).some(Boolean);

/* ---------- choosing a tema ---------- */

async function viewAfirmacionsInici() {
  show("afirmacions");
  crumbs([["Inici", "#/"], ["Cert o fals", null]]);
  $("#view-afirmacions").replaceChildren(carregant());
  const data = await getCfFonts(true);
  // Open the first tema with a ready quiz, so the student lands where something opens without waiting.
  const obert = Math.max(0, data.temes.findIndex((t) => cfTeQuestionaris(t.disponibles)
    || t.items.some((it) => cfTeQuestionaris(it.disponibles))));
  $("#view-afirmacions").replaceChildren(
    el("section", { class: "hero left" },
      el("div", { class: "eyebrow", text: "Cert o fals" }),
      el("h2", { text: "Demostra-ho o troba'n un contraexemple" }),
      math(el("p", { class: "muted", text: "Afirmacions sobre un tema que semblen certes i potser no ho són: límits iterats que coincideixen sense límit doble, continuïtat en cada variable que no és continuïtat, un teorema sense una hipòtesi. Decideix, i justifica-ho: una demostració o un contraexemple." }))),
    el("ol", { class: "pipeline cf-pipeline" },
      pipelineStage(1, "Generació", "Un model escriu les afirmacions amb la resolució, les idees clau i els càlculs del contraexemple.", "LLM · sortida estructurada", "llm"),
      pipelineStage(2, "Comprovació", "Cada càlcul del contraexemple (límits, derivades) es comprova amb sympy. Si un falla, l'afirmació es descarta.", "CAS · sympy", "rule"),
      pipelineStage(3, "Verificació", "Un segon model les resol a cegues i un tercer audita les solucions. Només queden les que tots dos accepten.", "2 LLM independents", "llm"),
      pipelineStage(4, "Correcció", "El veredicte el corregeix el codi; la justificació, un model amb la rúbrica, i els teus càlculs, sympy.", "LLM + CAS + regles", "rule")),
    el("div", { class: "teoria-temes" }, ...data.temes.map((t, i) => {
      const d = el("details", { class: "teoria-tema" },
        el("summary", {}, el("strong", { text: `Tema ${t.tema}` }), math(el("span", { text: ` · ${t.titol}` }))),
        el("a", { class: "er-item cf-whole", href: `#/afirmacions/${t.id}` },
          el("span", { class: "theory-label", text: "Tot el tema" }),
          el("span", { class: "theory-name", text: "Afirmacions variades sobre tots els conceptes del tema" }),
          cfDots(t.disponibles)),
        el("p", { class: "small muted cf-sub", text: "O centra-ho en un resultat: recíprocs, hipòtesis que falten, conclusions massa fortes." }),
        el("ul", { class: "er-items" }, ...t.items.map((it) => el("li", {},
          el("a", { class: "er-item", href: `#/afirmacions/${it.id}` },
            el("span", { class: "theory-label", text: etiquetaCurta(it.etiqueta) }),
            math(el("span", { class: "theory-name", text: it.nom || "" })),
            cfDots(it.disponibles))))));
      if (i === obert) d.open = true;
      return d;
    })));
}

/* ---------- a quiz ---------- */

async function viewAfirmacions(fontId) {
  show("afirmacions");
  $("#view-afirmacions").replaceChildren(carregant());
  const data = await getCfFonts();
  const tema = data.temes.find((t) => t.id === fontId);
  const item = tema ? null : data.temes.flatMap((t) => t.items).find((it) => it.id === fontId);
  if (!tema && !item) throw new Error("Tema o resultat desconegut");
  const temaN = tema ? tema.tema : item.tema;
  crumbs([["Inici", "#/"], ["Cert o fals", "#/afirmacions"],
    [tema ? `Tema ${temaN}` : etiquetaCurta(item.etiqueta, ` · T${temaN}`), null]]);
  Object.assign(CF, { font: fontId, item, tema: temaN, disp: (tema || item).disponibles || {}, mida: data.mida });
  CF.dificultat = triaDificultat(CF.disp, CF.dificultat);
  cfShell(tema);
  await cfCarregar(false);
}

function cfShell(tema) {
  const root = $("#view-afirmacions");
  const chips = difficultyChips({
    current: CF.dificultat,
    disp: CF.disp,
    sub: (d) => `${CF.mida[d.id]} afirmacions`,
    isBusy: () => CF.busy,
    onPick: (id) => { CF.dificultat = id; cfCarregar(false); },
  });
  const nova = el("button", { type: "button", class: "btn ghost small-btn", id: "cf-nova", text: "↻ Un altre qüestionari" });
  nova.addEventListener("click", cfUnAltre);
  root.replaceChildren(
    el("header", { class: "er-head" },
      el("div", { class: "er-title" },
        el("div", { class: "eyebrow", text: `Cert o fals · Tema ${CF.tema}` }),
        el("h2", {}, math(el("span", { text: tema ? `Tema ${CF.tema}: ${tema.titol}`
          : CF.item.nom ? `${etiquetaCurta(CF.item.etiqueta)} — ${CF.item.nom}` : etiquetaCurta(CF.item.etiqueta) }))),
        el("p", { class: "muted", text: "Per a cada afirmació: és certa o falsa? Si és certa, demostra-la; si és falsa, dona un contraexemple i comprova que funciona. Fórmules entre $...$." })),
      el("div", { class: "er-controls" }, chips, nova)),
    el("div", { class: "er-bar", id: "cf-bar" }),
    el("div", { class: "cf-list", id: "cf-list" }));
}

function cfDraftKey() { return `cf:${CF.q?.id}`; }
function cfSaveDraft() {
  try { localStorage.setItem(cfDraftKey(), JSON.stringify(CF.respostes)); } catch { /* storage unavailable */ }
}
function cfLoadDraft() {
  try { return JSON.parse(localStorage.getItem(cfDraftKey()) || "{}") || {}; } catch { return {}; }
}

function cfBusy(on) {
  // While a quiz loads or a correction runs: no other paid call (difficulty, another quiz, hints) can be fired.
  CF.busy = on;
  document.querySelectorAll("#view-afirmacions .er-controls button, #cf-list .note-actions button").forEach((b) => { b.disabled = on; });
}

function cfStale(req, hash) {
  // A response that is not for the latest load, or arrives after the student left this page, is dropped.
  return req !== CF.req || location.hash !== hash;
}

function cfUnAltre() {
  // With more than one ready quiz, "another" picks a different one (no API cost);
  // otherwise generating a new one needs an explicit click.
  if ((CF.disp[CF.dificultat] || 0) > 1) cfCarregar(false);
  else cfOferirGenerar(true);
}

function cfOferirGenerar(altre = false) {
  // Generating a quiz is a paid, minutes-long call: it only starts on an explicit click.
  CF.req++;  // a load still in flight for another difficulty must not replace this
  cfBusy(false);
  Object.assign(CF, { sessionId: null, q: null, respostes: {}, pistes: {}, resultat: null });
  $("#cf-bar").replaceChildren();
  const ready = DIFICULTATS.filter((d) => CF.disp[d.id]).map((d) => d.label);
  const gen = el("button", { type: "button", class: "btn primary", text: "Genera'n un de nou (pot trigar uns minuts)" });
  gen.addEventListener("click", () => cfCarregar(true));
  $("#cf-list").replaceChildren(el("div", { class: "er-paper er-generate" },
    el("strong", { text: altre ? "No n'hi ha cap altre de preparat en aquesta dificultat." : "Encara no hi ha cap qüestionari preparat en aquesta dificultat." }),
    POT_GENERAR ? el("p", { class: "muted", text: "Se'n pot generar un de nou: un model escriu les afirmacions, sympy en comprova els càlculs i dos models més les verifiquen." }) : null,
    ready.length ? el("p", { class: "muted", text: `Hi ha qüestionaris preparats per a: ${ready.join(", ")}.` }) : null,
    POT_GENERAR ? gen : el("p", { class: "muted", text: "Prova una altra dificultat, o demana al professorat que en prepari un." })));
}

async function cfCarregar(nova) {
  // nova=false only opens a ready quiz; with none ready, the student chooses whether to generate one.
  if (!nova && !CF.disp[CF.dificultat]) return cfOferirGenerar();
  const req = ++CF.req;
  const hash = location.hash;
  const anterior = CF.q?.id || null;
  Object.assign(CF, { sessionId: null, q: null, respostes: {}, pistes: {}, resultat: null });
  const list = $("#cf-list");
  const ready = !nova;
  list.replaceChildren(el("div", { class: "er-paper cf-loading" },
    el("div", { class: "er-loading" },
      el("div", { class: "er-loading-step", id: "cf-step", text: ready ? "Obrint el qüestionari…" : CF_LOADING[0] }),
      ...[92, 78, 88, 64, 95, 70].map((w) => el("div", { class: "skeleton", style: `width:${w}%` })),
      ready ? null : el("p", { class: "small muted", text: "Generar i verificar un qüestionari nou pot trigar uns minuts." }))));
  $("#cf-bar").replaceChildren();
  cfBusy(true);
  let k = 0;
  const ticker = setInterval(() => {
    k = Math.min(k + 1, CF_LOADING.length - 1);
    const s = $("#cf-step");
    if (s && !ready) s.textContent = CF_LOADING[k];
  }, 20000);
  try {
    const data = await api("/api/afirmacions/sessions", {
      method: "POST",
      body: JSON.stringify({ font: CF.font, dificultat: CF.dificultat, nova, excepte: anterior }),
    });
    if (cfStale(req, hash)) return;
    CF.sessionId = data.session_id;
    CF.q = data.questionari;
    if (data.generat_ara) CF.disp[CF.dificultat] = (CF.disp[CF.dificultat] || 0) + 1;
    CF.respostes = cfLoadDraft();
    cfRender();
  } catch (err) {
    if (cfStale(req, hash)) return;
    // 403/409: the server refuses to generate (not allowed, or one already being generated): its message, as is.
    const refusal = err.status === 403 || err.status === 409;
    list.replaceChildren(el("div", { class: "er-paper er-error" },
      el("strong", { text: refusal ? err.message : "No s'ha pogut preparar el qüestionari" }),
      refusal ? null : el("p", { class: "muted", text: err.message })));
  } finally {
    clearInterval(ticker);
    if (req === CF.req) cfBusy(false);
  }
}

function cfResposta(id) {
  CF.respostes[id] ??= { veredicte: "", justificacio: "" };
  return CF.respostes[id];
}

function cfRender() {
  $("#cf-list").replaceChildren(...CF.q.afirmacions.map((a, i) => cfCard(a, i)));
  cfBar();
}

function cfCard(a, i) {
  const r = cfResposta(a.id);
  const res = CF.resultat?.afirmacions.find((x) => x.id === a.id);
  const card = el("article", { class: `cf-card${res ? (res.encert ? " right" : " wrong") : ""}`, id: `cf-${a.id}` });
  card.append(el("div", { class: "cf-card-head" },
    el("span", { class: "cf-num", text: String(i + 1) }),
    el("span", { class: "note-tag", text: a.concepte }),
    res ? el("span", { class: "cf-points", text: `${Math.round(res.punts * 100)} / 100` }) : null));
  card.append(math(el("div", { class: "cf-statement", text: a.enunciat })));

  const verdict = el("div", { class: "cf-verdict", role: "radiogroup", "aria-label": "Veredicte" },
    ...[["cert", "Cert"], ["fals", "Fals"]].map(([v, label]) => {
      const b = el("button", { type: "button", class: `cf-v ${v}${r.veredicte === v ? " on" : ""}`, role: "radio",
        "aria-checked": String(r.veredicte === v), text: label });
      if (res) b.disabled = true;
      else b.addEventListener("click", () => {
        r.veredicte = r.veredicte === v ? "" : v;
        cfSaveDraft();
        card.replaceWith(cfCard(a, i));
        cfBar();
      });
      return b;
    }));
  card.append(verdict);

  if (!res) {
    const ta = el("textarea", { rows: "4", placeholder: r.veredicte === "fals"
      ? "Contraexemple: quina funció (o conjunt), i comprova que compleix les hipòtesis però no la conclusió."
      : r.veredicte === "cert" ? "Demostració: per què és certa? Cita els resultats que facis servir."
      : "Tria primer cert o fals. Després justifica-ho aquí (fórmules entre $...$)." });
    ta.value = r.justificacio;
    const preview = el("div", { class: "cf-preview muted" });
    let t = null;
    const renderPreview = () => {
      preview.textContent = ta.value.includes("$") ? ta.value : "";
      math(preview);
    };
    ta.addEventListener("input", () => {
      r.justificacio = ta.value;
      cfSaveDraft();
      cfBar();
      clearTimeout(t);
      t = setTimeout(renderPreview, 350);
    });
    renderPreview();
    card.append(ta, preview);
    const actions = el("div", { class: "note-actions" });
    if (CF.pistes[a.id]) {
      card.append(math(el("p", { class: "note-hint", text: CF.pistes[a.id] })));
    } else {
      const hint = el("button", { type: "button", class: "btn ghost small-btn", text: "Dona'm una pista (−15%)" });
      if (CF.busy) hint.disabled = true;
      hint.addEventListener("click", async () => {
        if (CF.busy) return;
        const sid = CF.sessionId;
        hint.disabled = true;
        try {
          const p = await api(`/api/afirmacions/sessions/${sid}/pista/${a.id}`, { method: "POST" });
          if (CF.sessionId !== sid || CF.resultat) return;  // another quiz, or already corrected: the hint is late
          CF.pistes[a.id] = p.pista;
          card.replaceWith(cfCard(a, i));
        } catch (err) {
          if (CF.sessionId !== sid) return;
          hint.disabled = CF.busy;
          hint.textContent = err.message;
        }
      });
      actions.append(hint);
    }
    card.append(actions);
    return card;
  }

  // After the correction.
  const [cls, label] = CF_JUST[res.justificacio] || CF_JUST.absent;
  card.append(el("div", { class: "cf-pills" },
    el("span", { class: `pill ${res.encert ? "ok" : "bad"}`,
      text: res.resposta ? `${res.encert ? "Encertat" : "No"}: és ${res.veredicte === "cert" ? "certa" : "falsa"}` : `Sense resposta: és ${res.veredicte === "cert" ? "certa" : "falsa"}` }),
    res.resposta ? el("span", { class: `pill ${cls}`, text: label }) : null,
    res.pista_usada ? el("span", { class: "pill neutral", text: "Pista usada" }) : null));
  if (r.justificacio.trim()) {
    card.append(el("div", { class: "note-student" }, el("span", { text: "La teva justificació" }), math(el("p", { text: r.justificacio }))));
  }
  if (res.feedback) card.append(math(el("p", { class: "note-feedback", text: res.feedback })));
  if (res.nota_cas) card.append(el("p", { class: "note-hint", text: res.nota_cas }));
  if (res.comprovacions_alumne?.length) card.append(cfChecks("Els teus càlculs, comprovats amb sympy", res.comprovacions_alumne));

  const s = res.solucio;
  const sol = el("details", { class: "cf-solution" }, el("summary", { text: "Resolució de referència" }));
  if (s.contraexemple) sol.append(el("div", { class: "note-fix" }, el("span", { text: "Contraexemple" }), math(el("p", { text: s.contraexemple }))));
  sol.append(math(el("p", { class: "cf-res", text: s.resolucio })));
  sol.append(el("div", { class: "cf-ideas" }, el("span", { class: "note-tag", text: "Idees clau" }),
    el("ul", {}, ...s.idees_clau.map((t) => math(el("li", { text: t }))))));
  if (s.comprovacions?.length) sol.append(cfChecks("Contraexemple verificat amb sympy", s.comprovacions));
  const items = (s.teoria || []).map((id) => CF.resultat.teoria?.[id]).filter(Boolean);
  if (items.length) sol.append(theoryButton(`Teoria (${items.length})`, "Resultats dels apunts que fa servir", items));
  if (!res.encert) sol.open = true;
  card.append(sol);
  return card;
}

function cfChecks(title, checks) {
  const icon = { ok: "✓", falla: "✗", indeterminat: "?" };
  return el("div", { class: "cf-checks" }, el("span", { class: "note-tag", text: title }),
    el("ul", {}, ...checks.map((c) => el("li", { class: `cf-check ${c.estat}` },
      el("span", { class: "cf-check-icon", text: icon[c.estat] || "?" }),
      el("span", {}, el("span", { text: c.descripcio || c.tipus }), " ",
        el("code", { text: c.tipus === "igualtat" ? `${c.expressio} = ${c.valor}`
          : c.tipus === "no_limit" ? `lim ${c.variable}→${c.punt} ${c.expressio} no existeix`
          : `lim ${c.variable}→${c.punt} ${c.expressio} = ${c.valor}` }),
        c.estat === "falla" && c.calculat ? el("span", { class: "muted", text: ` (sympy: ${c.calculat})` }) : null)))));
}

function cfBar() {
  const bar = $("#cf-bar");
  if (!CF.q) return bar.replaceChildren();
  if (CF.resultat) return cfScore();
  const n = CF.q.afirmacions.length;
  const fets = CF.q.afirmacions.filter((a) => cfResposta(a.id).veredicte).length;
  const sense = CF.q.afirmacions.filter((a) => cfResposta(a.id).veredicte && !cfResposta(a.id).justificacio.trim()).length;
  const submit = el("button", { type: "button", class: "btn primary", text: "Envia les respostes" });
  submit.disabled = fets === 0;
  submit.addEventListener("click", cfEnviar);
  bar.replaceChildren(
    el("div", { class: "er-progress" },
      el("div", { class: "er-dots" }, ...CF.q.afirmacions.map((a) =>
        el("span", { class: cfResposta(a.id).veredicte ? "on" : "", title: a.concepte }))),
      el("span", {}, el("strong", { text: String(fets) }), ` de ${n} contestades`),
      sense ? el("span", { class: "warn-text", text: ` · ${sense} sense justificar` }) : null),
    submit);
}

async function cfEnviar() {
  if (CF.busy || !CF.sessionId) return;
  const req = CF.req;
  const hash = location.hash;
  const bar = $("#cf-bar");
  bar.replaceChildren(el("div", { class: "er-progress" }, el("span", { class: "spinner" }),
    el("span", { text: "Corregint: el model valora els arguments i sympy comprova els teus càlculs…" })));
  cfBusy(true);
  try {
    const resultat = await api(`/api/afirmacions/sessions/${CF.sessionId}/correccio`, {
      method: "POST",
      body: JSON.stringify({ respostes: CF.q.afirmacions.map((a) => ({ id: a.id, ...cfResposta(a.id) })) }),
    });
    if (cfStale(req, hash)) return;
    CF.resultat = resultat;
    try { localStorage.removeItem(cfDraftKey()); } catch { /* storage unavailable */ }
    cfRender();
    $("#view-afirmacions").scrollTo({ top: 0, behavior: "smooth" });
    window.scrollTo({ top: 0, behavior: "smooth" });
  } catch (err) {
    if (cfStale(req, hash)) return;
    cfBar();
    bar.append(el("span", { class: "warn-text", text: err.message }));
  } finally {
    if (req === CF.req) cfBusy(false);
  }
}

function cfScore() {
  const r = CF.resultat;
  const again = el("button", { type: "button", class: "btn primary", text: "Un altre qüestionari" });
  again.addEventListener("click", cfUnAltre);
  $("#cf-bar").replaceChildren(
    el("div", { class: "er-score" }, scoreRing(r.nota),
      el("div", {},
        el("strong", { text: `${r.encerts} de ${r.total} veredictes encertats` }),
        r.resum ? math(el("p", { class: "muted", text: r.resum })) : null)),
    again);
}
