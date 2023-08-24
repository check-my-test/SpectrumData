from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pymongo import ReplaceOne
from starlette import status
from starlette.responses import JSONResponse

from database import htmls
from parser.model import HTMLModel
from parser.parser_logic import run_coros

router = APIRouter(
    prefix="/parse",
    tags=["Parser"],
)


@router.post("")
async def do_parse(
        url: str = "https://jsonformatter.curiousconcept.com/",
        depth: int = 0,
        count_loaders: int = 1,
) -> JSONResponse:
    items = await run_coros(url=url, depth=depth, count_loaders=count_loaders)
    requests = []
    for url, item in items.items():
        # Добавление или обновление страницы. Я бы добавил опцию Update (bool), разрешающую обновлять или нет
        action = ReplaceOne({'url': url}, item, upsert=True)
        requests.append(action)
    await htmls.bulk_write(requests)
    message = {"message": f"Сохранено/обновлено {len(items)} страниц"}
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=message)
