from app.models.website_section import SectionType
from app.schemas.website_sections import (
    CTASectionContent,
    FAQSectionContent,
    HeroSectionContent,
    RichTextSectionContent,
    TextSectionContent,
)

SECTION_SCHEMA = {
    SectionType.HERO: HeroSectionContent,
    SectionType.TEXT: TextSectionContent,
    SectionType.RICH_TEXT: RichTextSectionContent,
    SectionType.CTA: CTASectionContent,
    SectionType.FAQ: FAQSectionContent,
}


class WebsiteSectionService:
    @staticmethod
    def validate_content(section_type: SectionType, content: dict) -> dict:
        schema = SECTION_SCHEMA.get(section_type)

        if schema is None:
            raise ValueError(
                f"no schema registered for section type" f"{section_type.value}"
            )

        validated = schema.model_validate(content)
        return validated.model_dump()
