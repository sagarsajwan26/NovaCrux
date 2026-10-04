from pydantic import BaseModel, Field, HttpUrl


class HeroSectionContent(BaseModel):
    heading: str = Field(min_length=1, max_length=200)
    subheading: str | None = Field(default=None, max_length=500)
    button_text: str | None = Field(default=None, max_length=100)
    button_url: str | None = Field(default=None, max_length=500)
    image_url: str | None = Field(default=None, max_length=1000)


class TextSectionContent(BaseModel):
    heading: str | None = Field(default=None, max_length=200)
    body: str = Field(min_length=1)


class RichTextSectionContent(BaseModel):
    heading: str | None = Field(default=None, max_length=200)
    body: str = Field(min_length=1)


class CTASectionContent(BaseModel):
    heading: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=500)
    button_text: str = Field(min_length=1, max_length=100)
    button_url: str = Field(min_length=1, max_length=500)


class FAQItem(BaseModel):
    question: str = Field(min_length=1, max_length=300)
    answer: str = Field(min_length=1)


class FAQSectionContent(BaseModel):
    heading: str | None = Field(default=None, max_length=200)
    items: list[FAQItem] = Field(min_length=1)
