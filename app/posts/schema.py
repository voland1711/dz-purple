from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class PostPath(BaseModel):
    post_id: int = Field(gt=0)


class PostGetResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    likes_count: int


class PostCreateRequest(BaseModel):
    content: str
    model_config = {"extra": "forbid"}

    @field_validator("content")
    @classmethod
    def key_not_empty(cls, value):
        clean_value = value.rstrip()
        if not clean_value:
            raise ValueError("content must be valid string")
        return clean_value


class PostCreateResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    likes_count: int


class PostUpdateRequest(BaseModel):
    content: str | None = None

    model_config = {"extra": "forbid"}

    @field_validator("content")
    @classmethod
    def key_not_empty(cls, value):
        if value is None:
            return value
        clean_value = value.rstrip()
        if not clean_value:
            raise ValueError("content must be valid string")
        return clean_value


class PostUpdateResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    likes_count: int


class PostSearchParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)


class PostSearchResponse(BaseModel):
    items: list[PostGetResponse]
    total: int
    limit: int
    offset: int
