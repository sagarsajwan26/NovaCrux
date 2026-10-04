from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.auth import get_current_user
from app.core.exceptions import TenantAccessDeniedError
from app.db.session import get_db
from app.repositories.membership_repository import MembershipRepository


async def get_current_tenant_membership(
    tenant_id: int = Path(...),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    membership_repository = MembershipRepository(db)

    membership = await membership_repository.get_active_by_user_and_tenant(
        user_id=current_user.id, tenant_id=tenant_id
    )
    if membership is None:
        raise TenantAccessDeniedError()

    return membership
