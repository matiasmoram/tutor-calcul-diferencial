import base64

import pytest
from sqlmodel import select

from core.shared.llm.client import Image, Stage
from core.shared.storage.session_provider import SQLModelSessionProvider
from core.tutoring.application.photo_transcriber import PhotoTranscriberInput
from core.tutoring.domain.exceptions import InvalidPhotoException
from core.tutoring.domain.values.photo import Photo
from core.tutoring.infra.sqlmodel_repository import TranscriptionRecord
from tests.core.tutoring.builders import EX4C, tutoring
from tests.fakes.llm import ScriptedLLMClient


def test_photo_validation() -> None:
    assert Photo(b"x", "image/png").media_type == "image/png"
    for data, media_type in (
        (b"x", "application/pdf"),
        (b"", "image/jpeg"),
        (b"x" * (6 * 1024 * 1024 + 1), "image/jpeg"),
    ):
        with pytest.raises(InvalidPhotoException) as e:
            Photo(data, media_type)
        assert e.value.error_code == 400


def test_photo_from_a_data_url() -> None:
    photo = Photo.from_data_url("data:image/png;base64," + base64.b64encode(b"fakepng").decode())
    assert photo == Photo(b"fakepng", "image/png")
    with pytest.raises(InvalidPhotoException, match="Format no admès"):
        Photo.from_data_url("data:application/pdf;base64,AAAA")
    for bad in ("no comma", "data:image/png,AAAA", "data:image/png;base64,***"):
        with pytest.raises(InvalidPhotoException, match="data URL"):
            Photo.from_data_url(bad)


async def test_transcription_sends_the_photo_and_keeps_the_student_text_verbatim(
    session_provider: SQLModelSessionProvider,
) -> None:
    llm = ScriptedLLMClient(
        {
            Stage.TRANSCRIPTION: [
                {
                    "transcripcio": "  $y=kx$ dona 0, per tant el límit és 0  ",
                    "llegibilitat": "bona",
                    "contingut": "treball_matematic",
                    "dubtes": [],
                }
            ]
        }
    )
    t = tutoring(llm, session_provider)
    sid = (await t.starter.start(EX4C.id)).session.id
    photo = Photo(b"PNG", "image/png")
    out = await t.transcriber.transcribe(PhotoTranscriberInput(session_id=sid, photo=photo))
    assert out.transcription.text == "$y=kx$ dona 0, per tant el límit és 0"
    assert out.transcription.model_dump()["llegibilitat"] == "bona" and out.call.stage == "transcription"
    [request] = llm.requests[Stage.TRANSCRIPTION]
    assert request.image == Image(b"PNG", "image/png") and EX4C.statement_md() in request.user
    async with session_provider.begin() as db:
        [stored] = (await db.exec(select(TranscriptionRecord))).all()
    assert stored.session_id == sid and stored.result["transcripcio"] == out.transcription.text
