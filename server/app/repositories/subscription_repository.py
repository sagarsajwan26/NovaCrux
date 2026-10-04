from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.subscription import Subscription, SubscriptionStatus


class SubscriptionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        subscription: Subscription,
    ) -> Subscription:
        self.db.add(subscription)
        await self.db.flush()
        await self.db.refresh(subscription)
        return subscription

    async def get_by_id(
        self,
        subscription_id: int,
    ) -> Subscription | None:
        result = await self.db.execute(
            select(Subscription).where(Subscription.id == subscription_id)
        )

        return result.scalar_one_or_none()

    async def get_by_tenant_id(
        self,
        tenant_id: int,
    ) -> Subscription | None:
        result = await self.db.execute(
            select(Subscription).where(
                Subscription.tenant_id == tenant_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_active_by_tenant_id(
        self,
        tenant_id: int,
    ) -> Subscription | None:
        result = await self.db.execute(
            select(Subscription).where(
                Subscription.tenant_id == tenant_id,
                Subscription.status.in_(
                    [
                        SubscriptionStatus.TRIALING,
                        SubscriptionStatus.ACTIVE,
                    ]
                ),
            )
        )

        return result.scalar_one_or_none()

    async def get_by_provider_subscription_id(
        self,
        provider_subscription_id: str,
    ) -> Subscription | None:
        result = await self.db.execute(
            select(Subscription).where(
                Subscription.provider_subscription_id == provider_subscription_id,
            )
        )

        return result.scalar_one_or_none()
