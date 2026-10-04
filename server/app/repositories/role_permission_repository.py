from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.role_permission import RolePermission


class RolePermissionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, role_permission: RolePermission) -> RolePermission:
        self.db.add(role_permission)
        await self.db.flush()
        await self.db.refresh(role_permission)

        return role_permission

    async def exists(self, role_id: int, permission_id: int) -> bool:
        result = await self.db.execute(
            select(RolePermission.id)
            .where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id,
            )
            .limit(1)
        )

        return result.scalar_one_or_none() is not None

    async def get_permission_ids_for_role(
        self,
        role_id: int,
    ) -> list[int]:
        result = await self.db.execute(
            select(RolePermission.permission_id).where(
                RolePermission.role_id == role_id
            )
        )
        return list(result.scalars().all())

    async def get_role_ids_for_permission(
        self,
        permission_id: int,
    ) -> list[int]:
        result = await self.db.execute(
            select(RolePermission.role_id).where(
                RolePermission.permission_id == permission_id
            )
        )
        return list(result.scalars().all())
