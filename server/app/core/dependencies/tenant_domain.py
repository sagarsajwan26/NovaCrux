from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.service.tenant_domain import TenantDomainService
from app.core.exceptions import TenantNotFoundError


async def get_tenant_from_domain(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    host = request.headers.get("host")
    if not host:
        raise TenantDomainService()

    tenant_domain_service = TenantDomainService(db)
    tenant = await tenant_domain_service.resolve_tenant_by_domain(host)

    return tenant
