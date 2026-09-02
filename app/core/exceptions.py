class AppException(Exception):
    """Base exception for application-specific errors."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code

        super().__init__(message)


class UserAlreadyExistsError(AppException):
    """Raised when a user with the given email already exists."""

    def __init__(self):
        super().__init__(
            code="USER_ALREADY_EXISTS",
            message="A user with this email already exists.",
            status_code=409,
        )


class InvalidCredentialsError(AppException):
    """Raised when the provided login credentials are invalid."""

    def __init__(self):
        super().__init__(
            code="INVALID_CREDENTIALS",
            message="Invalid email or password.",
            status_code=401,
        )


class InvalidTokenError(AppException):
    """Raised when the provided JWT authentication token is invalid or expired."""

    def __init__(self):
        super().__init__(
            code="INVALID_TOKEN",
            message="Invalid or expired authentication token.",
            status_code=401,
        )



class PermissionDeniedError(AppException):

    def __init__(self,message: str = "You do not have permission to perform this action",):
        super().__init__(
            code="PERMISSION_DENIED",
            message=message,
            status_code=403,
        )
