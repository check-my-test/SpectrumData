import logging

from fastapi import FastAPI

from database import close_db_connection

app = FastAPI()
app.add_event_handler("shutdown", close_db_connection)


@app.on_event("startup")
async def startup_event():
    # Костыль из-за появленяи циклического импорта в тестах
    from parser.router_parser import router as router_parser

    from api.router import router as router_api

    app.include_router(router_parser)
    app.include_router(router_api)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("my_logger")
