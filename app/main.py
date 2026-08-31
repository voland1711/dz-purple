from fastapi import FastAPI
from posts import routes as post_routes
from rand import routes as rand_routes

app = FastAPI(
    title="My Posts API",
    description="API аналог приложения Twitter",
    version="0.0.1",
    openapi_tags=[
        {"name": "Posts-service", "description": "Сервис для управления постами"}
    ],
)

app.include_router(post_routes.router)
app.include_router(rand_routes.router)
