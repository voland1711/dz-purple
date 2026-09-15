from fastapi import FastAPI

from .core.settings import Settings
from .posts import routes as post_routes
from .rand import routes as rand_routes


def create_app() -> FastAPI:
    settings = Settings()
    new_app = FastAPI(
        title=settings.app.name,
        description=settings.app.description,
        version="0.1.6",
        openapi_tags=[
            {"name": "Posts", "description": "Сервис для управления постами"},
            {
                "name": "Random",
                "description": "Сервис получения случайного целого числа",
            },
        ],
    )
    new_app.state.settings = settings
    new_app.include_router(post_routes.router)
    new_app.include_router(rand_routes.router)

    return new_app


app = create_app()
