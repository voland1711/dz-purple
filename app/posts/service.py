import logging
from typing import Annotated

from fastapi import Depends, HTTPException

from app.posts.model import Post
from app.posts.schema import PostCreateRequest, PostSearchParams, PostUpdateRequest

from .repository import PostRepository, PostRepositoryDeps

logger = logging.getLogger(__name__)


class PostService:
    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    async def get_post(self, post_id: int) -> Post:
        post = await self.post_repo.get_by_id(post_id)
        if post is None or post.is_deleted:
            raise HTTPException(404, "Not found")
        return post

    async def create(self, data: PostCreateRequest):
        # project = await self.post_repo.get_by_id(data.id)
        # if project is None:
        #     raise HTTPException(404, "Project not found")
        post = Post(**data.model_dump())
        return await self.post_repo.save(post)

    async def update(self, data: PostUpdateRequest, post_id: int):
        post = await self.post_repo.get_by_id(post_id)
        if post is None or post.is_deleted:
            raise HTTPException(404, "Not found")

        logger.info(
            "post, который требуется обновить: post_id = %s, post_content = %s",
            post.id,
            post.content,
        )
        if data.content is not None:
            post.content = data.content
            post.id = post_id
            logger.info("писец %s", post.id)
        return await self.post_repo.update(post)

    async def delete(self, post_id: int) -> Post:
        post = await self.post_repo.get_by_id(post_id)
        if post is None or post.is_deleted:
            raise HTTPException(404, "Not found or deleted")

        logger.info("Удаление результат2: res= %s", post.id)

        post.is_deleted = True
        post.id = post_id
        res = await self.post_repo.delete(post)

        logger.info("Удаление результат2: res= %s", res.is_deleted)
        return res

    async def get_posts(self, params: PostSearchParams) -> tuple[list[Post], int]:
        return await self.post_repo.get_posts(offset=params.offset, limit=params.limit)

    async def like_post(self, post_id: int) -> Post:
        post = await self.post_repo.get_by_id(post_id)
        if post is None or post.is_deleted:
            raise HTTPException(404, "Not found")

        return await self.post_repo.like_post(post_id)


def get_post_service(post_repo: PostRepositoryDeps):
    logger.info("Работает: PostsService")
    return PostService(post_repo)


PostServiceDeps = Annotated[PostService, Depends(get_post_service)]
