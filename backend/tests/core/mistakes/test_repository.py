from pathlib import Path

import pytest
from sqlalchemy import bindparam, text

from core.mistakes.application.pregenerated_importer import PregeneratedImporter
from core.mistakes.domain.entities.annotation import Annotation
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise
from core.mistakes.domain.entities.mistake_grading import MistakeGrading, PartGrading
from core.mistakes.domain.entities.mistake_session import MistakeSession
from core.mistakes.domain.exceptions import (
    MistakeExerciseNotFoundException,
    MistakePartAlreadyGradedException,
    MistakeSessionAlreadyGradedException,
    MistakeSessionNotFoundException,
)
from core.mistakes.domain.services.grading import grade
from core.mistakes.domain.values.mistake_exercise_id import MistakeExerciseId
from core.mistakes.infra.json_file_source import JsonFileMistakeSource
from core.mistakes.infra.sqlmodel_repository import (
    SQLModelMistakeExerciseRepository,
    SQLModelMistakeSessionRepository,
)
from core.shared.domain.ids import SessionId
from core.shared.storage.session_provider import JsonColumn, SQLModelSessionProvider
from settings import BACKEND_DIR
from tests.core.mistakes.builders import parted, solution


def session_of(exercise_id: str = "0000000000aa") -> MistakeSession:
    return MistakeSession(
        id=SessionId.generate(),
        source_kind="problema",
        source_id="t2-4c",
        exercise_id=MistakeExerciseId(exercise_id),
        difficulty="normal",
        created_at=10.0,
    )


def empty_grading() -> MistakeGrading:
    return grade(solution(), [], None, None)


def test_every_stored_document_loads_and_writes_back_the_same_json() -> None:
    """The committed documents are a stored contract: each one loads and serializes to exactly its file."""
    directory = BACKEND_DIR / "generats" / "errades"
    paths = sorted(directory.glob("*/*/*.json"))
    documents = JsonFileMistakeSource(directory).load()
    assert paths and len(documents) == len(paths)
    for path, document in zip(paths, documents, strict=True):
        assert document.model_dump_json(indent=2) == path.read_text(encoding="utf-8"), path


async def test_documents_round_trip_and_are_replaced_by_id(session_provider: SQLModelSessionProvider) -> None:
    repo = SQLModelMistakeExerciseRepository(session_provider)
    doc = solution()
    await repo.save(doc)
    assert await repo.get(doc.id) == doc
    edited = doc.model_copy(update={"fragments": [*doc.fragments[:-1], "Per tant el límit val $0$."]})
    await repo.save(edited)
    assert await repo.get(doc.id) == edited
    assert await repo.availability() == {"t2-4c": {"normal": 1}}
    with pytest.raises(MistakeExerciseNotFoundException):
        await repo.get(MistakeExerciseId("ffffffffffff"))


async def test_documents_of_a_source_are_ordered_by_id_and_counted(session_provider: SQLModelSessionProvider) -> None:
    repo = SQLModelMistakeExerciseRepository(session_provider)
    for i, doc_id in enumerate(("cccccccccccc", "aaaaaaaaaaaa", "bbbbbbbbbbbb")):
        await repo.save(solution(doc_id).model_copy(update={"difficulty": "dificil" if i == 0 else "normal"}))
    await repo.save(solution("dddddddddddd").model_copy(update={"source_id": "T3.21", "source_kind": "teoria"}))
    assert [d.id for d in await repo.of_source("t2-4c", "normal")] == ["aaaaaaaaaaaa", "bbbbbbbbbbbb"]
    assert await repo.of_source("t2-4c", "facil") == []
    assert await repo.availability() == {"t2-4c": {"normal": 2, "dificil": 1}, "T3.21": {"normal": 1}}


async def test_sessions_round_trip_with_their_grading(session_provider: SQLModelSessionProvider) -> None:
    exercises = SQLModelMistakeExerciseRepository(session_provider)
    sessions = SQLModelMistakeSessionRepository(session_provider)
    await exercises.save(solution())
    s = session_of()
    await sessions.add(s)
    assert await sessions.get(s.id) == s
    annotations = [Annotation(id="a1", fragment=1, start=0, end=3, comment="?")]
    await sessions.save_grading(s.id, annotations, empty_grading(), 11.0)
    assert (await sessions.get(s.id)).grading == empty_grading()
    with pytest.raises(MistakeSessionNotFoundException):
        await sessions.get(SessionId.generate())


async def test_grading_claims_are_exclusive_until_released_or_stale(session_provider: SQLModelSessionProvider) -> None:
    exercises = SQLModelMistakeExerciseRepository(session_provider)
    sessions = SQLModelMistakeSessionRepository(session_provider)
    await exercises.save(solution())
    s = session_of()
    await sessions.add(s)
    assert await sessions.claim_grading(s.id, now=100.0, stale_before=0.0)
    assert not await sessions.claim_grading(s.id, now=101.0, stale_before=1.0)
    assert await sessions.claim_grading(s.id, now=500.0, stale_before=200.0)  # the first claim went stale
    await sessions.release_grading(s.id, claimed_at=100.0)  # the dead grading cannot drop the new claim
    assert not await sessions.claim_grading(s.id, now=501.0, stale_before=201.0)
    await sessions.release_grading(s.id, claimed_at=500.0)
    assert await sessions.claim_grading(s.id, now=501.0, stale_before=201.0)
    await sessions.save_grading(s.id, [], empty_grading(), 502.0)
    await sessions.release_grading(s.id, claimed_at=501.0)
    assert not await sessions.claim_grading(s.id, now=503.0, stale_before=203.0)  # graded: never again
    assert not await sessions.claim_grading(SessionId.generate(), now=1.0, stale_before=0.0)


async def test_a_session_is_graded_once_in_storage(session_provider: SQLModelSessionProvider) -> None:
    exercises = SQLModelMistakeExerciseRepository(session_provider)
    sessions = SQLModelMistakeSessionRepository(session_provider)
    await exercises.save(solution())
    s = session_of()
    await sessions.add(s)
    first = empty_grading()
    await sessions.save_grading(s.id, [], first, 11.0)
    second = first.model_copy(update={"summary": "una altra"})
    with pytest.raises(MistakeSessionAlreadyGradedException) as e:
        await sessions.save_grading(s.id, [], second, 12.0)
    assert e.value.error_code == 409
    assert (await sessions.get(s.id)).grading == first


async def test_each_layout_is_served_and_counted_on_its_own(session_provider: SQLModelSessionProvider) -> None:
    repo = SQLModelMistakeExerciseRepository(session_provider)
    await repo.save(solution("aaaaaaaaaaaa"))
    doc = parted("bbbbbbbbbbbb")
    await repo.save(doc)
    assert [d.id for d in await repo.of_source("t2-4c", "normal")] == ["aaaaaaaaaaaa"]
    assert await repo.of_source("t2-4c", "normal", "per_parts") == [doc]
    assert await repo.get(doc.id) == doc
    assert isinstance(await repo.get(MistakeExerciseId("aaaaaaaaaaaa")), MistakeExercise)
    assert await repo.availability() == {"t2-4c": {"normal": 1}}
    await repo.save(parted("cccccccccccc", difficulty="facil"))
    assert await repo.availability("per_parts") == {"t2-4c": {"normal": 1, "facil": 1}}
    assert await repo.availability() == {"t2-4c": {"normal": 1}}


async def test_rows_written_without_a_layout_are_sencer(session_provider: SQLModelSessionProvider) -> None:
    """What every row written before layouts existed gets from the database."""
    doc, sid = solution(), SessionId.generate()
    async with session_provider.begin() as db:
        connection = await db.connection()  # raw SQL: the records' Python-side default would fill the layout
        await connection.execute(
            text(
                "INSERT INTO mistake_exercises (id, source_kind, source_id, difficulty, created_at, data) "
                "VALUES (:id, 'problema', 't2-4c', 'normal', 1.0, :data)"
            ).bindparams(bindparam("data", type_=JsonColumn)),
            {"id": doc.id, "data": doc.model_dump(mode="json")},
        )
        await connection.execute(
            text(
                "INSERT INTO mistake_sessions (id, source_kind, source_id, exercise_id, difficulty, created_at) "
                "VALUES (:sid, 'problema', 't2-4c', :id, 'normal', 1.0)"
            ),
            {"sid": str(sid), "id": doc.id},
        )
    assert await SQLModelMistakeExerciseRepository(session_provider).of_source("t2-4c", "normal") == [doc]
    assert (await SQLModelMistakeSessionRepository(session_provider).get(sid)).layout == "sencer"


def parted_session_of(exercise_id: str = "0000000000bb") -> MistakeSession:
    return session_of(exercise_id).model_copy(update={"layout": "per_parts"})


def part_grading(part: int, hint_used: bool = False) -> PartGrading:
    return PartGrading(part=part, hint_used=hint_used, grading=grade(parted().view(part), [], None, None))


async def test_a_part_is_graded_once_and_the_session_reads_back_its_parts_and_hints(
    session_provider: SQLModelSessionProvider,
) -> None:
    exercises = SQLModelMistakeExerciseRepository(session_provider)
    sessions = SQLModelMistakeSessionRepository(session_provider)
    await exercises.save(parted())
    s = parted_session_of()
    await sessions.add(s)
    assert await sessions.get(s.id) == s
    await sessions.add_hint(s.id, 3, 11.0)
    await sessions.add_hint(s.id, 3, 12.0)
    await sessions.save_part_grading(s.id, [], part_grading(3, hint_used=True), 13.0)
    annotations = [Annotation(id="a1", fragment=3, start=0, end=3, comment="?")]
    await sessions.save_part_grading(s.id, annotations, part_grading(2), 14.0)
    stored = await sessions.get(s.id)
    assert stored.layout == "per_parts" and stored.hinted_parts == [3] and stored.grading is None
    assert stored.part_gradings == [part_grading(2), part_grading(3, hint_used=True)]
    with pytest.raises(MistakePartAlreadyGradedException) as e:
        await sessions.save_part_grading(s.id, [], part_grading(2, hint_used=True), 15.0)
    assert e.value.error_code == 409
    assert (await sessions.get(s.id)).part_grading(2) == part_grading(2)


async def test_a_part_claim_is_the_session_claim_and_refuses_a_graded_part(
    session_provider: SQLModelSessionProvider,
) -> None:
    exercises = SQLModelMistakeExerciseRepository(session_provider)
    sessions = SQLModelMistakeSessionRepository(session_provider)
    await exercises.save(parted())
    s = parted_session_of()
    await sessions.add(s)
    assert await sessions.claim_part(s.id, 2, now=100.0, stale_before=0.0)
    assert not await sessions.claim_part(s.id, 3, now=101.0, stale_before=1.0)  # one claim per session
    await sessions.save_part_grading(s.id, [], part_grading(2), 102.0)
    await sessions.release_grading(s.id, claimed_at=100.0)
    assert not await sessions.claim_part(s.id, 2, now=103.0, stale_before=3.0)  # graded: never again
    assert await sessions.claim_part(s.id, 3, now=103.0, stale_before=3.0)


async def test_both_layouts_are_files_in_the_same_tree_and_both_are_imported(
    session_provider: SQLModelSessionProvider, tmp_path: Path
) -> None:
    files = JsonFileMistakeSource(tmp_path)
    assert files.save(parted()) == tmp_path / "t2-4c" / "normal" / "0000000000bb.json"
    files.save(solution())
    assert [type(d).__name__ for d in files.load_all()] == ["MistakeExercise", "PartedMistakeExercise"]
    assert files.load() == [solution()]
    repo = SQLModelMistakeExerciseRepository(session_provider)
    assert await PregeneratedImporter(files, repo).import_all() == 2
    assert await repo.of_source("t2-4c", "normal", "per_parts") == [parted()]
