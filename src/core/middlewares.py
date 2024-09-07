import time
import logging
from fastapi import Request

logger = logging.getLogger("uvicorn")


async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    time_in_ms = (time.time() - start_time) * 1_000
    logger.info(f"Took {int(time_in_ms)} ms to response")
    return response
