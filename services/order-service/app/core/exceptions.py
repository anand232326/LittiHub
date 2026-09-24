
class AppException(Exception):

    def __init__(
        self,
        message: str,
        status_code: int = 400,
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
        details: object | None = None,
    ):
        super().__init__(
            message=message,
            status_code=404,
            details=details,
        )


class ResourceAlreadyExistsError(AppException):

    def __init__(
        self,
        message: str = "Resource already exists",
        details: object | None = None,
    ):
        super().__init__(
            message=message,
            status_code=409,
            details=details,
        )


class PermissionDeniedError(AppException):

    def __init__(
        self,
        message: str = "Permission denied",
        details: object | None = None,
    ):
        super().__init__(
            message=message,
            status_code=403,
            details=details,
        )


class InvalidRequestError(AppException):

    def __init__(
        self,
        message: str = "Invalid request",
        details: object | None = None,
    ):
        super().__init__(
            message=message,
            status_code=400,
            details=details,
        )


class ServiceCommunicationError(AppException):

    def __init__(
        self,
        message: str = "Service communication failed",
        details: object | None = None,
    ):
        super().__init__(
            message=message,
            status_code=503,
            details=details,
        )

