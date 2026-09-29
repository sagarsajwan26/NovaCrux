from datetime import datetime, timedelta, timezone
import re
import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import InvalidTokenError
from app.core.exceptions import (
    UserAlreadyExistsError,
    SessionNotFoundError,
    SessionRevokedError,
    SessionExpiredError,
    UserNotFoundError,
    InactiveUserError,
)
from app.core.security.security import hash_password
from app.core.security.tokens import (
    create_access_token,
    generate_refresh_token,
    hash_refresh_token,
)
from app.models.audit_log import AuditLog
from app.models.membership import Membership
from app.models.sessions import Session
from app.models.user import User
from app.models.user_consent import UserConsent
from app.repositories.audit_log_repository import AuditLogRepository
from app.repositories.user_consent import UserConsentRepository
from app.service.tenant import TenantService
from app.repositories.user_repository import UserRepository
from app.repositories.session_repository import SessionRepository
from app.repositories.tenant_repository import TenantRepository
from app.repositories.membership_repository import MembershipRepository
from app.repositories.role_repository import RoleRepository


class AuthService:
    def __init__(self, db: AsyncSession):

        self.db = db

        self.user_repository = UserRepository(db)
        self.session_repository = SessionRepository(db)
        self.tenant_repository = TenantRepository(db)
        self.membership_repository = MembershipRepository(db)
        self.role_repository = RoleRepository(db)

        self.user_consent_repository = UserConsentRepository(db)
        self.audit_log_repository = AuditLogRepository(db)
        self.tenant_service = TenantService(db)

    async def register(
        self,
        email: str,
        password: str,
        first_name: str | None,
        last_name: str,
        tenant_name: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ):
        async with self.db.begin():
            existing_user = await self.user_repository.get_by_email(email)
            if existing_user:
                raise UserAlreadyExistsError()

            slug = await self._generate_unique_slug(tenant_name)

            user = User(
                email=email.lower(),
                password_hash=hash_password(password),
                first_name=first_name,
                last_name=last_name,
            )

            user = await self.user_repository.create(user)

            tenant = await self.tenant_service.create_tenant(
                name=tenant_name, slug=slug
            )

            admin_role = await self.role_repository.get_by_name(
                tenant_id=tenant.id, name="Admin"
            )

            if admin_role is None:
                raise RuntimeError("Default Admin role was not created.")

            membership = Membership(
                tenant_id=tenant.id,
                user_id=user.id,
                role_id=admin_role.id,
                is_active=True,
            )

            await self.membership_repository.create(membership)

            consent = UserConsent(
                user_id=user.id,
                consent_type="terms_and_privacy",
                policy_version="1.0",
                ip_address=ip_address,
                user_agent=user_agent,
            )

            await self.user_consent_repository.create(consent)

            refresh_token = generate_refresh_token()
            refresh_token_hash = hash_refresh_token(refresh_token)

            session = Session(
                user_id=user.id,
                session_token_hash=refresh_token_hash,
                expires_at=datetime.now(timezone.utc) + timedelta(days=30),
                ip_address=ip_address,
                user_agent=user_agent,
            )

            session = await self.session_repository.create(session)

            access_token = create_access_token(user_id=user.id, session_id=session.id)

            audit_log = AuditLog(
                tenant_id=tenant.id,
                user_id=user.id,
                action="user.registered",
                resource_type="user",
                resource_id=str(user.id),
                description="User registered and tenant was created.",
                ip_address=ip_address,
            )

            await self.audit_log_repository.create(audit_log)

            return {
                "user": user,
                "tenant": tenant,
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

    async def _generate_unique_slug(self, tenant_name: str) -> str:
        base_slug = re.sub(
            r"[^a-z0-9]+",
            "-",
            tenant_name.lower(),
        ).strip("-")

        if not base_slug:
            base_slug = "tenant"

        slug = base_slug

        while await self.tenant_repository.exists_by_slug(slug):
            slug = f"{base_slug}-{secrets.token_hex(3)}"

        return slug

    async def refresh_access_token(
        self,
        refresh_token: str,
    ):
        token_hash = hash_refresh_token(refresh_token)

        session = await self.session_repository.get_by_token_hash(token_hash)

        if session is None:
            raise SessionNotFoundError()

        now = datetime.now(timezone.utc)

        if session.revoked_at is not None:
            raise SessionRevokedError()

        if session.expires_at <= now:
            raise SessionExpiredError()

        user = await self.user_repository.get_by_id(session.user_id)

        if user is None:
            raise UserNotFoundError()
        if not user.is_active:
            raise InactiveUserError()

        access_token = create_access_token(user_id=user.id, session_id=session.id)

        return access_token

    async def logout(self, refresh_token: str):
        token_hash = hash_refresh_token(refresh_token)

        session = await self.session_repository.get_by_token_hash(token_hash)
        if session is None:
            return

        if session.revoked_at is not None:
            return

        await self.session_repository.revoke(
            session=session, revoked_at=datetime.now(timezone.utc)
        )
