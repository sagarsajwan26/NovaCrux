from datetime import datetime, timezone
from fastapi import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.core.exceptions import InactiveUserError, InvalidTokenError, UserNotFoundError
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.core.security.tokens import decode_access_token


async def get_current_user(
    access_token: str | None = Cookie(default=None), db: AsyncSession = Depends(get_db)
):
    if not access_token:
        raise InvalidTokenError()

    try:
        payload = decode_access_token(access_token)

    except Exception:
        raise InvalidTokenError()

    user_id = payload.get("sub")
    session_id = payload.get("session_id")
    if not user_id or not session_id:
        raise InvalidTokenError()

    try:
        user_id = int(user_id)
        session_id = int(session_id)

    except (TypeError, ValueError):
        raise InvalidTokenError()

    user_repository = UserRepository(db)
    session_repository = SessionRepository(db)

    user = await user_repository.get_by_id(user_id)
    if user is None:
        raise UserNotFoundError()

    if not user.is_active:
        raise InactiveUserError()

    session = await session_repository.get_by_id(session_id)

    if session is None:
        raise InvalidTokenError()

    if session.user_id != user.id:
        raise InvalidTokenError()

    if session.revoked_at is not None:
        raise InvalidTokenError()
        
    if session.expires_at <= datetime.now(timezone.utc):
        raise InvalidTokenError()

    return user
