from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.models.membership import Membership
from app.models.subscription import Subscription, SubscriptionStatus
from app.models.website import Website
from app.repositories.membership_repository import MembershipRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.plan_repository import PlanRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.service.tenant import TenantService
from app.models.plans import PlanCode
from app.models.TenantDomain import TenantDomain, TenantDomainType
from app.repositories.tenant_domain_repository import TenantDomainRepository


class OnboardingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tenant_service = TenantService(db)
        self.role_repository = RoleRepository(db)
        self.membership_repository = MembershipRepository(db)
        self.plan_repository = PlanRepository(db)
        self.subscription_repository = SubscriptionRepository(db)
        self.tenant_domain_repository = TenantDomainRepository(db)

    async def provision_tenant(
        self,
        user_id: int,
        tenant_name: str,
        slug: str,
        app_env: str = "development",
        trial_days: int = 1,
    ):
        # 1. Tenant, TenantSettings, Default Roles
        tenant = await self.tenant_service.create_tenant(name=tenant_name, slug=slug)

        # 2. Membership for the creator
        admin_role = await self.role_repository.get_by_name(
            tenant_id=tenant.id, name="Admin"
        )
        if admin_role is None:
            raise RuntimeError("Default Admin role was not created.")

        membership = Membership(
            tenant_id=tenant.id,
            user_id=user_id,
            role_id=admin_role.id,
            is_active=True,
        )
        await self.membership_repository.create(membership)

        # 3. Trial Subscription
        free_plan = await self.plan_repository.get_by_code(PlanCode.FREE)
        if free_plan is None:
            raise RuntimeError("Free plan not found.")

        now = datetime.now(timezone.utc)
        trial_ends = now + timedelta(days=trial_days)

        subscription = Subscription(
            tenant_id=tenant.id,
            plan_id=free_plan.id,
            status=SubscriptionStatus.TRIALING,
            trial_started_at=now,
            trial_ends_at=trial_ends,
            current_period_start=now,
            current_period_end=trial_ends,
        )
        await self.subscription_repository.create(subscription)

        # 4. Default Website Shell
        website = Website(
            tenant_id=tenant.id,
            name=f"{tenant_name} Website",
            is_active=True,
        )

        self.db.add(website)
        tenant_domain = TenantDomainRepository(
            tenant_id=tenant.id,
            domain=f"{tenant.slug}.{settings.tenant_base_domain}",
            domain_type=TenantDomainType.SUBDOMAIN,
            is_primary=True,
            is_verified=True,
        )

        await self.tenant_domain_repository.create(tenant_domain)

        await self.db.flush()

        return tenant
