import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.sql.functions import count

from app.core.db import DbSessionDeps
from app.posts.model import Post

logger = logging.getLogger(__name__)


class PostRepository:
    def __init__(self, session: DbSessionDeps):
        self.session = session

    async def get_by_id(self, post_id: int):
        return await self.session.get(Post, post_id)

    async def save(self, post: Post) -> Post:
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def update(self, post: Post) -> Post:
        managed_post = await self.session.merge(post)
        await self.session.commit()
        await self.session.refresh(managed_post)
        return managed_post

    async def delete(self, post: Post) -> Post:
        managed_post = await self.session.merge(post)
        await self.session.commit()
        await self.session.refresh(managed_post)
        return managed_post

    async def get_posts(self, offset: int = 0, limit: int = 20):

        # Создаем базовый фильтр, чтобы не дублировать код
        base_filter = Post.is_deleted == False

        count_query = select(count()).select_from(Post)
        query = select(Post).where(base_filter)

        count_query = count_query.where(base_filter)

        total_result = await self.session.execute(count_query)

        total = total_result.scalar_one()

        query = query.order_by(Post.created_at).offset(offset).limit(limit)

        result = await self.session.execute(query)

        posts = list(result.scalars().all())

        return posts, total

    async def like_post(self, post: Post) -> Post:
        managed_post = await self.session.merge(post)
        await self.session.commit()
        await self.session.refresh(managed_post)
        return managed_post


def get_post_repository(session: DbSessionDeps):
    logger.info("Работает: PostRepository")
    return PostRepository(session)


PostRepositoryDeps = Annotated[PostRepository, Depends(get_post_repository)]
