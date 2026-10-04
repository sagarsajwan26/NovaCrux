from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.plan_entitlement import PlanEntitlement


class PlanEntitlementRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        entitlement: PlanEntitlement,
    ) -> PlanEntitlement:
        self.db.add(entitlement)

        await self.db.flush()
        await self.db.refresh(entitlement)

        return entitlement

    async def get_by_id(
        self,
        entitlement_id: int,
    ) -> PlanEntitlement | None:
        result = await self.db.execute(
            select(PlanEntitlement).where(
                PlanEntitlement.id == entitlement_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_plan_and_feature(
        self,
        plan_id: int,
        feature_key: str,
    ) -> PlanEntitlement | None:
        result = await self.db.execute(
            select(PlanEntitlement).where(
                PlanEntitlement.plan_id == plan_id,
                PlanEntitlement.feature_key == feature_key,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_plan_id(
        self,
        plan_id: int,
    ) -> list[PlanEntitlement]:
        result = await self.db.execute(
            select(PlanEntitlement)
            .where(
                PlanEntitlement.plan_id == plan_id,
            )
            .order_by(
                PlanEntitlement.feature_key.asc(),
            )
        )

        return list(result.scalars().all())
