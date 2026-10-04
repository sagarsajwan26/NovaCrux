from pydantic import BaseModel, Field


class WebsitePageCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=200)


class WebsitePageUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    slug: str | None = Field(default=None, min_length=1, max_length=200)


class WebsitePageResponse(BaseModel):
    id: int
    website_id: int
    title: str
    slug: str
    status: str
    meta_title: str | None
    meta_description: str | None

    model_config = {
        "from_attributes": True,
    }
