from botocore.exceptions import ClientError
from fastapi import Request, status
from fastapi.responses import JSONResponse


async def handle_boto_error(_: Request, err: ClientError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={"detail": err.response["Error"]},
    )
