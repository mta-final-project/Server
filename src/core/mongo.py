from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.apps.courses.models import Course
from src.apps.schedule.models import CoursesSchedule


async def init(mongo_url: str, mongo_database: str):
    # Create Motor client
    client = AsyncIOMotorClient(mongo_url)

    # Initialize beanie with the Sample document class and a database
    await init_beanie(
        database=client[mongo_database], document_models=[Course, CoursesSchedule]
    )
