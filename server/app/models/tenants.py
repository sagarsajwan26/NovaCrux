from datetime import datetime
from enum import Enum
from sqlalchemy import (
    BigInteger,
    DateTime,
    String,
    Text,
    func,
    ForeignKey,
    Enum as SQLEnum,
)
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class TenantStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    slug: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[TenantStatus] = mapped_column(
        SQLEnum(
            TenantStatus,
            name="tenant_status",
            values_callable=lambda enum: [item.value for item in enum],
        ),
        nullable=False,
        default=TenantStatus.ACTIVE,
        server_default="active",
        index=True,
    )

    suspended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    suspended_by: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    suspension_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
