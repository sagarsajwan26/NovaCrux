from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_consent import UserConsent


class UserConsentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, consent: UserConsent) -> UserConsent:
        self.db.add(consent)

        await self.db.flush()
        await self.db.refresh(consent)
        return consent

    async def get_by_user_id(self, user_id: int) -> list[UserConsent]:
        result = await self.db.execute(
            select(UserConsent)
            .where(UserConsent.user_id == user_id)
            .order_by(UserConsent.accepted_at.desc())
        )

        return list(result.scalars().all())
