from fastapi import APIRouter, HTTPException, UploadFile, status

from src.apps.courses.api.schemas import CourseViewSchema
from src.apps.courses import service
from src.apps.courses.models import Course

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", status_code=status.HTTP_200_OK, response_model=list[CourseViewSchema])
async def list_courses() -> list[Course]:
    return await service.list_courses()


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_courses() -> None:
    await service.delete_courses()


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def upload_courses(file: UploadFile):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file should be an .xlsx file",
        )

    contents = await file.read()
    await service.upload_courses(contents)
