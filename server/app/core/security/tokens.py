import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings


def create_access_token(
    user_id: int, session_id: int, expires_minutes: int = 15
) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "session_id": str(session_id),
        "iat": now,
        "exp": now + timedelta(minutes=expires_minutes),
    }

    return jwt.encode(
        payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def decode_access_token(token: str) -> dict:

    return jwt.decode(
        token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
    )


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def hash_refresh_token(refresh_token: str) -> str:
    return hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()
