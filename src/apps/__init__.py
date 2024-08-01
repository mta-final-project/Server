from fastapi import APIRouter

from src.apps.courses.api.endpoints import router as courses_router
from src.apps.files.api.endpoints import router as files_router
from src.apps.schedule.api.endpoints import router as schedule_router
from src.apps.users.api.endpoints import router as users_router

router = APIRouter()
router.include_router(users_router)
router.include_router(files_router)
router.include_router(courses_router)
router.include_router(schedule_router)
