import re, sys, collections, yaml
from pathlib import Path
sys.path.insert(0, "backend")
from tutor.fitxes import load_llistes
from tutor.teoria import load_teoria, parse_ref, CITA
from tutor.guardia import count_sentences
T = load_teoria()
L, EX = load_llistes(teoria=T)
print("exercises", len(EX))
# indicacio non-null
n_ind = sum(1 for l in L.values() for p in l.problemes if p.indicacio)
print("problems with indicacio:", n_ind)
# theory problemes field formats
fmts = collections.Counter()
for it in T.values():
    for p in it.problemes: fmts[re.sub(r"\d+", "N", p)] += 1
print("theory.problemes formats:", fmts)
# duplicates (tema,num)
keys = collections.Counter((it.tema, it.num) for it in T.values() if it.num is not None)
print("dup (tema,num):", [k for k, c in keys.items() if c > 1][:10])
# refs to num-less items
nonum = {i for i, it in T.items() if it.num is None}
uses = [(e.id, r) for e in EX.values() for r in e.all_refs() if parse_ref(r)[0] in nonum]
print("sheet refs to items without num:", len(uses), uses[:5])
# cross-tema refs
cross = [(e.id, r) for e in EX.values() for r in e.all_refs() if T[parse_ref(r)[0]].tema != e.tema]
print("cross-tema refs:", len(cross), cross[:5])
# auto reserved count
print("exercises with auto/declared reserved:", sum(1 for e in EX.values() if e.reserved_ids(T)))
# reserved items that are also in step teoria or ex.teoria
clash = [(e.id, i) for e in EX.values() for i in e.reserved_ids(T) if i in {parse_ref(r)[0] for r in e.teoria + [r for p in e.passos for r in p.teoria]}]
print("reserved items also cited as background/step theory:", len(clash), clash[:8])
# empty result fuites / step fuites
print("empty resultat.fuites:", sum(1 for e in EX.values() if not e.resultat.fuites))
print("steps with empty fuites:", sum(1 for e in EX.values() for p in e.passos if not p.fuites), "of", sum(len(e.passos) for e in EX.values()))
print("n steps distribution:", collections.Counter(len(e.passos) for e in EX.values()))
# titles matching any step/result fuites (fallback uses titol)
bad_t = []
for e in EX.values():
    for i, p in enumerate(e.passos):
        regs = list(e.resultat.fuites) + list(p.fuites) + [r for q in e.passos[i+1:] for r in q.fuites]
        for r in regs:
            if re.search(r, p.titol, re.IGNORECASE):
                bad_t.append((e.id, p.id, r)); break
print("step titles matching vetoed regexes (fallback leaks/bypasses guard):", len(bad_t), bad_t[:8])
# objectiu/idea matching LATER steps' fuites (level 1/2 content vetoed)
bad_o = []
for e in EX.values():
    for i, p in enumerate(e.passos):
        for q in e.passos[i+1:]:
            for r in q.fuites:
                for f in ("objectiu", "idea"):
                    if re.search(r, getattr(p, f), re.IGNORECASE): bad_o.append((e.id, p.id, f, q.id, r))
print("objectiu/idea matching a LATER step's fuites:", len(bad_o), bad_o[:6])
# detail sentence counts vs mostrar_pas max 6 (+1 tolerance)
long = [(e.id, p.id, count_sentences(p.detall)) for e in EX.values() for p in e.passos if count_sentences(p.detall) >= 7]
print("details with >=7 sentences (mostrar_pas cannot show them within 7):", len(long), long[:6])
# detail of step i matched by later-step fuites -> at level 3/4 target detail vetoed by later regex
bad_d = []
for e in EX.values():
    for i, p in enumerate(e.passos):
        for q in e.passos[i+1:]:
            for r in q.fuites:
                if re.search(r, p.detall, re.IGNORECASE): bad_d.append((e.id, p.id, q.id, r)); break
print("step detail matched by a LATER step's fuites (mostrar_pas/level3 vetoed):", len(bad_d), bad_d[:6])
# result regex matching an error question -> checked; result regex matching step details
# preguntes matching later steps relative to... checked by check_fitxes
# Citations inside sheet texts: pregunta (fallback) with theory citations
cit = [(e.id, er.id) for e in EX.values() for er in e.errors_comuns if CITA.search(er.pregunta)]
print("error questions citing theory:", len(cit), cit[:4])
# step ids order & pas named 'cap'
print("step id 'cap':", [e.id for e in EX.values() if "cap" in e.step_ids])
