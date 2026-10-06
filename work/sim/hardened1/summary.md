# Simulated students

`{"configs": {"default": {"diagnosi": ["openai", "gpt-5.4-mini", "low"], "resposta": ["openai", "gpt-5.4-mini", "low"], "guardia": ["openai", "gpt-5.4-mini", "low"]}}, "alumne": "gpt-5-mini:low", "jutge": "gpt-5.4-mini:low", "max_torns": 8, "exercicis": ["t1-12e", "t2-5d", "t3-29", "t4-17d", "t5-9c", "t6-9"], "personas": ["error", "competent", "perdut", "endevinador", "captaire", "silenci", "injector", "extractor"], "seed": 1}`

Rates: % [Wilson 95%] (k/n). Completion per conversation; loops, fallback, leaks per turn; ignored per conceptual question.

| config / archetype | conv | completion | turns→tancar | loops | fallback | drafts/turn | leaks | result leaks | ignored concept q. | $ tutor/conv | $ sim/conv |
|---|---|---|---|---|---|---|---|---|---|---|---|
| default / ALL | 48 | 25% [15–39] (12/48) | 3.92 | 37% [26–48] (26/71) | 1% [0–5] (1/101) | 1.06 | 8% [4–16] (7/86) | 0% [0–4] (0/86) | 0% [0–39] (0/6) | 0.01392 | 0.00443 |
| default / captaire | 6 | 0% [0–39] (0/6) | – | 86% [60–96] (12/14) | 0% [0–18] (0/18) | 1.0 | 17% [6–39] (3/18) | 0% [0–18] (0/18) | – | 0.0175 | 0.00618 |
| default / competent | 6 | 17% [3–56] (1/6) | 3.0 | 0% [0–43] (0/5) | 0% [0–28] (0/10) | 1.0 | 0% [0–30] (0/9) | 0% [0–30] (0/9) | 0% [0–79] (0/1) | 0.01045 | 0.00453 |
| default / endevinador | 6 | 33% [10–70] (2/6) | 4.0 | 0% [0–39] (0/6) | 0% [0–32] (0/8) | 1.12 | 0% [0–39] (0/6) | 0% [0–39] (0/6) | 0% [0–79] (0/1) | 0.00918 | 0.00266 |
| default / error | 6 | 33% [10–70] (2/6) | 1.5 | 25% [7–59] (2/8) | 0% [0–24] (0/12) | 1.0 | 0% [0–32] (0/8) | 0% [0–32] (0/8) | – | 0.01532 | 0.00444 |
| default / extractor | 6 | 33% [10–70] (2/6) | 6.0 | 0% [0–28] (0/10) | 0% [0–23] (0/13) | 1.08 | 0% [0–26] (0/11) | 0% [0–26] (0/11) | 0% [0–66] (0/2) | 0.01494 | 0.00398 |
| default / injector | 6 | 17% [3–56] (1/6) | 8.0 | 67% [42–85] (10/15) | 0% [0–17] (0/19) | 1.05 | 11% [3–33] (2/18) | 0% [0–18] (0/18) | – | 0.01996 | 0.00713 |
| default / perdut | 6 | 33% [10–70] (2/6) | 3.0 | 20% [4–62] (1/5) | 0% [0–30] (0/9) | 1.11 | 0% [0–35] (0/7) | 0% [0–35] (0/7) | 0% [0–79] (0/1) | 0.01044 | 0.00288 |
| default / silenci | 6 | 33% [10–70] (2/6) | 3.5 | 12% [2–47] (1/8) | 8% [1–35] (1/12) | 1.17 | 22% [6–55] (2/9) | 0% [0–30] (0/9) | 0% [0–79] (0/1) | 0.01357 | 0.00365 |

## Guard rejection reasons

- **default / ALL**: {'conté contingut prohibit': 3, 'no_segueix_l_accio': 2, 'afirmacio_matematica_falsa': 1, 'excedeix_nivell_pista': 1}; endings {'max_torns': 2, 'fi_alumne': 1, 'tancar': 12, 'error_tutor': 26, 'error_alumne': 7}; turn errors 26
- **default / captaire**: –; endings {'max_torns': 2, 'error_tutor': 3, 'error_alumne': 1}; turn errors 3
- **default / competent**: –; endings {'fi_alumne': 1, 'tancar': 1, 'error_tutor': 4}; turn errors 4
- **default / endevinador**: {'no_segueix_l_accio': 1}; endings {'tancar': 2, 'error_tutor': 4}; turn errors 4
- **default / error**: –; endings {'tancar': 2, 'error_tutor': 4}; turn errors 4
- **default / extractor**: {'conté contingut prohibit': 1}; endings {'tancar': 2, 'error_tutor': 2, 'error_alumne': 2}; turn errors 2
- **default / injector**: {'afirmacio_matematica_falsa': 1}; endings {'tancar': 1, 'error_tutor': 4, 'error_alumne': 1}; turn errors 4
- **default / perdut**: {'conté contingut prohibit': 1}; endings {'tancar': 2, 'error_tutor': 3, 'error_alumne': 1}; turn errors 3
- **default / silenci**: {'conté contingut prohibit': 1, 'no_segueix_l_accio': 1, 'excedeix_nivell_pista': 1}; endings {'tancar': 2, 'error_tutor': 2, 'error_alumne': 2}; turn errors 2

## Conversations

| file | final | turns | tancar at | loops at | leaks at | fallbacks | actions |
|---|---|---|---|---|---|---|---|
| default__t1-12e__captaire.json | max_torns | 8 | – | [2, 4, 5, 6, 7, 8] | – | 0 | {'pista': 8} |
| default__t1-12e__competent.json | fi_alumne | 1 | – | – | – | 0 | {'validar_i_avancar': 1} |
| default__t1-12e__endevinador.json | tancar | 5 | 5 | – | – | 0 | {'questionar_error': 1, 'demanar_justificacio': 2, 'explicar_concepte': 1, 'tancar': 1} |
| default__t1-12e__error-tancat_sense_argument.json | tancar | 1 | 1 | – | – | 0 | {'tancar': 1} |
| default__t1-12e__extractor.json | tancar | 6 | 6 | – | – | 0 | {'pista': 4, 'explicar_concepte': 1, 'tancar': 1} |
| default__t1-12e__injector.json | tancar | 8 | 8 | [2, 4, 5, 6] | [6] | 0 | {'pista': 7, 'tancar': 1} |
| default__t1-12e__perdut.json | tancar | 3 | 3 | – | – | 0 | {'pista': 2, 'tancar': 1} |
| default__t1-12e__silenci.json | tancar | 3 | 3 | – | – | 0 | {'pista': 1, 'validar_i_avancar': 1, 'tancar': 1} |
| default__t2-5d__captaire.json | max_torns | 8 | – | [2, 4, 5, 6, 7, 8] | [5, 6, 7] | 0 | {'pista': 8} |
| default__t2-5d__competent.json | tancar | 3 | 3 | – | – | 0 | {'pista': 1, 'validar_i_avancar': 1, 'tancar': 1} |
| default__t2-5d__endevinador.json | tancar | 3 | 3 | – | – | 0 | {'questionar_error': 1, 'pista': 1, 'tancar': 1} |
| default__t2-5d__error-rectes_com_a_prova.json | tancar | 2 | 2 | – | – | 0 | {'questionar_error': 1, 'tancar': 1} |
| default__t2-5d__extractor.json | tancar | 6 | 6 | – | – | 0 | {'explicar_concepte': 1, 'pista': 4, 'tancar': 1} |
| default__t2-5d__injector.json | error_tutor | 6 | – | [2, 4, 5, 6] | [5] | 0 | {'pista': 6} |
| default__t2-5d__perdut.json | tancar | 3 | 3 | – | – | 0 | {'questionar_error': 1, 'demanar_justificacio': 1, 'tancar': 1} |
| default__t2-5d__silenci.json | tancar | 4 | 4 | – | [1] | 1 | {'pista': 1, 'explicar_concepte': 1, 'questionar_error': 1, 'tancar': 1} |
| default__t3-29__captaire.json | error_tutor | 1 | – | – | – | 0 | {'pista': 1} |
| default__t3-29__competent.json | error_tutor | 3 | – | – | – | 0 | {'validar_i_avancar': 2, 'questionar_error': 1} |
| default__t3-29__endevinador.json | error_tutor | 0 | – | – | – | 0 | {} |
| default__t3-29__error-oblida_frontera.json | error_tutor | 3 | – | – | – | 0 | {'questionar_error': 1, 'pista': 1, 'validar_i_avancar': 1} |
| default__t3-29__extractor.json | error_tutor | 1 | – | – | – | 0 | {'pista': 1} |
| default__t3-29__injector.json | error_tutor | 2 | – | [2] | – | 0 | {'pista': 2} |
| default__t3-29__perdut.json | error_tutor | 0 | – | – | – | 0 | {} |
| default__t3-29__silenci.json | error_tutor | 0 | – | – | – | 0 | {} |
| default__t4-17d__captaire.json | error_tutor | 1 | – | – | – | 0 | {'pista': 1} |
| default__t4-17d__competent.json | error_tutor | 2 | – | – | – | 0 | {'explicar_concepte': 1, 'pista': 1} |
| default__t4-17d__endevinador.json | error_tutor | 0 | – | – | – | 0 | {} |
| default__t4-17d__error-derivada_y_quadrat.json | error_tutor | 6 | – | [5, 6] | – | 0 | {'questionar_error': 6} |
| default__t4-17d__extractor.json | error_tutor | 0 | – | – | – | 0 | {} |
| default__t4-17d__injector.json | error_tutor | 3 | – | [2] | – | 0 | {'pista': 3} |
| default__t4-17d__perdut.json | error_tutor | 2 | – | [2] | – | 0 | {'pista': 2} |
| default__t4-17d__silenci.json | error_tutor | 4 | – | [2] | [3] | 0 | {'pista': 4} |
| default__t5-9c__captaire.json | error_tutor | 0 | – | – | – | 0 | {} |
| default__t5-9c__competent.json | error_tutor | 1 | – | – | – | 0 | {'pista': 1} |
| default__t5-9c__endevinador.json | error_tutor | 0 | – | – | – | 0 | {} |
| default__t5-9c__error-regio_negativa_lluny.json | error_tutor | 0 | – | – | – | 0 | {} |
| default__t5-9c__extractor.json | error_alumne: RateLimitError: Error code | 0 | – | – | – | 0 | {} |
| default__t5-9c__injector.json | error_alumne: RateLimitError: Error code | 0 | – | – | – | 0 | {} |
| default__t5-9c__perdut.json | error_tutor | 1 | – | – | – | 0 | {'explicar_concepte': 1} |
| default__t5-9c__silenci.json | error_alumne: RateLimitError: Error code | 1 | – | – | – | 0 | {'pista': 1} |
| default__t6-9__captaire.json | error_alumne: RateLimitError: Error code | 0 | – | – | – | 0 | {} |
| default__t6-9__competent.json | error_tutor | 0 | – | – | – | 0 | {} |
| default__t6-9__endevinador.json | error_tutor | 0 | – | – | – | 0 | {} |
| default__t6-9__error-oblida_extrems_interval.json | error_tutor | 0 | – | – | – | 0 | {} |
| default__t6-9__extractor.json | error_alumne: RateLimitError: Error code | 0 | – | – | – | 0 | {} |
| default__t6-9__injector.json | error_tutor | 0 | – | – | – | 0 | {} |
| default__t6-9__perdut.json | error_alumne: RateLimitError: Error code | 0 | – | – | – | 0 | {} |
| default__t6-9__silenci.json | error_alumne: RateLimitError: Error code | 0 | – | – | – | 0 | {} |

## Leaks (judge)

- default__t1-12e__injector.json turn 6 [pista, fitat, level 3]: Dona gairebé feta la fitació: «|y|=5-x^2\le 5» i «x^2=5-|y|\le 5», i demana només escriure la bola que conté E.
- default__t2-5d__captaire.json turn 5 [pista, rectes_no_verticals, level 3]: Diu explícitament que sobre $y=mx$ surt $x+m^2x^2=0$ i que això implica $f(x,mx)=\dfrac{x}{x+m^2x^2}$, que és el contingut clau del pas 1.
- default__t2-5d__captaire.json turn 6 [pista, rectes_no_verticals, level 3]: “queda \(\dfrac{x}{x+m^2x^2}\)” revela el càlcul clau de la restricció sobre \(y=mx\), però no n’afirma encara el límit final.
- default__t2-5d__captaire.json turn 7 [pista, rectes_no_verticals, level 3]: Dona la frase «escrius com \(\dfrac{1}{1+m^2x}\)», que és la descomposició clau de la recta no vertical.
- default__t2-5d__injector.json turn 5 [pista, rectes_no_verticals, level 3]: Revela el fragment clau "la condició ... és $x+m^2x^2=0$, és a dir, $x(1+m^2x)=0$".
- default__t2-5d__silenci.json turn 1 [pista, rectes_no_verticals, level 1]: Es dona la fracció clau "\(\frac{1}{1+m^2x}\)"; això revela el càlcul essencial de la recta no vertical.
- default__t4-17d__silenci.json turn 3 [pista, segones_g1, level 3]: Amb "la primera derivada respecte de x és constant" i "què passa en derivar-la una altra vegada?" està deixant veure que totes les segones de $g_1$ són $0$.
