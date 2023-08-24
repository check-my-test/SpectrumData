from fastapi import APIRouter

from database import htmls
from parser.model import HTMLModel

router = APIRouter(
    prefix="/find",
    tags=["Get html"],
)


@router.post("")
async def find_htmls(url: str = None, title: str = None, merge: bool = True) -> list:


    return []


@router.get("/find_one", response_model=HTMLModel)
async def find_one(url: str) -> dict:
    result = await htmls.find_one({"url": url})
    return result


# @app.get(
#     "/{id}", response_description="Get a single student", response_model=StudentModel
# )
# async def show_student(id: str):
#     if (student := await db["students"].find_one({"_id": id})) is not None:
#         return student
#
#     raise HTTPException(status_code=404, detail=f"Student {id} not found")