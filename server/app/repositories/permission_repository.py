from sqlalchemy import select
from app.models.permission import Permission
from sqlalchemy.ext.asyncio import AsyncSession


class PermissionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, permission: Permission) -> Permission:
        self.db.add(permission)
        await self.db.flush()
        await self.db.refresh(permission)

        return permission

    async def get_by_id(
        self,
        permission_id: int,
    ) -> Permission | None:
        result = await self.db.execute(
            select(Permission).where(Permission.id == permission_id)
        )

        return result.scalar_one_or_none()

    async def get_by_resource_and_action(
        self,
        resource: str,
        action: str,
    ) -> Permission | None:
        result = await self.db.execute(
            select(Permission).where(
                Permission.resource == resource, Permission.action == action
            )
        )
        return result.scalar_one_or_none()

    async def exists_by_resource_and_action(
        self,
        resource: str,
        action: str,
    ) -> bool:
        result = await self.db.execute(
            select(Permission.id)
            .where(Permission.resource == resource, Permission.action == action)
            .limit(1)
        )
        return result.scalar_one_or_none() is not None
