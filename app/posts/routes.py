from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from .schema import (
    PostCreateRequest,
    PostCreateResponse,
    PostsPath,
    PostsPathResponse,
    PostUpdateRequest,
    PostUpdateResponse,
)

router = APIRouter(prefix="/posts", tags=["Posts"])


class UnAuthHttpException(HTTPException):
    def __init__(self):
        super().__init__(401, "Не авторизован")


@router.get(
    "/{post_id}",
    response_model=PostsPathResponse,
    summary="Возвращает пост по запрошенному id",
    description="""Сервис получает id требуемого поста. После валидации данных возвращает пост, в случае его наличия.
""",
)
def get_post(path: PostsPath = Depends()):
    return PostsPathResponse(path.post_id)


@router.post(
    "/",
    response_class=JSONResponse,
    response_model=PostCreateResponse,
    status_code=201,
    summary="Создание поста",
    description="""Сервис получает данные для нового поста, в случае успешной валидации создается пост.
                   Пользователь получает в ответ данные созданного поста, размещенного для публикации.
""",
)
async def create_post(data: PostCreateRequest):

    return PostCreateResponse(
        user_id=data.user_id,
        content=data.content,
        post_id=123,
        answer_id=data.answer_id,
    )


@router.patch(
    "/{post_id}",
    response_model=PostUpdateResponse,
    summary="Обновлени поста по id",
    description="""Сервис получает обновленные данные поста. В случае.
""",
)
async def update_post(data: PostUpdateRequest, path: PostsPath = Depends()):

    if data.content:
        tmp_content = data.content
    else:
        tmp_content = "Старое сообщение"
    return PostUpdateResponse(
        user_id=data.user_id, content=tmp_content, post_id=path.post_id
    )


@router.delete(
    "/{post_id}",
    response_model=PostsPathResponse,
    summary="Удаляет пост по id",
    description="""Сервис получает id поста, которое требуется удалить. После валидации данных удаляет пост, в случае его наличия.
""",
)
async def delete_post(path: PostsPath = Depends()):

    return PostsPathResponse(path.post_id)
