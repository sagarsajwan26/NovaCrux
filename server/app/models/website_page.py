from datetime import datetime
from enum import Enum
from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class PageStatus(str, Enum):
    DRAFT = "draft"
    PREVIEW = "preview"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class WebsitePage(Base):
    __tablename__ = "website_pages"
    __table_args__ = (
        UniqueConstraint("website_id", "slug", name="uq_website_pages_website_slug"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    website_id: Mapped[int] = mapped_column(
        ForeignKey("websites.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    status: Mapped[PageStatus] = mapped_column(
        SQLEnum(
            PageStatus,
            name="page_status",
            values_callable=lambda enum: [item.value for item in enum],
        ),
        nullable=False,
        default=PageStatus.DRAFT,
        server_default=PageStatus.DRAFT.value,
        index=True,
    )
    meta_title: Mapped[str | None] = mapped_column(String(255), nullable=True)

    meta_description: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default="now()",
        onupdate=datetime.utcnow,
    )

    website: Mapped["Website"] = relationship(
        back_populates="pages",
    )

    sections: Mapped[list["WebsiteSection"]] = relationship(
        back_populates="page",
        cascade="all, delete-orphan",
        order_by="WebsiteSection.position",
    )
