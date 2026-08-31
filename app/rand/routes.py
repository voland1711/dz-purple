# Query get rnd_from и rnd_to, возвращающий случайное чилос типа int в пределах диапазона (границы включены)
from random import randint

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from .schema import RandomRequest, RandomResponse

router = APIRouter(prefix="/rand", tags=["Random"])


@router.get(
    "/",
    response_class=JSONResponse,
    summary="Возвращает случайное целое число",
    description="""
Получает два целых числа(по умолчанию [0; 100]) и возвращает
случайное число из полученного диапазона
""",
)
def get_rnd(randomRequest: RandomRequest = Depends()):
    res = randint(randomRequest.rnd_from, randomRequest.rnd_to)
    return RandomResponse(rnd=res)
