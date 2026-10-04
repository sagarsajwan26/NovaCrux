from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tenants import Tenant


class TenantRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, tenant: Tenant) -> Tenant:
        self.db.add(tenant)
        await self.db.flush()
        return tenant

    async def get_by_id(self, tenant_id: int) -> Tenant | None:
        result = await self.db.execute(select(Tenant).where(Tenant.id == tenant_id))
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Tenant | None:
        result = await self.db.execute(select(Tenant).where(Tenant.slug == slug))

        return result.scalar_one_or_none()

    async def exists_by_slug(self, slug: str) -> bool:
        result = await self.db.execute(
            select(Tenant.id).where(Tenant.slug == slug).limit(1)
        )

        return result.scalar_one_or_none() is not None
