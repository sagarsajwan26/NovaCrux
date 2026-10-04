from datetime import datetime
from enum import Enum
from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Integer, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base


class SectionType(str, Enum):
    HERO = "hero"
    TEXT = "text"
    RICH_TEXT = "rich_text"
    IMAGE = "image"
    VIDEO = "video"
    CTA = "cta"
    POLICY_LIST = "policy_list"
    DOCUMENT_LIST = "document_list"
    CERTIFICATION_LIST = "certification_list"
    SUBPROCESSOR_LIST = "subprocessor_list"
    FAQ = "faq"
    CONTACT = "contact"
    LOGO_CLOUD = "logo_cloud"
    STATISTICS = "statistics"
    TESTIMONIALS = "testimonials"
    FEATURES = "features"
    FOOTER = "footer"


class WebsiteSection(Base):
    __tablename__ = "website_sections"

    __table_args__ = (
        UniqueConstraint(
            "page_id",
            "position",
            name="uq_website_sections_page_position",
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    page_id: Mapped[int] = mapped_column(
        ForeignKey("website_pages.id", ondelete="CASCADE"), nullable=False, index=True
    )

    section_type: Mapped[SectionType] = mapped_column(
        SQLEnum(
            SectionType,
            name="section_type",
            values_callable=lambda enum: [item.value for item in enum],
        ),
        nullable=False,
    )

    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    content: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict, server_default="{}"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )
    page: Mapped["WebsitePage"] = relationship(back_populates="sections")
