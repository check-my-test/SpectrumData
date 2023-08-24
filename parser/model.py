from bson import ObjectId
from pydantic import BaseModel, Field

from database import PyObjectId


class HTMLModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    url: str = Field(...)
    title: str = Field(...)
    html: str = Field(...)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "url": "https://jsonformatter.curiousconcept.com/",
                "title": "JSON Formatter & Validator",
                "html": "The HTML page...",
            }
        }
