from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.plan_entitlement_repository import PlanEntitlementRepository
from app.repositories.subscription_repository import SubscriptionRepository


class EntitlementService:
    def __init__(self, db: AsyncSession):
        self.db = db

        self.subscription_repository = SubscriptionRepository(db)
        self.entitlement_repository = PlanEntitlementRepository(db)

    async def get_tenant_entitlement(self, tenant_id: int, feature_key: str):
        subscription = await self.subscription_repository.get_active_by_tenant_id(
            tenant_id=tenant_id
        )

        if subscription is None:
            return None

        entitlement = await self.entitlement_repository.get_by_plan_and_feature(
            plan_id=subscription.plan_id, feature_key=feature_key
        )

        return entitlement

    async def is_enabled(
        self,
        tenant_id: int,
        feature_key: str,
    ) -> bool:
        entitlement = await self.get_tenant_entitlement(
            tenant_id=tenant_id, feature_key=feature_key
        )

        if entitlement is None:
            return False

        return entitlement.enabled

    async def get_limit(self, tenant_id: int, feature_key: str) -> int | None:
        entitlement = await self.get_tenant_entitlement(
            tenant_id=tenant_id, feature_key=feature_key
        )

        if entitlement is None:
            return None
        return entitlement.limit_value
