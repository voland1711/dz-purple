from fastapi import APIRouter, HTTPException, Path, Response
from fastapi.requests import Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/posts")


class UnAuthHttpException(HTTPException):
    def __init__(self):
        super().__init__(401, "Не авторизован")


@router.get("/{post_id}")
def get_greet(post_id: int = Path(ge=1)):

    return {"Пост": post_id}


@router.post("/", response_class=JSONResponse)
async def create_post(request: Request, response: Response):
    data = await request.json()
    response.status_code = 201
    return data


@router.patch("/{post_id}")
async def update_post(request: Request, post_id: int = Path(ge=1)):
    data = await request.json()
    return {"Пост обновлен": post_id, "Пост": data}


@router.delete("/{post_id}")
async def delete_post(post_id: int = Path(ge=1)):

    return {"Удален пост": post_id}
