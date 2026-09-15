import logging
from typing import Annotated

from fastapi import Depends

logger = logging.getLogger(__name__)


class PostRepository:
    def get_by_id(self, post_id: int):
        return post_id - 11


def get_post_repository():
    logger.info("Работает: PostRepository")
    return PostRepository()


PostRepositoryDeps = Annotated[PostRepository, Depends(get_post_repository)]
