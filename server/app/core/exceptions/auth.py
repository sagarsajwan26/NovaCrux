from app.core.exceptions.base import AppException


class UserAlreadyExistsError(AppException):
    def __init__(self):
        super().__init__(
            message="A user with this email already exists.",
            status_code=409,
            code="user_already_exists",
        )


class InvalidCredentialsError(AppException):
    def __init__(self):
        super().__init__(
            message="Invalid email or password.",
            status_code=401,
            code="invalid_credentials",
        )


class UserNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            message="User not found.",
            status_code=404,
            code="user_not_found",
        )


class InactiveUserError(AppException):
    def __init__(self):
        super().__init__(
            message="User account is inactive.",
            status_code=403,
            code="user_inactive",
        )


class InvalidTokenError(AppException):
    def __init__(self):
        super().__init__(
            message="Invalid or expired authentication token.",
            status_code=401,
            code="invalid_token",
        )


class SessionNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            message="Session not found for the given token.",
            status_code=401,
            code="session_not_found",
        )


class SessionRevokedError(AppException):
    def __init__(self):
        super().__init__(
            message="This session has been revoked.",
            status_code=401,
            code="session_revoked",
        )


class SessionExpiredError(AppException):
    def __init__(self):
        super().__init__(
            message="This session has expired.",
            status_code=401,
            code="session_expired",
        )
