from app.core.exceptions.base import AppException


class TenantAccessDeniedError(AppException):
    def __init__(self):
        super().__init__(
            message="You do not have access to this tenant.",
            status_code=403,
            code="tenant_access_denied",
        )


class PermissionDeniedError(AppException):
    def __init__(self):
        super().__init__(
            message="You do not have permission to perform this action.",
            status_code=403,
            code="permission_denied",
        )
