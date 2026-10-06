import sys
sys.path.insert(0, "backend"); sys.path.insert(0, "tests")
from test_harness import EX, ScriptedLLM  # noqa
from tutor.errades import SolucioAmbErrors, ErrorDeclarat, Anotacio, grade, compare_verification
frag = ["Sigui $f$.", "Per tant $|f|\ge|x|$ i el limit es 0.", "Fi."]
e1 = ErrorDeclarat(id="e1", fragment=2, cita="$|f|\ge|x|$", inici=9, fi=20, tipus="desigualtat", explicacio="", correccio="", pista="")
sol = SolucioAmbErrors(id="x", exercici="t2-4c", dificultat="facil", fragments=frag, errors=[e1])
exact = Anotacio(id="a1", fragment=2, inici=9, fi=20, comentari="la desigualtat esta girada")
whole = Anotacio(id="a1", fragment=2, inici=0, fi=len(frag[1]), comentari="")
def g(ann, avals):
    return grade(ScriptedLLM({"errades_correccio": [{"avaluacions": avals, "resum": ""}]}), EX["t2-4c"], sol, ann)
r = g([exact], [])  # model omitted the evaluation
print("omitted eval on exact hit:", r["nota"], r["trobats"], r["falsos_positius"])
r = g([exact], [{"anotacio": "a1", "error": "cap", "explicacio": "incorrecta", "feedback": ""}])
print("LLM says 'cap' on exact hit:", r["nota"], r["trobats"], r["falsos_positius"])
r1 = g([exact], [{"anotacio": "a1", "error": "e1", "explicacio": "incorrecta", "feedback": ""}])
r2 = g([exact], [{"anotacio": "a1", "error": "e1", "explicacio": "absent", "feedback": ""}])
print("wrong reason vs no reason:", r1["nota"], r2["nota"])
r = g([whole], [{"anotacio": "a1", "error": "e1", "explicacio": "absent", "feedback": ""}])
print("whole-fragment highlight localisation:", r["anotacions"][0]["localitzacio"])
print("verifier finds a DIFFERENT error in the same fragment ->", compare_verification([e1], [{"fragment": 2, "gravetat": "error", "cita": "el limit es 0", "explicacio": "conclusio no justificada"}]))
