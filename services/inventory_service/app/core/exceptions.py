class AppException(Exception):
    """Base exception for application-level errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidRequestError(AppException):
    """Raised when the request is invalid."""

    pass


class ResourceNotFoundError(AppException):
    """Raised when a requested resource does not exist."""

    pass