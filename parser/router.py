import asyncio

from fastapi import APIRouter

from parser.parser_logic import parser, intermediate, run_coros

router = APIRouter(
    prefix="/parse",
    tags=["Parser"],
)


@router.post("")
async def do_parse(
        url: str = "https://jsonformatter.curiousconcept.com/",
        depth: int = 0,
        count_loaders: int = 1,
) -> dict:
    items = await run_coros(url=url, depth=depth, count_loaders=count_loaders)
    return {"message": f"Страницы успешно сохранены. Найдено страниц {len(items)}"}