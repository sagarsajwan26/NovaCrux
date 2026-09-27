from sqlalchemy.ext.asyncio import AsyncSession
from app.models.permission import Permission
from app.repositories.permission_repository import PermissionRepository
from app.seeds.permission import PERMISSIONS


class PermissionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.permission_repository = PermissionRepository(db)

    async def seed_permissions(self) -> list[Permission]:
        created_permissions: list[Permission] = []
        for definition in PERMISSIONS:
            existing_permission = (
                await self.permission_repository.get_by_resource_and_action(
                    resource=definition.resource, action=definition.action
                )
            )

            if existing_permission:
                continue

            permission = Permission(
                resource=definition.resource,
                action=definition.action,
                description=definition.description,
            )

            created_permission = await self.permission_repository.create(permission)

            created_permissions.append(created_permission)
        return created_permissions
