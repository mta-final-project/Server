from fastapi import APIRouter

from src.api.courses.endpoints import router as courses_router
from src.api.files.endpoints import router as files_router
from src.api.schedules.endpoints import router as schedule_router
from src.api.users.endpoints import router as users_router

router = APIRouter()
router.include_router(users_router)
router.include_router(files_router)
router.include_router(courses_router)
router.include_router(schedule_router)
