"""Throwaway: demonstrate policy state-machine bugs with synthetic diagnoses (no LLM)."""
import sys
sys.path.insert(0, "backend"); sys.path.insert(0, "tests")
from test_harness import diag, EX, TEORIA  # noqa
from tutor.politica import EstatSessio, decide, allowed_content, allowed_theory
from tutor.guardia import deterministic_check

def run(name, ex_id, seq, st=None):
    ex = EX[ex_id]; st = st or EstatSessio()
    print(f"\n== {name} ({ex_id})")
    for i, kw in enumerate(seq, 1):
        pla, st = decide(ex, diag(ex_id, **kw), st)
        print(f"  t{i}: accio={pla.accio:20s} pas={pla.pas_objectiu} niv={pla.nivell_pista} "
              f"completats={st.completats} nivells={st.nivell_per_pas} tancat={st.tancat}")
    return pla, st

# A: the diagnosis keeps reporting the (correct, unjustified) result already said earlier
run("A demanar_justificacio absorbs everything", "t2-4c", [
    dict(resultat_proposat="correcte", intencio="proposa_resultat", nivell_desorientacio="en_cami"),
    dict(resultat_proposat="correcte", intencio="demana_pista", nivell_desorientacio="encallat"),
    dict(resultat_proposat="correcte", intencio="demana_solucio", nivell_desorientacio="perdut"),
    dict(resultat_proposat="correcte", intencio="frustracio", nivell_desorientacio="perdut"),
    dict(resultat_proposat="correcte", intencio="mostra_treball", nivell_desorientacio="en_cami", passos={"candidat": "completat"}),
    dict(resultat_proposat="correcte", intencio="pregunta_conceptual", nivell_desorientacio="dubte_puntual", passos={"candidat": "completat"}),
])
# B: wrong result stays in the diagnosis
run("B questionar_resultat never escalates", "t2-4c", [
    dict(resultat_proposat="incorrecte", intencio="demana_pista", nivell_desorientacio="encallat")] * 4)
# C: same catalogued error repeated
pla, _ = run("C questionar_error loops at level 0", "t2-4c", [
    dict(errors_detectats=["camins_com_a_prova"], intencio="demana_pista", nivell_desorientacio="perdut")] * 4)
print("   fallback each turn =", (pla.pregunta_suggerida or "<per nivell>")[:70], "...")
# D: after tancar the session continues and forgets it was closed
run("D life after tancar", "t2-4c", [
    dict(resultat_proposat="correcte", resultat_justificat=True, intencio="proposa_resultat", nivell_desorientacio="en_cami"),
    dict(resultat_proposat="cap", intencio="mostra_treball", nivell_desorientacio="en_cami"),
    dict(resultat_proposat="correcte", resultat_justificat=False, intencio="proposa_resultat", nivell_desorientacio="en_cami"),
])
# E: a conceptual question raises the step level to 2; next ordinary turn escalates to 3
pla, st = run("E conceptual question escalates hints", "t2-4c", [
    dict(intencio="pregunta_conceptual", nivell_desorientacio="dubte_puntual"),
    dict(intencio="mostra_treball", nivell_desorientacio="en_cami", passos={"candidat": "en_curs"}),
])
# F: a student making partial progress (en_curs) is escalated every turn
run("F en_curs progress still escalates", "t2-4c", [
    dict(intencio="mostra_treball", nivell_desorientacio="en_cami", passos={"candidat": "en_curs"})] * 3)
# H: frustrated / lost student plateaus at level 3 forever (mostrar_pas only on demana_solucio)
run("H level-3 plateau", "t2-4c", [dict(intencio="frustracio", nivell_desorientacio="perdut")] * 5)
# K: tancar wins over a detected error
run("K tancar beats detected error", "t2-4c", [
    dict(resultat_proposat="correcte", resultat_justificat=True, errors_detectats=["camins_com_a_prova"],
         intencio="proposa_resultat", nivell_desorientacio="en_cami")])
# M: wrong result after all steps done -> questionar_resultat with no target
pla, st = run("M questionar_resultat without target", "t2-4c", [
    dict(passos={s: "completat" for s in EX["t2-4c"].step_ids}, resultat_proposat="incorrecte",
         intencio="proposa_resultat", nivell_desorientacio="en_cami")])
print("   allowed_content:", allowed_content(EX["t2-4c"], pla, st.completats)[-120:].replace("\n", " | "))
# N: 'altre' error with empty error_altre
pla, st = run("N altre with empty description", "t2-4c", [dict(errors_detectats=["altre"], error_altre="")])
print("   allowed_content:", allowed_content(EX["t2-4c"], pla, st.completats))
# O: result oracle: guesses phrased as questions
run("O result oracle", "t2-4c", [
    dict(resultat_proposat="incorrecte", intencio="proposa_resultat", nivell_desorientacio="dubte_puntual"),
    dict(resultat_proposat="correcte", intencio="proposa_resultat", nivell_desorientacio="dubte_puntual")])

# G: out-of-order completion: completed later step's detail is vetoed
ex = EX["t2-4c"]
pla, st = decide(ex, diag(passos={"candidat": "completat", "concloure": "completat"}, nivell_desorientacio="en_cami"), EstatSessio())
print("\n== G out-of-order completed step", pla.accio, pla.pas_objectiu, st.completats)
det = ex.pas("concloure").detall
print("   concloure detail in allowed content:", det.strip()[:60] in allowed_content(ex, pla, st.completats))
print("   restating it is vetoed:", deterministic_check(f"Molt bé: {det.strip()} Com fitaries ara el quocient?", pla)[:1])

# L: mostrar_pas cannot show a step whose detail matches a later step's regex
for ex_id, step in [("t5-14", "signe_phi"), ("t1-7d", "frontera"), ("t6-3a", "existencia")]:
    ex = EX[ex_id]; i = ex.step_ids.index(step); done = ex.step_ids[:i]
    st = EstatSessio(completats=done, nivell_per_pas={step: 3}, ultim_pas=step)
    pla, _ = decide(ex, diag(ex_id, passos={s: "completat" for s in done}, intencio="demana_solucio", nivell_desorientacio="perdut"), st)
    msg = f"Aquest és el pas: {ex.pas(step).detall.strip()} Amb això, com continuaries?"
    print(f"\n== L {ex_id}/{step}: accio={pla.accio} niv={pla.nivell_pista}; verbatim step rejected by:",
          [p[:90] for p in deterministic_check(msg, pla) if "prohibit" in p])
