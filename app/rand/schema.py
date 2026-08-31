from fastapi import HTTPException
from pydantic import BaseModel


class validException(HTTPException):
    def __init__(self):
        super().__init__(400, "rnd_from > rnd_to")


class RandomRequest(BaseModel):
    rnd_from: int = 0
    rnd_to: int = 100

    if rnd_from > rnd_to:
        raise validException()


class RandomResponse(BaseModel):
    rnd: int
