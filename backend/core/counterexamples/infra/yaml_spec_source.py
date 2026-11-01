"""The authored challenges (`contraexemples/reptes.yaml`). Catalan keys, read through the entities' aliases."""

from pathlib import Path

import yaml
from pydantic import ValidationError

from core.counterexamples.domain.entities.spec import Spec, SpecCatalog
from core.counterexamples.domain.exceptions import InvalidSpecContentException
from core.counterexamples.domain.ports import SpecSource
from core.counterexamples.domain.values.spec_id import SpecId


class YamlSpecSource(SpecSource):
    def __init__(self, path: Path) -> None:
        self._path = path

    def load(self) -> SpecCatalog:
        data = yaml.safe_load(self._path.read_text(encoding="utf-8")) or {}
        specs: dict[SpecId, Spec] = {}
        for raw in data.get("reptes", []):
            try:
                spec = Spec.model_validate(raw)
            except ValidationError as e:
                raise InvalidSpecContentException(f"{self._path.name}: repte «{raw.get('id')}» invàlid: {e}") from e
            if spec.id in specs:
                raise InvalidSpecContentException(f"{self._path.name}: repte «{spec.id}» repetit")
            specs[spec.id] = spec
        try:
            return SpecCatalog(specs=specs, property_theory=data.get("teoria_propietats") or {})
        except ValidationError as e:
            raise InvalidSpecContentException(f"{self._path.name}: teoria_propietats invàlid: {e}") from e
