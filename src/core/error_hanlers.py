from botocore.exceptions import ClientError
from fastapi import Request, status
from fastapi.responses import JSONResponse


async def handle_boto_error(_: Request, err: ClientError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": err.response["Error"]},
    )
