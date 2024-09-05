from pydantic import Field

from src.core.base_document import BaseDocument
from src.models.schedule import CoursesSchedule


class User(BaseDocument):
    cognito_id: str
    email: str
    favorite_courses: list[str] = Field(default_factory=list)
    schedule: CoursesSchedule = Field(default_factory=CoursesSchedule)
