from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse

from .schema import (
    PostCreateRequest,
    PostCreateResponse,
    PostsPath,
    PostUpdateRequest,
    PostUpdateResponse,
)

router = APIRouter(prefix="/posts")


class UnAuthHttpException(HTTPException):
    def __init__(self):
        super().__init__(401, "Не авторизован")


@router.get("/{post_id}")
def get_greet(path: PostsPath = Depends()):

    return {"Пост": path.post_id}


@router.post("/", response_class=JSONResponse)
async def create_post(data: PostCreateRequest, response: Response):

    response.status_code = 201
    return PostCreateResponse(
        user_id=data.user_id,
        content=data.content,
        post_id=123,
        answer_id=data.answer_id,
    )


@router.patch("/{post_id}")
async def update_post(data: PostUpdateRequest, path: PostsPath = Depends()):
    return PostUpdateResponse(
        user_id=data.user_id, content=data.content, post_id=path.post_id
    )


@router.delete("/{post_id}")
async def delete_post(path: PostsPath = Depends()):

    return {"Удален пост": path.post_id}
