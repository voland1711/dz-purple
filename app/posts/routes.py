import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.core.settings import SettingsDeps

from .schema import (
    PostCreateRequest,
    PostCreateResponse,
    PostsPath,
    PostsPathResponse,
    PostUpdateRequest,
    PostUpdateResponse,
)
from .service import PostServiceDeps

logger = logging.getLogger(__name__)
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
def get_post(
    service: PostServiceDeps, settings: SettingsDeps, path: PostsPath = Depends()
):
    logger.info("Строка подключения БД для размещения постов: %s", settings.db.url)
    logger.info(
        "Минимальное количество минут для размещения следующего поста: : %s",
        settings.debounce.minimal_post_debounce_time,
    )

    logger.info("Запрос поста, под номером: %s", path.post_id)
    res = service.get_post(path.post_id)
    return PostsPathResponse(post_id=res)


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
    logger.info("answer_id = %s", data.answer_id, extra={"user_id": data.user_id})
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

    logger.info(
        "Обновлен пост, post_id = %s", path.post_id, extra={"user_id": data.user_id}
    )

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
    logger.info("Удален пост с post_id = %s", path.post_id)
    return PostsPathResponse(post_id=path.post_id)
