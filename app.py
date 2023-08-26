from fastapi import FastAPI

from database import close_db_connection
from parser.router import router as router_parser
from api.router import router as router_api


app = FastAPI()
app.include_router(router_parser)
app.include_router(router_api)
app.add_event_handler("shutdown", close_db_connection)
