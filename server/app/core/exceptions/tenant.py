from app.core.exceptions.base import AppException


class TenantNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            message="Tenant not found.",
            status_code=404,
            code="tenant_not_found",
        )
