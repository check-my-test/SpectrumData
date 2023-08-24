import re

from fastapi import APIRouter, HTTPException

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
    temp = {"url": url, "title": title}
    subquery = {}
    for field, data in temp.items():
        if data is not None:
            subquery[field] = {"$regex": re.compile(data, re.IGNORECASE)}
    if len(subquery) == 1:
        return await htmls.find(subquery).to_list(length=100)
    else:
        option = "$and" if combine else "$or"
        total_query = {
            option: [
                {"url": subquery["url"]},
                {"title": subquery["title"]},
            ]
        }
        return await htmls.find(total_query).to_list(length=100)


@router.get("/get_html", response_model=HTMLModel)
async def get_html(url: str) -> dict:
    result = await htmls.find_one({"url": url})
    if result is None:
        raise HTTPException(status_code=404, detail=f"Страница не найдена")
    return result
