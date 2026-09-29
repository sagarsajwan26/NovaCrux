from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tenant_settings import TenantSettings
from app.models.tenants import Tenant
from app.repositories.tenant_settings import TenantSettingsRepository
from app.repositories.tenant_repository import TenantRepository
from app.service.role import RoleService


class TenantService:
    def __init__(self, db: AsyncSession):
        self.db = db

        self.tenant_repository = TenantRepository(db)
        self.tenant_settings_repository = TenantSettingsRepository(db)
        self.role_service = RoleService(db)

    async def create_tenant(
        self,
        name: str,
        slug: str,
    ) -> Tenant:
        existing_tenant = await self.tenant_repository.get_by_slug(slug)

        if existing_tenant:
            raise ValueError(f'Tenant with slug "{slug} already exists."')

        tenant = Tenant(name=name, slug=slug)

        tenant = await self.tenant_repository.create(tenant)

        tenant_settings = TenantSettings(tenant_id=tenant.id)

        tenant_settings = await self.tenant_settings_repository.create(tenant_settings)

        await self.role_service.create_default_roles(tenant_id=tenant.id)

        return tenant
