from pydantic import BaseModel


class HTMLModel(BaseModel):
    url: str
    title: str
    html: str

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://jsonformatter.curiousconcept.com/",
                "title": "JSON Formatter & Validator",
                "html": "The HTML page...",
            }
        }
