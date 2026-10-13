from pydantic import BaseModel

from core.counterexamples.domain.entities.spec import SpecCatalog
from core.counterexamples.domain.ports import PropertyChecker
from core.counterexamples.domain.values.spec_id import SpecId
from core.counterexamples.domain.values.submission import PropertyCheck, Submission, validate_submission
from core.counterexamples.domain.values.verdict import RevealedExample, SubmissionResult


class SubmissionGraderInput(BaseModel):
    spec_id: SpecId
    submission: Submission
    reveal_example: bool = False  # a professor sees the authored example whatever the outcome


class SubmissionGrader:
    """Checks a proposed counterexample against every property its challenge asks for."""

    def __init__(self, catalog: SpecCatalog, checker: PropertyChecker) -> None:
        self._catalog = catalog
        self._checker = checker

    async def grade(self, data: SubmissionGraderInput) -> SubmissionResult:
        spec = self._catalog.spec(data.spec_id)
        # Builds the expression trees without evaluating them: cheap and bounded, so it stays on the event loop.
        validate_submission(data.submission, spec.properties)
        paths = [path for cert in data.submission.certificates.values() for path in cert.paths]
        checks = [
            PropertyCheck(
                kind=kind,
                function=data.submission.function,
                origin_value=data.submission.origin_value,
                certificate=data.submission.certificate(kind),
                context_paths=paths,
            )
            for kind in spec.properties
        ]
        result = SubmissionResult(verdicts=await self._checker.check(checks))
        if result.passed or data.reveal_example:
            result.example = RevealedExample(submission=spec.example, explanation=spec.explanation)
        return result
