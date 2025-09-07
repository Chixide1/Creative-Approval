from fastapi import FastAPI
from src.routers.main_router import router

app = FastAPI()

app.include_router(router)