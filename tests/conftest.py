"""Every test run uses a throwaway SQLite database, never data/tutor.db or a configured DATABASE_URL."""

import os
import tempfile
from pathlib import Path

os.environ["DATABASE_URL"] = f"sqlite:///{(Path(tempfile.mkdtemp(prefix='tutor-tests-')) / 'tests.db').as_posix()}"
