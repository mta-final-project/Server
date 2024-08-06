from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import RedirectResponse

from src.apps.files import service
from src.apps.files.models import FileInfo, FileMetadata
from src.core.auth import cognito_auth

router = APIRouter(
    prefix="/files",
    tags=["Files"],
    dependencies=[Depends(cognito_auth)]
)

service = service.S3Service()


@router.get("/download", status_code=status.HTTP_200_OK)
async def download(
    file_name: str,
) -> RedirectResponse:
    if not file_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No file name provided"
        )
    presigned_url = await service.s3_get_presigned_url(file_name)
    return RedirectResponse(url=presigned_url)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload(file: UploadFile) -> None:
    await service.s3_upload(file)


@router.get("/metadata", status_code=status.HTTP_200_OK)
async def metadata(file_name: str) -> FileMetadata:
    if not file_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No file name provided"
        )
    return await service.s3_get_metadata(file_name)


@router.get("/list-folders", status_code=status.HTTP_200_OK)
async def list_folders(path: str = "") -> list[str]:
    return await service.s3_list_folders(path)


@router.get("/list-objects", status_code=status.HTTP_200_OK)
async def list_objects(path: str = "") -> list[FileInfo]:
    return await service.s3_list_objects(path)
