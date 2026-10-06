import base64
import binascii
from dataclasses import dataclass
from typing import ClassVar

from core.tutoring.domain.exceptions import InvalidPhotoException


@dataclass(frozen=True)
class Photo:
    """A photo of the student's notebook, checked on construction (format and size)."""

    MAX_BYTES: ClassVar[int] = 6 * 1024 * 1024
    MEDIA_TYPES: ClassVar[frozenset[str]] = frozenset({"image/jpeg", "image/png", "image/webp"})

    data: bytes
    media_type: str

    def __post_init__(self) -> None:
        if self.media_type not in self.MEDIA_TYPES:
            raise InvalidPhotoException(f"Format no admès ({self.media_type}). Fes servir JPG, PNG o WebP.")
        if not self.data:
            raise InvalidPhotoException("La imatge és buida.")
        if len(self.data) > self.MAX_BYTES:
            raise InvalidPhotoException(
                f"La imatge és massa gran ({len(self.data) // 1024} KB; màxim {self.MAX_BYTES // 1024 // 1024} MB)."
            )

    @classmethod
    def from_data_url(cls, url: str) -> "Photo":
        """``data:image/png;base64,...`` as the web sends it."""
        try:
            header, b64 = url.split(",", 1)
            if not header.endswith(";base64"):
                raise ValueError(header)
            data = base64.b64decode(b64, validate=True)
        except (ValueError, binascii.Error) as e:
            raise InvalidPhotoException("La imatge no és un data URL base64 vàlid.") from e
        return cls(data=data, media_type=header.removeprefix("data:").removesuffix(";base64"))
