
from fastapi import status


class AppException(Exception):

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: object | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details

        super().__init__(message)


class ResourceNotFoundError(AppException):

    def __init__(
        self,
        message: str = "Resource not found",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


class InvalidRequestError(AppException):

    def __init__(
        self,
        message: str = "Invalid request",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class PermissionDeniedError(AppException):

    def __init__(
        self,
        message: str = "Permission denied",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
        )


class ServiceCommunicationError(AppException):

    def __init__(
        self,
        message: str = "Service communication failed",
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

