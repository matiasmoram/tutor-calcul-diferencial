"""Loads a script of ``scripts/`` as a module: scripts are command-line entry points, not a package."""

import importlib.util
import sys
from types import ModuleType

from settings import ROOT_DIR


def load_script(relpath: str) -> ModuleType:
    """``relpath`` is the script's path under ``scripts/`` without ``.py`` (``"check_fitxes"``, ``"eval/simulate"``).

    The script's folder goes on ``sys.path`` so it imports its siblings by name, as when it runs from the command line.
    """
    path = ROOT_DIR / "scripts" / f"{relpath}.py"
    name = "scripts_" + relpath.replace("/", "_")
    if name in sys.modules:
        return sys.modules[name]
    if str(path.parent) not in sys.path:
        sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module
