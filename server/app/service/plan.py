from sqlalchemy.ext.asyncio import AsyncSession
from app.models.plans import Plan
from app.repositories.plan_repository import PlanRepository
from app.models.plan_entitlement import PlanEntitlement
from app.repositories.plan_entitlement_repository import (
    PlanEntitlementRepository,
)

from app.seeds.plans import PLAN_DEFINITIONS


class PlanService:
    def __init__(self, db: AsyncSession):
        self.db = db

        self.plan_repository = PlanRepository(db)
        self.entitlement_repository = PlanEntitlementRepository(db)

    async def seed_plans(self) -> list[Plan]:
        created_or_existed_plans: list[Plan] = []

        for definition in PLAN_DEFINITIONS:
            plan = await self.plan_repository.get_by_code(definition.code)
            if plan is None:
                plan = Plan(
                    code=definition.code,
                    name=definition.name,
                    description=definition.description,
                    billing_interval=definition.billing_interval,
                    price=definition.price,
                    is_active=True,
                )
                plan = await self.plan_repository.create(plan)
            created_or_existed_plans.append(plan)

            await self._seed_entitlements(
                plan=plan, entitlements=definition.entitlements
            )

        return created_or_existed_plans

    async def _seed_entitlements(
        self,
        plan: Plan,
        entitlements,
    ) -> None:

        for definition in entitlements:
            existing_entitlement = (
                await self.entitlement_repository.get_by_plan_and_feature(
                    plan_id=plan.id,
                    feature_key=definition.feature_key,
                )
            )

            if existing_entitlement:
                continue

            entitlement = PlanEntitlement(
                plan_id=plan.id,
                feature_key=definition.feature_key,
                enabled=definition.enabled,
                limit_value=definition.limit_value,
                config=definition.config,
            )

            await self.entitlement_repository.create(entitlement)
