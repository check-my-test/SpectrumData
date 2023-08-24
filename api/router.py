from fastapi import APIRouter, HTTPException

from api.service import create_query
from database import htmls
from parser.model import HTMLModel

router = APIRouter(
    prefix="/find",
    tags=["Get html"],
)


@router.post("", response_model=list[HTMLModel])
async def find_htmls(url: str = None, title: str = None, combine: bool = True) -> list[HTMLModel]:
    if not url and not title:
        return await htmls.find().to_list(length=100)
    query = await create_query(url=url, title=title, combine=combine)

    return await htmls.find(query).to_list(length=100)


@router.get("/get_html", response_model=HTMLModel)
async def get_html(url: str) -> dict:
    result = await htmls.find_one({"url": url})
    if result is None:
        raise HTTPException(status_code=404, detail=f"Страница не найдена")
    return result
