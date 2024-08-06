from fastapi import APIRouter, HTTPException, UploadFile, status, Depends

from src.core.auth import cognito_auth
from src.services import courses as service
from src.api.courses.schemas import CourseViewSchema
from src.models.course import Course

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[CourseViewSchema],
    dependencies=[Depends(cognito_auth)]
)
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
