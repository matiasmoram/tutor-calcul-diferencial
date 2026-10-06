from core.course.application.course_importer import CourseImporter
from core.course.application.course_loader import CourseLoader
from core.course.infra.sqlmodel_repository import SQLModelCourseRepository
from core.shared.storage.session_provider import SQLModelSessionProvider
from tests.fixtures.course import authored_course, authored_source


async def test_the_course_round_trips_through_the_database(session_provider: SQLModelSessionProvider) -> None:
    repo = SQLModelCourseRepository(session_provider)
    assert await repo.load() is None and await repo.count_exercises() == 0
    summary = await CourseImporter(authored_source(), repo).import_course()
    original = authored_course()
    assert summary.exercises == len(original.exercises) == await repo.count_exercises()
    stored = await repo.load()
    assert stored == original
    assert list(stored.exercises) == list(original.exercises)  # order of the sheets is kept


async def test_reimport_replaces_the_content(session_provider: SQLModelSessionProvider) -> None:
    repo = SQLModelCourseRepository(session_provider)
    importer = CourseImporter(authored_source(), repo)
    await importer.import_course()
    await importer.import_course()
    assert await repo.count_exercises() == len(authored_course().exercises)


async def test_the_loader_imports_on_first_start_then_reads_the_database(
    session_provider: SQLModelSessionProvider,
) -> None:
    repo = SQLModelCourseRepository(session_provider)

    class CountingSource:
        loads = 0

        def load(self):
            CountingSource.loads += 1
            return authored_course()

    loader = CourseLoader(repo, CountingSource())
    assert (await loader.load()) == authored_course() and CountingSource.loads == 1
    assert (await loader.load()) == authored_course() and CountingSource.loads == 1
