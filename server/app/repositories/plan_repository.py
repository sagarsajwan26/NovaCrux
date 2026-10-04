from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.plans import Plan, PlanCode


class PlanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, plan: Plan) -> Plan:
        self.db.add(plan)

        await self.db.flush()
        await self.db.refresh(plan)

        return plan

    async def get_by_id(
        self,
        plan_id: int,
    ) -> Plan | None:
        result = await self.db.execute(
            select(Plan).where(
                Plan.id == plan_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_code(
        self,
        code: PlanCode,
    ) -> Plan | None:
        result = await self.db.execute(
            select(Plan).where(
                Plan.code == code,
            )
        )

        return result.scalar_one_or_none()

    async def get_active_by_code(
        self,
        code: PlanCode,
    ) -> Plan | None:
        result = await self.db.execute(
            select(Plan).where(
                Plan.code == code,
                Plan.is_active.is_(True),
            )
        )

        return result.scalar_one_or_none()

    async def get_all_active(self) -> list[Plan]:
        result = await self.db.execute(
            select(Plan)
            .where(
                Plan.is_active.is_(True),
            )
            .order_by(
                Plan.price.asc(),
            )
        )

        return list(result.scalars().all())

    async def exists_by_code(
        self,
        code: PlanCode,
    ) -> bool:
        result = await self.db.execute(
            select(Plan.id)
            .where(
                Plan.code == code,
            )
            .limit(1)
        )

        return result.scalar_one_or_none() is not None
