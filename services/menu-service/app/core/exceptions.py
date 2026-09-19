from typing import Any


class AppException(Exception):

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

    def __init__(
        self,
        message: str = "Invalid or expired access token",
    ):
        super().__init__(
            message=message,
            status_code=401,
        )


class PermissionDeniedError(AppException):

    def __init__(
        self,
        message: str = "You do not have permission to perform this action",
    ):
        super().__init__(
            message=message,
            status_code=403,
        )


class ResourceNotFoundError(AppException):

    def __init__(
        self,
        message: str = "Resource not found",
    ):
        super().__init__(
            message=message,
            status_code=404,
        )


class ResourceAlreadyExistsError(AppException):

    def __init__(
        self,
        message: str = "Resource already exists",
    ):
        super().__init__(
            message=message,
            status_code=409,
        )