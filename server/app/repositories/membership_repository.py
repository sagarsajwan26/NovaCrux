from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.membership import Membership


class MembershipRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, membership: Membership) -> Membership:
        self.db.add(membership)
        await self.db.flush()

        await self.db.refresh(membership)

        return membership

    async def get_by_user_and_tenant(
        self, user_id: int, tenant_id: int
    ) -> Membership | None:
        result = await self.db.execute(
            select(Membership).where(
                Membership.user_id == user_id, Membership.tenant_id == tenant_id
            )
        )

        return result.scalar_one_or_none()

    async def get_active_by_user_and_tenant(
        self, user_id: int, tenant_id: int
    ) -> Membership | None:

        result = await self.db.execute(
            select(Membership).where(
                Membership.user_id == user_id,
                Membership.tenant_id == tenant_id,
                Membership.is_active.is_(True),
            )
        )

        return result.scalar_one_or_none()
