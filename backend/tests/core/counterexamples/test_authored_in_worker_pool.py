"""The authored examples through the production path: a real worker pool with the production deadline, one
property at a time, so that a property that only passes in-process (no deadline) or takes most of the deadline is
caught."""

import time
from collections.abc import Iterator

import pytest

from core.counterexamples.domain.services.property_deciders import check_property, undecided
from core.counterexamples.domain.values.properties import PropertyKind
from core.counterexamples.domain.values.spec_id import SpecId
from core.counterexamples.domain.values.submission import Certificate, PropertyCheck
from core.shared.math.infra.sympy_pool import SympyCheckPool
from tests.fixtures.counterexamples import authored_challenges

PRODUCTION_DEADLINE_S = 25.0
BUDGET_S = 10.0

CATALOG = authored_challenges()
CASES = [(spec_id, kind) for spec_id, spec in sorted(CATALOG.specs.items()) for kind in spec.properties]


@pytest.fixture(scope="module")
def pool() -> Iterator[SympyCheckPool]:
    pool = SympyCheckPool(max_workers=1, timeout_s=PRODUCTION_DEADLINE_S)
    warm = PropertyCheck(kind="parcials_existeixen", function="x*y", origin_value="0", certificate=Certificate())
    pool.map_blocking(check_property, [warm], undecided)  # the worker's spawn and imports are not the property's
    yield pool
    pool.close()


@pytest.mark.parametrize(("spec_id", "kind"), CASES)
def test_every_authored_property_passes_well_within_the_deadline(
    pool: SympyCheckPool, spec_id: str, kind: PropertyKind
) -> None:
    example = CATALOG.specs[SpecId(spec_id)].example
    paths = [p for c in example.certificates.values() for p in c.paths]
    check = PropertyCheck(
        kind=kind,
        function=example.function,
        origin_value=example.origin_value,
        certificate=example.certificate(kind),
        context_paths=paths,
    )
    start = time.perf_counter()
    [verdict] = pool.map_blocking(check_property, [check], undecided)
    elapsed = time.perf_counter() - start
    assert verdict.status in ("ok", "plausible"), f"{spec_id} / {kind}: {verdict.detail}"
    assert elapsed < BUDGET_S, f"{spec_id} / {kind}: {elapsed:.1f} s"
