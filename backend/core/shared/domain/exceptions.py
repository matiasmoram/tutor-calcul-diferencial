class DomainException(Exception):
    """Base of every context's exceptions. ``error_code`` is the HTTP status the API layer translates this to."""

    def __init__(self, message: str, error_code: int) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
