from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import TenantNotFoundError
from app.core.tenant.domain import normalize_domain
from app.repositories.tenant_domain_repository import TenantDomainRepository
from app.repositories.tenant_repository import TenantRepository


class TenantDomainService:
    def __init__(self, db: AsyncSession):
        self.db = db

        self.domain_repository = TenantDomainRepository(db)
        self.tenant_repository = TenantRepository(db)

    async def resolve_tenant_by_domain(self, domain: str):
        normalize_domain = normalize_domain(domain)
        tenant_domain = await self.domain_repository.get_by_domain(normalize_domain)

        if tenant_domain is None:
            raise TenantNotFoundError()

        tenant = await self.tenant_repository.get_by_id(tenant_domain.tenant_id)

        if tenant is None:
            raise TenantNotFoundError()

        return tenant
