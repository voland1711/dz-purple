from typing import Annotated

from fastapi import Depends

from .repository import PostRepository, PostRepositoryDeps


class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    def get_post(self, post_id: int):
        return self.repo.get_by_id(post_id)


def get_post_service(repo: PostRepositoryDeps):
    print("PostsService")
    return PostService(repo)


PostServiceDeps = Annotated[PostService, Depends(get_post_service)]
