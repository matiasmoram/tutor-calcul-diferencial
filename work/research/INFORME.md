# Informe combinat — models, errors de lògica, alternatives i arquitectura (2026-10-06)

Fonts: `work/study/` (estudi de models), `work/research/bugs.md`, `work/research/frameworks.md`,
`work/research/architectures.md`, `work/sim/hardened1/` (primera simulació d'alumnes).

## 1. Models (4 exercicis × 4 torns guionitzats; indicatiu, no estadístic)

| Configuració (diagnosi / redacció / guardià) | Intenció | Error | $/torn | Latència | Lectura de transcripcions |
|---|---|---|---|---|---|
| gpt-5.5 / 5.4-mini / 5.4-mini (anterior) | 14/16 | 14/16 | 0.035 | 12 s | Bona |
| **gpt-5.4-mini ×3 (recomanada)** | **15/16** | **16/16** | **0.008** | **7 s** | **Bona, concisa, respecta el nivell** |
| gpt-5-mini ×3 | 14/16 | 14/16 | 0.004 | 17 s | Verbosa, s'excedeix de nivell |
| gpt-5-nano ×3 | 14/16 | 16/16 | 0.001 | 28 s | Marca passos massa d'hora, una fuita, LaTeX sense `$` |
| gpt-5.4-nano, gpt-4.1-nano | 9–11/16 | 9–15/16 | 0.001–0.003 | 8 s | Pitjor, fallbacks |
| Oberts 4–20B (gpt-oss, nemo, llama, gemma) | 1–5/16 | 5–11/16 | <0.001 | 8–130 s | Inservibles |
| Kimi K2.5, GLM-4.7-Flash, DeepSeek V4 | — | — | — | 2–6 min | "Thinking": massa lents |
| Qwen3.5-Flash | — | — | — | — | No respecta l'esquema |

Conclusió: per sota de "mini" la qualitat cau; per sobre, el que falla és la lògica, no el model.
Kimi K2-0905 (no-thinking) queda per provar: OpenRouter sense crèdit.

## 2. Errors de lògica (auditoria) — resolts
Arrel comuna: l'escalada només existia a la branca "pista" i l'estat no tenia fets de sessió.
- Bucles: demanar justificació, error repetit, resultat incorrecte repetit → ara una sola regla d'escalada.
- Oracle sí/no amb endevinalles → no es confirma ni es desmenteix sense raonament.
- Tancar no era terminal → ara ho és.
- Regex que vetaven contingut permès (22 casos de "mostrar pas" impossible) → filtre general.
- Fallbacks que gastaven nivells → el fallback lliura el contingut del nivell.
- Torn no atòmic, JSON invàlid del guardià, cites "Teorema 17(d)" mal enllaçades, indicacions perdudes,
  respostes que arribaven a un altre exercici, correcció de "Troba l'error" → resolts.
- Regressió pròpia trobada i resolta: "pas erroni → error 'altre'" generava errors fantasma cada torn.

## 3. Alternatives famoses — què s'ha adoptat
| Font | Idea | Estat |
|---|---|---|
| Cognitive Tutors, Ruffle&Riley | Anti-abús de pistes; pista final només després d'un intent; auto-explicació | Fet |
| Bridge, StratL | Decisió abans de la generació; branca afectiva (to empàtic) | Fet |
| MathDial | Etiquetes de moviment docent (Focus/Probing/Telling) | Fet |
| LearnLM | Exemples de to per acció; rúbrica del guardià ampliada | Fet |
| CS50, CodeHelp, atacs adversaris | Defensa contra injeccions; text de l'alumne = dades | Fet |
| Khanmigo, Eedi | Registre i revisió del professorat | Fet (`#/professor`) |
| MathDial, PedagogicalRL | Alumnes simulats + personatges adversaris | Fet (`scripts/simulate.py`) |
| TutorGym, Khanmigo (calculadora), EduFair | Verificació simbòlica (sympy) de fuites i respostes | En curs |
| OATutor (BKT) | Model d'aprenent entre exercicis | Pendent (cal identitat persistent) |

On som per davant: el redactor no veu el que no pot revelar (Study Mode, Khanmigo, CS50 i CodeHelp només
ho demanen al prompt). On som per darrere: verificació formal de la correcció i avaluació a escala.

## 4. Arquitectura recomanada
"Hybrid CAS + statechart": mantenir el pipeline (diagnosi → política determinista → redacció amb contingut
limitat → guardià), amb la política com a màquina d'estats amb invariants (fet), sympy al guardià i a la
diagnosi de passos computacionals (en curs), i un banc d'avaluació amb alumnes simulats (fet; falta executar-lo
a escala). Descartat: crida única diagnosi+resposta (perd la garantia de no-fuita per estalviar <1 cèntim).

## 5. Primera simulació (parcial: crèdit esgotat a mitja execució)
Dels 2 exercicis complets: 0 fuites del resultat final; 1 fuita real a nivell 1 (la fórmula clau del pas), que
detectarà el verificador sympy; bucles amb el "captaire" i l'"injector" → nova acció `demanar_intent`.

## 6. Pendent (quan hi hagi crèdit)
1. Integrar sympy al guardià i tornar a simular (40 exercicis × 8 personatges, ~25 $).
2. Provar Kimi K2-0905 i mini+Kimi K2.
3. Següents: `comprova:` a les fitxes (correcció simbòlica de respostes), passos en ordre parcial, BKT.
