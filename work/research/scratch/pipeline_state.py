"""Throwaway: pipeline-level state invariants with a scripted fake LLM (no network)."""
import json, sys
sys.path.insert(0, "backend"); sys.path.insert(0, "tests")
from test_harness import EX, TEORIA, ScriptedLLM, _diag_json  # noqa
from tutor.pipeline import Sessio, Tutor

bad = {"veredicte": "rebutjat", "infraccions": ["excedeix_nivell_pista"], "explicacio": "massa"}
# I: three turns where every draft is rejected -> fallback; hint levels still climb to 3 / mostrar_pas eligibility
llm = ScriptedLLM({
    "diagnosis": [],
    "diagnosi": [_diag_json(intencio="demana_pista", nivell_desorientacio="encallat")] * 3 + [_diag_json(intencio="demana_solucio")],
    "resposta": [{"text": "Pensa en una fita. Què en dius?"}] * 12,
    "guardia": [bad] * 12,
})
t, s = Tutor(llm, TEORIA), Sessio(exercici=EX["t2-4c"])
for msg in ["no sé", "ajuda", "no ho veig", "dona'm la solució"]:
    out = t.turn(s, msg)
    print("I:", out["trace"]["pla"]["accio"], out["trace"]["pla"]["nivell_pista"], "fallback=", out["trace"]["fallback"],
          "->", out["missatge"][:60])

# J1: provider error (not LLMError) in the reply stage leaves a dangling student message
class Boom(Exception): pass
class Flaky(ScriptedLLM):
    def structured(self, stage, *a, **kw):
        if stage == "resposta": raise Boom("429 rate limit from provider SDK")
        return super().structured(stage, *a, **kw)
s = Sessio(exercici=EX["t2-4c"])
try:
    Tutor(Flaky({"diagnosi": [_diag_json()]}), TEORIA).turn(s, "hola, he provat rectes")
except Boom:
    pass
print("J1 historial after failed reply stage:", [m["rol"] for m in s.historial], "torns:", s.estat.torns)

# J2: judge returns invalid JSON -> json.JSONDecodeError is not caught by the fail-closed handler
class BadJudge(ScriptedLLM):
    def structured(self, stage, *a, **kw):
        if stage == "guardia": json.loads("{not json")
        return super().structured(stage, *a, **kw)
s = Sessio(exercici=EX["t2-4c"])
try:
    Tutor(BadJudge({"diagnosi": [_diag_json()], "resposta": [{"text": "Què has provat?"}]}), TEORIA).turn(s, "hola")
    print("J2 handled")
except json.JSONDecodeError as e:
    print("J2 JSONDecodeError escapes turn():", type(e).__name__, "| historial:", [m["rol"] for m in s.historial])
