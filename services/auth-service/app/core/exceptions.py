
from typing import Any


class AppException(Exception):
    """
    Base application exception for expected business/API errors.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        details: Any = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details

        super().__init__(message)


class AuthenticationError(AppException):
    """
    Raised when authentication fails.
    """

    def __init__(
        self,
        message: str = "Invalid email or password",
    ):
        super().__init__(
            message=message,
            status_code=401,
        )


class AuthorizationError(AppException):
    """
    Raised when an authenticated user does not have
    permission to perform an operation.
    """

    def __init__(
        self,
        message: str = "You do not have permission to perform this action",
    ):
        super().__init__(
            message=message,
            status_code=403,
        )


class ResourceNotFoundError(AppException):
    """
    Raised when a requested resource does not exist.
    """

    def __init__(
        self,
        message: str = "Resource not found",
    ):
        super().__init__(
            message=message,
            status_code=404,
        )


class ResourceAlreadyExistsError(AppException):
    """
    Raised when trying to create a resource that already exists.
    """

    def __init__(
        self,
        message: str = "Resource already exists",
    ):
        super().__init__(
            message=message,
            status_code=409,
        )

