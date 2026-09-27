from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tenant_settings import TenantSettings


class TenantSettingsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, tenant_settings: TenantSettings) -> TenantSettings:
        self.db.add(tenant_settings)

        await self.db.flush()
        await self.db.refresh(tenant_settings)

        return tenant_settings

    async def get_by_tenant_id(
        self,
        tenant_id: int,
    ) -> TenantSettings:
        result = await self.db.execute(
            select(TenantSettings).where(TenantSettings.tenant_id == tenant_id)
        )

        return result.scalar_one_or_none()
