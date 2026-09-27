from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, func, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import INET
from app.models.base import Base


class UserConsent(Base):

    __tablename__ = "user_consents"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    consent_type: Mapped[str] = mapped_column(String(100), nullable=False)

    policy_version: Mapped[str] = mapped_column(String(50), nullable=False)

    accepted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    ip_address: Mapped[str | None] = mapped_column(
        INET,
        nullable=True,
    )
    user_agent: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
