# Simulated students

`{"configs": {"gemini": {"diagnosi": ["gemini", "gemini-3-flash-preview", "medium"], "resposta": ["gemini", "gemini-3.5-flash-lite", "low"], "guardia": ["gemini", "gemini-3.5-flash-lite", "low"]}}, "alumne": "gemini-3.5-flash-lite", "jutge": "gemini-3.5-flash-lite", "max_torns": 6, "exercicis": ["t2-4c", "t3-5"], "personas": ["competent", "captaire", "endevinador"], "seed": 0}`

Rates: % [Wilson 95%] (k/n). Completion per conversation; loops, fallback, leaks per turn; ignored per conceptual question.

| config / archetype | conv | completion | turns→tancar | loops | fallback | drafts/turn | leaks | result leaks | ignored concept q. | $ tutor/conv | $ sim/conv |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini / ALL | 6 | 0% [0–39] (0/6) | – | – | – | – | – | – | – | 0.0 | 0.0 |
| gemini / captaire | 2 | 0% [0–66] (0/2) | – | – | – | – | – | – | – | 0.0 | 0.0 |
| gemini / competent | 2 | 0% [0–66] (0/2) | – | – | – | – | – | – | – | 0.0 | 0.0 |
| gemini / endevinador | 2 | 0% [0–66] (0/2) | – | – | – | – | – | – | – | 0.0 | 0.0 |

## Guard rejection reasons

- **gemini / ALL**: –; endings {'error_tutor': 6}; turn errors 6
- **gemini / captaire**: –; endings {'error_tutor': 2}; turn errors 2
- **gemini / competent**: –; endings {'error_tutor': 2}; turn errors 2
- **gemini / endevinador**: –; endings {'error_tutor': 2}; turn errors 2

## Conversations

| file | final | turns | tancar at | loops at | leaks at | fallbacks | actions |
|---|---|---|---|---|---|---|---|
| gemini__t2-4c__captaire.json | error_tutor | 0 | – | – | – | 0 | {} |
| gemini__t2-4c__competent.json | error_tutor | 0 | – | – | – | 0 | {} |
| gemini__t2-4c__endevinador.json | error_tutor | 0 | – | – | – | 0 | {} |
| gemini__t3-5__captaire.json | error_tutor | 0 | – | – | – | 0 | {} |
| gemini__t3-5__competent.json | error_tutor | 0 | – | – | – | 0 | {} |
| gemini__t3-5__endevinador.json | error_tutor | 0 | – | – | – | 0 | {} |
