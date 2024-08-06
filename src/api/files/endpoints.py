from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import RedirectResponse

from src.api.files.deps import s3_service
from src.api.files.schemas import FileInfo, FileMetadata
from src.core.auth import cognito_auth
from src.services.files import S3Service

router = APIRouter(
    prefix="/files", tags=["Files"], dependencies=[Depends(cognito_auth)]
)

S3ServiceDep = Annotated[S3Service, Depends(s3_service)]


@router.get("/download", status_code=status.HTTP_200_OK)
async def download(file_name: str, service: S3ServiceDep) -> RedirectResponse:
    if not file_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No file name provided"
        )
    presigned_url = await service.s3_get_presigned_url(file_name)
    return RedirectResponse(url=presigned_url)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload(file: UploadFile, service: S3ServiceDep) -> None:
    await service.s3_upload(file)


@router.get("/metadata", status_code=status.HTTP_200_OK)
async def metadata(file_name: str, service: S3ServiceDep) -> FileMetadata:
    if not file_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No file name provided"
        )
    return await service.s3_get_metadata(file_name)


@router.get("/list-folders", status_code=status.HTTP_200_OK)
async def list_folders(service: S3ServiceDep, path: str = "") -> list[str]:
    return await service.s3_list_folders(path)


@router.get("/list-objects", status_code=status.HTTP_200_OK)
async def list_objects(service: S3ServiceDep, path: str = "") -> list[FileInfo]:
    return await service.s3_list_objects(path)
