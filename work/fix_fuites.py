"""One-off fixes for leak regexes that failed check_fitxes (textual replace of single-quoted YAML strings)."""
import sys
from pathlib import Path

D = Path(__file__).parent / "fitxes"

SP = r"(\\\s|\s)*"  # LaTeX "\ " spacing or plain spaces

FIXES = [
    ("tema1_p1", r"\\sqrt\{\\lambda\^\{?2\}?\}", r"\\sqrt\{\\lambda\^\{?2\}?\}\s*\\sqrt"),
    ("tema3_p2", r"\(\s*4[.,]8\s*,\s*7[.,]4\s*\)", r"\(\s*4[.,]8\s*," + SP + r"7[.,]4\s*\)"),
    ("tema5_p1", r"x\^\{?2\}?\s*y\^\{?2\}?\s*t[ée]\s*grau", r"x\^\{?2\}?\s*y\^\{?2\}?\$?\s*t[ée]\s*grau"),
]

for name, old, new in FIXES:
    p = D / f"{name}.yaml"
    s = p.read_text(encoding="utf-8")
    q_old, q_new = "'" + old.replace("'", "''") + "'", "'" + new.replace("'", "''") + "'"
    n = s.count(q_old)
    if n == 0:
        print(f"{name}: not found: {old}", file=sys.stderr)
        continue
    p.write_text(s.replace(q_old, q_new), encoding="utf-8")
    print(f"{name}: fixed")
