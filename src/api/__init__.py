from fastapi import APIRouter

from src.api.courses.endpoints import router as courses_router
from src.api.schedule.endpoints import router as schedule_router

router = APIRouter()
router.include_router(courses_router)
router.include_router(schedule_router)
