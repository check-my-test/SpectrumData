from fastapi import FastAPI
from parser.router import router as router_parser


app = FastAPI()
app.include_router(router_parser)

