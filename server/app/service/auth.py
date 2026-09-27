from sqlalchemy.ext.asyncio import AsyncSession
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
