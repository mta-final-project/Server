from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.mongo import init
from src.core.settings import get_settings


async def on_start(_app: FastAPI):
    settings = get_settings()
    await init(settings.mongo.url, settings.mongo.database)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_start(app)
    yield
