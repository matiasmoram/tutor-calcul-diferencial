"""One real tutor turn against the configured provider: checks schemas, theory citations and cache metrics.

    python scripts/smoke_turn.py [exercise_id] ["student message" ...]

The provider and models come from the environment (.env: LLM_PROVIDER, TUTOR_MODEL, TUTOR_MODEL_<STAGE>, ...), as for
the server. The session lives in a throwaway SQLite database.
"""

import argparse
import asyncio
import json

from dotenv import load_dotenv
from model_study import LocalTutor, load_course, scratch_database

from core.shared.llm.infra.factory import make_llm_client
from settings import ROOT_DIR, Config

DEFAULT_MESSAGES = [
    "Què vol dir exactament que el límit existeixi? No entenc la definició.",
    "He provat les rectes y=kx i dona 0, per tant el límit és 0.",
]


async def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("exercise", nargs="?", default="t2-4c", help="exercise id (default t2-4c)")
    ap.add_argument("messages", nargs="*", help="student messages, one per turn (default: two scripted ones)")
    args = ap.parse_args(argv)
    load_dotenv(ROOT_DIR / ".env")
    course = load_course()
    if args.exercise not in course.exercises:
        ap.error(f"unknown exercise {args.exercise!r}")
    async with scratch_database() as provider:
        tutoring = LocalTutor(course, provider, make_llm_client(Config()))
        session_id = await tutoring.start(args.exercise)
        for m in args.messages or DEFAULT_MESSAGES:
            out = await tutoring.turn(session_id, m)
            t = out.trace
            print(f"\nALUMNE: {m}\nTUTOR: {out.message}")
            print(f"  acció={t.plan.action} teoria_permesa={t.allowed_theory} refs={[r.id for r in out.references]}")
            print("  " + json.dumps([(c.stage, c.input_tokens, c.cached_tokens, c.output_tokens) for c in t.calls]))


if __name__ == "__main__":
    asyncio.run(main())
