import importlib
import pkgutil

import core


def register_all_tables() -> None:
    """Imports every `core.<context>.infra` module, so each SQLModel table is in `SQLModel.metadata`.

    For composition roots that need the whole schema (test fixtures, scripts/db.py); contexts never call it."""
    for module in pkgutil.walk_packages(core.__path__, prefix="core."):
        if ".infra." in module.name or module.name.endswith(".infra"):
            importlib.import_module(module.name)
