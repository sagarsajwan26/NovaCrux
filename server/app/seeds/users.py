from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.security import hash_password
from app.models.user import PlatformRole, User
from app.repositories.user_repository import UserRepository

PLATFORM_USERS = (
    {
        "email": "superadmin@novacrux.com",
        "password": "NovaCrux@SuperAdmin2026",
        "first_name": "NovaCrux",
        "last_name": "Superadmin",
        "platform_role": PlatformRole.SUPERADMIN,
    },
    {
        "email": "admin@novacrux.com",
        "password": "NovaCrux@Admin2026",
        "first_name": "NovaCrux",
        "last_name": "Admin",
        "platform_role": PlatformRole.PLATFORM_ADMIN,
    },
)


async def seed_platform_users(
    db: AsyncSession,
) -> None:
    user_repository = UserRepository(db)

    for user_data in PLATFORM_USERS:
        existing_user = await user_repository.get_by_email(user_data["email"])

        if existing_user:
            continue

        user = User(
            email=user_data["email"],
            password_hash=hash_password(user_data["password"]),
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            platform_role=user_data["platform_role"],
            is_active=True,
            email_verified_at=datetime.now(timezone.utc),
        )

        await user_repository.create(user)
