# Pla d'implementació — tutor per a tots els problemes + teoria del curs

Estat a 2026-10-06. Aquest fitxer és el punt de represa: llegeix-lo sencer abans de continuar.

## Objectiu

1. El tutor socràtic (`#/exercicis`) cobreix **tots** els problemes de `sources/Problemes/_Problemes Temes_1-6.pdf`
   (128 problemes, **328 exercicis** comptant apartats), amb fitxes de solució ocultes escrites offline.
2. Cada exercici porta la **teoria del curs** que necessita (ítems dels apunts `sources/Teoria/*.pdf`), i el tutor la
   **cita** («pel Teorema 12 del Tema 3»), amb l'enunciat de l'ítem desplegable a la UI.
3. Cost per torn controlat (vegeu "Tokens") i mesurat.

Decisions preses amb en Matías:
- Fitxes **offline**, escrites per agents Claude (no generació en temps d'execució).
- Les llistes antigues (`limits_4.yaml`, `teoria_t3.yaml`, numeració Sado-Rivero) es **substitueixen** per Tema 1…6
  del PDF nou. Es reaprofiten les fitxes antigues on el problema és el mateix (Llista 4 = Tema 2 problema 4).

Decisió de format (token-wise): **no** s'envien PDFs al model. La teoria es transcriu una vegada a YAML
(Markdown + LaTeX), partida en ítems numerats (`T3.12` = ítem 12 del Tema 3, comptador compartit dels apunts), i
cada fitxa cita els ítems que usa. Per torn només viatgen 2–6 ítems (~0,5–1,5k tokens) en lloc d'un tema sencer
(~15–20k) o d'un PDF (~1,5–3k tokens per pàgina).

## Fet

### Fase 1 — Transcripció (FET)
- `backend/teoria/tema1.yaml` … `tema6.yaml`: 232 ítems (def/teo/prop/lema/corol/obs/exemple/text), amb `id`,
  `tipus`, `num`, `resum` (número del requadre verd), `seccio`, `pagina`, `nom`, `enunciat`, `demostracio`,
  `problemes` (problemes de la col·lecció que l'ítem cita). ~282k caràcters en total.
- `work/enunciats/tema1.yaml` … `tema6.yaml`: enunciats de tots els problemes (preàmbul + apartats), transcrits de
  les imatges (la capa de text del PDF de problemes té els símbols matemàtics corromputs).
- Dubtes de transcripció reportats pels agents (cal mirar-los contra el PDF):
  - T2 4(e): llegit com `e^{x(y-1)-x-1}/(x^2+y^2)`; la fitxa antiga deia `e^{x(y-1)}-x-1`. **Comprovar.**
  - T3 2 (exponent `(\log x)(\arctan(\sin(\cos xy)))`), T3 13 (agrupació de l'arrel).
  - T4 24 (equacions en lletra petita), T4 16(c) (matriu).
  - T6 1(c) "passi per $(3,-1.0)$" (probablement $(3,-1,0)$), T6 12 i 14 (polinomis).
  - T1: `resum: 24` per a un requadre "24,25"; T2 Def. 6 té `resum: "40,41"` (string; el model ho admet).

### Fase 2 — Backend (FET)
- `backend/tutor/teoria.py` (nou): `ItemTeoria`, `load_teoria()`, `parse_ref()` (`"T3.12"` o `"T3.12+dem"` = amb
  demostració), `index_tema()`; `ItemTeoria.render()`, `.etiqueta` ("Teorema 12 (Tema 3)"), `.public()`.
- `backend/tutor/fitxes.py` (reescrit): format per tema `llista:` + `problemes:` → `exercicis:` (un per apartat).
  Camps nous a `Exercici`: `tema`, `problema`, `apartat`, `tipus` (calcul|teoric), `font`, `preambul`,
  `teoria` (fons, visible des del primer torn), `teoria_reservada` (ítems que resolen l'exercici: mai al redactor).
  `Pas.teoria` (resultats que usa el pas). `Exercici.reserved_ids()` reserva automàticament els ítems dels apunts
  que citen aquest problema. `load_llistes(dir, teoria=...)` valida que les refs existeixin. `Llista.problemes`
  agrupa per problema; `tipus` admet `mixt`.
- `backend/tutor/llm.py`: paràmetre `context=` (prefix estàtic per exercici) a `structured()` per a **prompt
  caching**: Anthropic = bloc amb `cache_control: ephemeral`; OpenAI/Gemini = prefix al començament (cache
  automàtica de prefixos). `CallMeta.cached_tokens` per a les tres APIs; `input_tokens` inclou els cached.
- `backend/tutor/schemas.py`: `Diagnosi.teoria_pregunta` (ítems que responen una pregunta conceptual, enum tancat),
  `Resposta.referencies` (enum = ítems permesos aquest torn), infracció `cita_teoria_incorrecta`;
  `diagnosi_schema(ex, teoria_ids)`, `resposta_schema(teoria_ids)`, `normalize_diagnosi(d, ex, teoria_ids)`.
  Sense `maxItems` (no tots els proveïdors l'accepten); límits aplicats en codi.
- `backend/tutor/politica.py`: `Pla.teoria_extra`; `explicar_concepte` es basa en la teoria; nova
  `allowed_theory(ex, pla, completats, teoria)`: teoria de l'exercici + passos completats + pas objectiu només des de
  nivell de pista 2 (anomenar un teorema = anomenar l'estratègia) + `teoria_extra`; tot a `tancar`; mai reservats.
- `backend/tutor/prompts.py`: regles de teoria a DIAGNOSI/RESPOSTA/GUARDIA; `diagnosi_context()` i
  `guardia_context()` (estàtics: fitxa + teoria de l'exercici + índex del tema) separats de `diagnosi_user()` /
  `guardia_user()` (dinàmics); `resposta_user(..., teoria=)`; `teoria_exercici()`, `diagnosi_teoria_ids()`.
  **Signatura canviada**: `guardia_user(pla, contingut, historial, missatge, teoria, referencies)` (ja no rep `ex`).
- `scripts/check_fitxes.py` (nou): valida estructura, ids `t3-5`/`t2-4c`, refs de teoria, regex de fuites
  (cada pas: alguna regex casa amb el seu `detall`; cap casa amb `objectiu`/`idea`; el resultat no es filtra a
  pistes ni preguntes), `$` balancejats, ≥2 passos, ≥2 errors, ≥1 ref de teoria.
  Ús: `.venv\Scripts\python.exe scripts\check_fitxes.py [fitxer --tema N]`.
- `work/SPEC_wave1.md` (transcripció), `work/SPEC_wave2.md` (escriptura de fitxes), `work/fitxes/EXEMPLE_t2-4c.yaml`
  (exemple validat del format nou).

## Pendent

### Fase 3 — Fitxes (FET)
328 exercicis a 22 trossos (work/fitxes/), tots passen check_fitxes.

### Fase 4 — Revisió de fitxes (FET: 22/22 trossos revisats; muntat a backend/exercicis/, 1023 tests passen)
Errates trobades als APUNTS (no a la transcripció; per comunicar al professorat):
- T2.26 (Definició 26, Lipschitz, pàg. 14): diu $d'(f(x),f(y)) < C\,d(x,y)$ amb desigualtat estricta, que falla per $x=y$; hauria de ser $\le$.
Errates a la col·lecció de problemes: T2 4(e) (exponent $x(y-1)-x-1$), T2 7(a) ($h\to0^+$ per $r\to0^+$), T6 1(c) ($(3,-1.0)$).
- Un agent revisor per tema (Opus): comprova matemàtica de cada `resultat`/`detall`, que les refs de teoria
  diguin el que el pas els fa dir (hipòtesis!), i que `objectiu`/`idea` no regalin el pas. Corregeix in situ.
- Resoldre els dubtes de transcripció de la Fase 1 contra el PDF.

### Fase 5 — Muntatge (FET; tornar a executar merge_fitxes.py quan arribin trossos nous)
- Script `scripts/merge_fitxes.py`: `work/fitxes/temaN_p*.yaml` → `backend/exercicis/temaN.yaml` amb capçalera
  `llista: {id: tema-N, etiqueta: "Tema N", titol: <títol del tema>, tema: N, tipus: mixt, format: text}`,
  problemes ordenats per número. Esborrar `limits_4.yaml` i `teoria_t3.yaml`.
- Caché de "Troba l'error" (`backend/generats/errades/<id>/`): reanomenar `4a`→`t2-4a`, `4c`→`t2-4c`,
  `4e`→`t2-4e` (i l'`exercici` dins de cada JSON); `t3-*` només si l'enunciat nou és el mateix; si no, esborrar.

### Fase 6 — Cablejat restant del backend (FET; 641 tests passen)
- `pipeline.py`: `Tutor(llm, teoria=None)` (carrega `load_teoria()` si cal); diagnosi amb
  `context=prompts.diagnosi_context(ex, teoria)`, `diagnosi_schema(ex, ids)`, `normalize_diagnosi(..., ids)`;
  `allowed_theory()` → `resposta_user(..., teoria=items)` + `resposta_schema([ids])`; filtrar `referencies` a ids
  permesos; guardià amb `context=prompts.guardia_context(ex, teoria)` i la nova `guardia_user`; la resposta del
  torn retorna `referencies: [item.public()]` (buit si fallback); traça amb `teoria_permesa` (ids).
- `errades.py`: passar `context=` amb fitxa + teoria (la generació i la verificació poden citar teoria).
- `app.py`: `load_llistes(teoria=load_teoria())` a l'arrencada (falla si hi ha refs trencades);
  `/api/llistes/{id}` retorna `problemes` (agrupació); `POST /api/sessions` retorna `teoria` (ítems de fons no
  reservats) i, per al panell del professor, totes les refs amb marca `reservada`; `GET /api/teoria/{id}`.
- `tests/test_harness.py`: ids nous (`4c`→`t2-4c`, `t3-6`→ el que toqui), `ScriptedLLM.structured(..., context=None)`,
  tests nous: refs existents; `allowed_theory` no dona teoria del pas a nivell 1 i sí a nivell 2; reservats mai al
  redactor; `referencies` fora de llista es descarten; `check_fitxes` a 0 per a totes les llistes;
  el prefix `context` és idèntic entre torns (cache).

### Fase 7 — Frontend (FET; verificat amb Playwright: llista agrupada, teoria de referència, panell)
- Vista de llista agrupada per problema (capçalera "Problema N" + preàmbul + apartats); barra lateral compacta.
- Sota l'enunciat: "Teoria de referència" plegable (ítems de fons).
- Missatges del tutor: xips de referència ("Teorema 12 · Tema 3 — nom") desplegables amb l'enunciat (KaTeX) i pàgina.
- Panell del professor: teoria permesa del torn, refs de la fitxa (reservades marcades), tokens `cached`.
- `TIPUS` amb `mixt`; pujar `?v=` de `app.js`/`style.css`.
- Verificar amb Playwright (com abans: `.playwright-mcp/`).

### Fase 8 — Tokens i cost (script FET: PYTHONPATH=work/pylib .venv/Scripts/python.exe scripts/token_budget.py)
Mesura (201 exercicis, 6 torns, 0,3 reescriptures/torn): diagnosi 4,6k entrada, redacció 1,9k, guardià 3,8k;
12,1k entrada/torn (p90 16k), ~73k entrada/sessió; 50% de l'entrada és prefix cacheable. Sortida ~1k/torn
(amb 600 tokens de raonament suposats a la diagnosi). Teoria per exercici: mitjana 963 tokens, p90 1,7k.
- `scripts/token_budget.py`: construeix els prompts reals de cada etapa per a cada exercici amb una conversa simulada
  de 6 torns i compta tokens (tiktoken `o200k_base` per a OpenAI; instal·lar a `work/pylib`). Sortida: mitjana /
  p90 per etapa i per sessió, i part cacheable.
- Estimació prèvia (a confirmar amb l'script), per torn amb la teoria: diagnosi ~4,5k entrada (+~150/torn de
  conversa) i 0,4k sortida + raonament; redacció ~1,5k / 0,2k; guardià ~4k / 0,1k + raonament. Total ≈ 10k entrada
  i 1,5–3k sortida per torn, +~40% per cada reescriptura rebutjada. Amb cache, ~70% de l'entrada de diagnosi i
  guardià és prefix estàtic (preu cached ≈ 10–25% del normal).
- Idees per abaratir (per decidir amb en Matías): guardià LLM només quan el determinista no és concloent o a
  nivells ≥3; diagnosi i redacció en una sola crida quan l'acció és trivial (redirigir/tancar); models petits per
  a redacció/guardià; esforç de raonament `low` a diagnosi per a exercicis `calcul`; índex del tema només quan
  l'alumne fa una pregunta conceptual (2a crida barata); resum de conversa després de N torns.

### Fase 10 — Estudi de models més barats (demanat per en Matías, després de les fases 3-4)
- Banc fix: ~20 exercicis variats (càlcul i teoria, tots els temes) x 3-4 converses d'alumne guionitzades
  (avança bé, error típic, demana la solució, pregunta conceptual) = ~250 torns.
- Configuracions per etapa (diagnosi / redacció / guardià): l'actual (gpt-5.5 + gpt-5.4-mini) contra models més barats
  (mini/nano d'OpenAI, Gemini Flash/Flash-Lite, Claude Haiku, DeepSeek/Kimi via OpenRouter) i esforç de raonament low/medium.
- Mètriques: cost real per torn (tokens x preu actual, amb cache), latència, % torns amb fallback, % esborranys rebutjats,
  fuites detectades per un jutge fort independent (revela resultat/pas futur), qualitat de la diagnosi contra una
  etiqueta de referència (passos completats, error detectat), i cites de teoria correctes.
- Variants d'arquitectura: guardià LLM només a nivell >=3 o si el determinista dubta; índex del tema només en preguntes
  conceptuals; diagnosi+redacció en una crida en torns trivials.
- Sortida: taula cost/qualitat per configuració i recomanació (script scripts/model_study.py + informe).

### Fase 9 — Docs
- Actualitzar `README.md` (llistes, teoria, cites, cache, comandes noves). Esborrar `work/` quan tot estigui muntat
  (o deixar-hi els enunciats com a font).

## Com reprendre
1. Llegeix aquest fitxer i `work/SPEC_wave2.md`.
2. Comprova què hi ha a `work/fitxes/` (trossos ja fets) i passa `check_fitxes.py` a cadascun.
3. Continua per la primera fase pendent. Les fases 6–7 es poden fer en paral·lel amb la 3–4 si es fa servir
   `work/fitxes/EXEMPLE_t2-4c.yaml` com a llista provisional per als tests.


## Fase 11 — Enduriment i funcions adoptades (2026-10-06, en curs)

FET:
- Política reescrita com a màquina d'estats explícita (backend/tutor/politica.py): una sola regla d'escalada,
  fets de sessió (tancat, mostrats, errors_vistos, repeticions, resultat_confirmat, intents_alumne), sense oracle,
  tancament terminal, preguntes conceptuals fora de l'escala, filtre "no vetar el permès" per a totes les regex.
  Tests d'invariants: tests/test_politica.py. Auditoria: work/research/bugs.md (H1–H6, M1–M12 resolts excepte L-*).
- Redactor en text pla (no JSON): referències extretes de les cites; reparació de LaTeX malmès per JSON.
- Torn atòmic, bloqueig per sessió, caducitat de sessions, transcripció acotada a 16 missatges.
- Rol de professor: TUTOR_CLAU_PROFESSOR + ?prof=<clau>. Sense clau: mode demo obert.
- Registre de converses (backend/registres/*.jsonl) i pàgina #/professor amb marques.
- Funcions adoptades: anti-abús de pistes (Cognitive Tutors), demanar_intent, to empàtic (Bridge/StratL),
  moviments MathDial, exemples de to (LearnLM), rúbrica del guardià ampliada, defensa contra injeccions.
- Arnès d'alumnes simulats: scripts/simulate.py (+ jutge de fuites conscient del nivell).
- Estudi de models (work/study/): gpt-5.4-mini a les 3 etapes = mateixa qualitat que gpt-5.5, ~4× més barat.
  nano i models oberts petits: pitjors. Kimi K2.5/GLM: massa lents.

PENDENT:
- (FET) Verificador sympy integrat al guardià: 2/104 torns reals marcats (frontera), 0 fuites reals perdudes.
- Repetir la simulació (40 exercicis × 8 personatges, ~$25) quan hi hagi crèdit (OpenAI i OpenRouter esgotats
  el 2026-10-06).
- Kimi K2-0905 (ràpid) per provar quan hi hagi crèdit d'OpenRouter.
- Següents: comprovació CAS de respostes de l'alumne (`comprova:` a les fitxes), passos en ordre parcial,
  model d'aprenent (BKT) amb identitat persistent.
