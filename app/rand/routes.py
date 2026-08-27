# Query get rnd_from и rnd_to, возвращающий случайное чилос типа int в пределах диапазона (границы включены)
from random import randint

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/rand")


class validException(HTTPException):
    def __init__(self):
        super().__init__(400, "rnd_from > rnd_to")


@router.get("/")
def get_rnd(rnd_from: int = 0, rnd_to: int = 100):
    if rnd_from > rnd_to:
        raise validException()
    return randint(rnd_from, rnd_to)
