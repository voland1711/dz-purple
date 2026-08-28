from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator


class PostsPath(BaseModel):
    post_id: int = Field(gt=0)


class PostCreateRequest(BaseModel):
    user_id: int = Field(ge=1)
    content: str
    answer_id: int | None = None

    model_config = {"extra": "forbid"}

    @field_validator("content")
    @classmethod
    def key_not_empty(cls, value):
        clean_value = value.rstrip()
        if not clean_value:
            raise HTTPException(400, "content must be valid string")
        return clean_value


class PostCreateResponse(BaseModel):
    user_id: int
    content: str
    post_id: int
    answer_id: int | None = None


class PostUpdateRequest(BaseModel):
    user_id: int = Field(ge=1)
    content: str

    @field_validator("content")
    @classmethod
    def key_not_empty(cls, value):
        clean_value = value.rstrip()
        if not clean_value:
            raise HTTPException(400, "content must be valid string")
        return clean_value


class PostUpdateResponse(BaseModel):
    user_id: int
    content: str
    post_id: int
