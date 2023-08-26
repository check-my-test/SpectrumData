from parser.model import HTMLModel

from fastapi import APIRouter, HTTPException

from api.service import create_query
from mongo.database import htmls

router = APIRouter(
    prefix="/find",
    tags=["Get html"],
)


@router.post("", response_model=list[HTMLModel])
async def find_htmls(url: str = "", title: str = "", combine: bool = True) -> list[HTMLModel]:
    """
    :param url: Часть или полный url для поиска по url
    :param title: Часть или полный title для поиска по title
    :param combine: Если True - поиск по пересечению двух условий, если False - в результат будут добавлены страницы,
    подходящие и по url и по title
    :return:
    """
    if not url and not title:
        return await htmls.find().to_list(length=100)
    query = await create_query(url=url, title=title, combine=combine)

    return await htmls.find(query).to_list(length=100)


@router.get("/get_html", response_model=HTMLModel)
async def get_html(url: str) -> dict:
    result = await htmls.find_one({"url": url})
    if result is None:
        raise HTTPException(status_code=404, detail="Страница не найдена")
    return result
