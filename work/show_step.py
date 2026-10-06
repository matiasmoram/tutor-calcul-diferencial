import sys, yaml
f, ex_id, step = sys.argv[1:4]
d = yaml.safe_load(open(f, encoding="utf-8"))
for p in d["problemes"]:
    for e in p["exercicis"]:
        if e["id"] == ex_id:
            for s in e["passos"]:
                if s["id"] == step:
                    print("OBJ:", s["objectiu"]); print("IDEA:", s["idea"]); print("DET:", s["detall"]); print("FUITES:", s["fuites"])
            if step == "-":
                print("RES:", e["resultat"]["fuites"])
