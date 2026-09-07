from typing import Annotated

from fastapi import Depends


class PostRepository:
    def get_by_id(self, post_id: int):
        return post_id - 11


def get_post_repository():
    print("PostRepository")
    return PostRepository()


PostRepositoryDeps = Annotated[PostRepository, Depends(get_post_repository)]
