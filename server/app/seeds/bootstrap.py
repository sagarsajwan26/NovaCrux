import asyncio

from app.db.session import AsyncSessionLocal
from app.seeds.users import seed_platform_users
from app.service.permission import PermissionService
from app.service.plan import PlanService


async def bootstrap() -> None:
    async with AsyncSessionLocal() as db:
        try:
            permission_service = PermissionService(db)
            plan_service = PlanService(db)

            await permission_service.seed_permissions()

            await plan_service.seed_plans()

            await seed_platform_users(db)

            await db.commit()

            print("NovaCrux bootstrap completed successfully.")

        except Exception:
            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(bootstrap())
