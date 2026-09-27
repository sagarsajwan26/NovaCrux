from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.role import Role


class RoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, role: Role) -> Role:
        self.db.add(role)
        await self.db.flush()
        await self.db.refresh(role)

        return role

    async def get_by_id(self, role_id: int, tenant_id: int) -> Role | None:
        result = await self.db.execute(
            select(Role).where(Role.id == role_id, Role.tenant_id == tenant_id)
        )

        return result.scalar_one_or_none()

    async def get_by_name(
        self,
        tenant_id: int,
        name: str,
    ) -> Role | None:
        result = await self.db.execute(
            select(Role).where(Role.tenant_id == tenant_id, Role.name == name)
        )

        return result.scalar_one_or_none()

    async def exists_by_name(self, tenant_id: int, name: str) -> bool:
        result = await self.db.execute(
            select(Role.id)
            .where(Role.tenant_id == tenant_id, Role.name == name)
            .limit(1)
        )

        return result.scalar_one_or_none() is not None
