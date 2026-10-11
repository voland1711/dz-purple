import logging

from fastapi import APIRouter, Depends, HTTPException

from app.core.settings import SettingsDeps

from .schema import (
    PostCreateRequest,
    PostCreateResponse,
    PostGetResponse,
    PostPath,
    PostSearchParams,
    PostSearchResponse,
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
    response_model=PostGetResponse,
    summary="Возвращает пост по запрошенному id",
    description="""Сервис получает id требуемого поста. После валидации данных возвращает пост, в случае его наличия.
""",
)
async def get_post(
    service: PostServiceDeps, settings: SettingsDeps, path: PostPath = Depends()
):
    logger.info("Строка подключения БД для размещения постов: %s", settings.db.url)
    logger.info(
        "Минимальное количество минут для размещения следующего поста: : %s",
        settings.debounce.minimal_post_debounce_time,
    )

    logger.info("Запрос поста, под номером: %s", path.post_id)
    res = await service.get_post(path.post_id)
    return PostGetResponse(
        id=res.id,
        content=res.content,
        created_at=res.created_at,
        updated_at=res.updated_at,
        likes_count=res.likes_count,
    )


@router.post(
    "/",
    response_model=PostCreateResponse,
    status_code=201,
    summary="Создание поста",
    description="""Сервис получает данные для нового поста, в случае успешной валидации создается пост.
                   Пользователь получает в ответ данные созданного поста, размещенного для публикации.
""",
)
async def create_post(service: PostServiceDeps, data: PostCreateRequest):
    logger.info(data)
    res = await service.create(data)

    return PostCreateResponse(
        id=res.id,
        content=res.content,
        created_at=res.created_at,
        update_at=res.updated_at,
        likes_count=res.likes_count,
    )


@router.patch(
    "/{post_id}",
    response_model=PostUpdateResponse,
    summary="Обновление поста по id",
    description="""Сервис получает обновленные данные поста. В случае.
""",
)
async def update_post(
    service: PostServiceDeps, data: PostUpdateRequest, path: PostPath = Depends()
):

    logger.info("Обновлен пост, post_id = %s", path.post_id)
    res = await service.update(data, path.post_id)

    return PostUpdateResponse(
        id=res.id,
        content=res.content,
        created_at=res.created_at,
        update_at=res.updated_at,
        likes_count=res.likes_count,
    )


@router.delete(
    "/{post_id}",
    response_model=PostGetResponse,
    summary="Удаляет пост по id",
    description="""Сервис получает id поста, которое требуется удалить. После валидации данных удаляет пост, в случае его наличия.
""",
)
async def delete_post(service: PostServiceDeps, path: PostPath = Depends()):
    logger.info("Удален пост с post_id = %s", path.post_id)
    res = await service.delete(path.post_id)

    return PostGetResponse(
        id=res.id,
        content=res.content,
        created_at=res.created_at,
        updated_at=res.updated_at,
        likes_count=res.likes_count,
    )


@router.get(
    "/",
    response_model=PostSearchResponse,
    description="""
           Получает список постов, иначе возвращает ошибку""",
)
async def get_posts(service: PostServiceDeps, params: PostSearchParams = Depends()):
    posts, total = await service.get_posts(params)

    # logger.warning("warning task_id: %s", res, extra={"user_id": 1})
    return PostSearchResponse(
        items=[
            PostGetResponse(
                id=t.id,
                content=t.content,
                created_at=t.created_at,
                updated_at=t.updated_at,
                likes_count=t.likes_count,
            )
            for t in posts
        ],
        total=total,
        limit=params.limit,
        offset=params.offset,
    )


@router.patch(
    "/{post_id}/add_like",
    response_model=PostGetResponse,
    summary="Увеличивает like по id поста",
    description="""Сервис получает id поста, которому требуется поставить like. В случае отсутствия возвращает ошибку""",
)
async def like_post(service: PostServiceDeps, path: PostPath = Depends()):
    logger.info("Добавляем лайк для поста с id = %s", path.post_id)
    res = await service.like_post(path.post_id)

    return PostGetResponse(
        id=res.id,
        content=res.content,
        created_at=res.created_at,
        updated_at=res.updated_at,
        likes_count=res.likes_count,
    )
