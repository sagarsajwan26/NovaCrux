from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.TenantDomain import TenantDomain


class TenantDomainRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, tenant_domain: TenantDomain) -> TenantDomain:
        self.db.add(tenant_domain)
        await self.db.flush()
        await self.db.refresh(tenant_domain)
        return tenant_domain

    async def get_by_domain(
        self,
        domain: str,
    ) -> TenantDomain | None:
        result = await self.db.execute(
            select(TenantDomain).where(TenantDomain.domain == domain.lower())
        )

        return result.scalar_one_or_none()

    async def get_primary_by_tenant_id(
        self,
        tenant_id: int,
    ) -> TenantDomain | None:
        result = await self.db.execute(
            select(TenantDomain).where(
                TenantDomain.tenant_id == tenant_id, TenantDomain.is_primary.is_(True)
            )
        )

        return result.scalar_one_or_none()
