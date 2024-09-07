import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from botocore.exceptions import ClientError

from src.api import router
from src.core.lifespan import lifespan
from src.core.settings import get_settings
from src.core.error_hanlers import handle_boto_error
from src.core.middlewares import add_process_time_header

app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO move to settings
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(ClientError, handle_boto_error)
app.middleware("http")(add_process_time_header)


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(app, host=settings.api.host, port=settings.api.port)
