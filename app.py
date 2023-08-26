from parser.router_parser import router as router_parser

from fastapi import FastAPI

from api.router import router as router_api
from database import close_db_connection

app = FastAPI()

app.add_event_handler("shutdown", close_db_connection)
app.include_router(router_parser)
app.include_router(router_api)
