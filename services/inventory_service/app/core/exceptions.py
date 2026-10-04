class AppException(Exception):

    def __init__(
        self,
        status_code: int,
        message: str,
        details=None,
    ):
        self.status_code = status_code
        self.message = message
        self.details = details

        super().__init__(message)


class InvalidRequestError(AppException):

    def __init__(
        self,
        message: str,
        details=None,
    ):
        super().__init__(
            status_code=400,
            message=message,
            details=details,
        )


class ResourceNotFoundError(AppException):

    def __init__(
        self,
        message: str,
        details=None,
    ):
        super().__init__(
            status_code=404,
            message=message,
            details=details,
        )

class PermissionDeniedError(AppException):

    def __init__(
        self,
        message: str = "Permission denied",
        details=None,
    ):
        super().__init__(
            status_code=403,
            message=message,
            details=details,
        )        

