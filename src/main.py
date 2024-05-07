import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import router
from src.core.lifespan import lifespan
from src.core.settings import get_settings

app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO move to settings
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(app, host=settings.api.host, port=settings.api.port)
