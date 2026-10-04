from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String, func

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Website(Base):
    __tablename__ = "websites"
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )
    tenant_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    tenant: Mapped["Tenant"] = relationship(back_populates="website")

    pages: Mapped[list["WebsitePage"]] = relationship(
        back_populates="website", cascade="all, delete-orphan"
    )
