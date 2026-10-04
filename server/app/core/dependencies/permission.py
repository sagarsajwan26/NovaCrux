from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies.auth import get_current_user
from app.core.dependencies.tenant import get_current_tenant_membership
from app.core.exceptions import PermissionDeniedError
from app.db.session import get_db
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_permission_repository import RolePermissionRepository


def required_permission(resource: str, action: str):
    async def permission_dependency(
        tenant_id: int = Path(...),
        current_user=Depends(get_current_user),
        membership=Depends(get_current_tenant_membership),
        db: AsyncSession = Depends(get_db),
    ):
        if (
            membership.user_id != current_user.id
            or membership.tenant_id != tenant_id
            or not membership.is_active
        ):
            raise PermissionDeniedError()

        permission_repository = PermissionRepository(db)
        role_permission_repository = RolePermissionRepository(db)

        permission = await permission_repository.get_by_resource_and_action(
            resource=resource, action=action
        )

        if permission is None:
            raise PermissionDeniedError()

        has_permission = await role_permission_repository.exists(
            role_id=membership.role_id, permission_id=permission.id
        )
        if not has_permission:
            raise PermissionDeniedError()

        return membership

    return permission_dependency
