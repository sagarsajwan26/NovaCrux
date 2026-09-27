from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.models.sessions import Session


class SessionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, session: Session) -> Session:
        self.db.add(session)
        await self.db.flush()
        await self.db.refresh(session)

        return session

    async def get_by_id(
        self,
        session_id: int,
    ) -> Session | None:
        result = await self.db.execute(
            select(Session).where(
                Session.id == session_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_token_hash(self, token_hash: str) -> Session | None:
        result = await self.db.execute(
            select(Session).where(Session.session_token_hash == token_hash)
        )

        return result.scalar_one_or_none()

    async def get_active_by_token_hash(
        self, token_hash: str, now: datetime
    ) -> Session | None:
        result = await self.db.execute(
            Session.session_token_hash == token_hash,
            Session.revoked_at.is_(None),
            Session.expires_at > now,
        )
        return result.scalar_one_or_none()

    async def revoke(self, session: Session, revoked_at: datetime) -> Session:
        session.revoked_at = revoked_at
        await self.db.flush()
        await self.db.refresh(session)

        return session

    async def revoke_all_for_user(self, user_id: int, revoked_at: datetime) -> int:

        result = await self.db.execute(
            select(Session).where(
                Session.user_id == user_id,
                Session.revoked_at.is_(None),
            )
        )
        sessions = result.scalars().all()

        for session in sessions:
            session.revoked_at == revoked_at

        await self.db.flush()
        return len(sessions)
