import pytest

from core.counterexamples.domain.entities.spec import SpecCatalog
from core.counterexamples.domain.exceptions import InvalidSpecContentException
from core.counterexamples.domain.properties import PROPERTIES
from tests.fixtures.counterexamples import authored_challenges
from tests.fixtures.course import authored_course


def test_every_cited_item_of_the_notes_exists() -> None:
    authored_challenges().check_theory(authored_course().theory)


def test_every_challenge_and_property_is_tied_to_the_notes() -> None:
    catalog = authored_challenges()
    assert set(catalog.property_theory) == set(PROPERTIES)
    for spec in catalog.specs.values():
        assert spec.theory, spec.id
        # The items that already solve the challenge are never shown before the student passes.
        assert not set(spec.theory) & set(spec.reserved_theory), spec.id


def test_a_missing_item_fails_the_check() -> None:
    catalog = authored_challenges()
    broken = SpecCatalog(specs=catalog.specs, property_theory={**catalog.property_theory, "continua": ["T9.99"]})
    with pytest.raises(InvalidSpecContentException, match=r"T9.99"):
        broken.check_theory(authored_course().theory)
