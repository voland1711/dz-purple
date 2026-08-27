from fastapi import FastAPI
from posts import routes as post_routes
from rand import routes as rand_routes

app = FastAPI()

app.include_router(post_routes.router)
app.include_router(rand_routes.router)
