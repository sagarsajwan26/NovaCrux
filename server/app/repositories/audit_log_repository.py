from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog


class AuditLogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, audit_log: AuditLog) -> AuditLog:
        self.db.add(audit_log)
        await self.db.flush()
        await self.db.refresh(audit_log)
        return audit_log

    async def get_by_tenant_id(
        self,
        tenant_id: int,
    ) -> list[AuditLog]:
        result = await self.db.execute(
            select(AuditLog)
            .where(AuditLog.tenant_id == tenant_id)
            .order_by(AuditLog.created_at.desc())
        )

        return list(result.scalars().all())

    async def get_by_user_id(
        self,
        user_id: int,
    ) -> list[AuditLog]:
        result = await self.db.execute(
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
            .order_by(AuditLog.created_at.desc())
        )
        return list(result.scalars().all())
