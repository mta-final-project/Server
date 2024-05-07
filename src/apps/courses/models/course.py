from typing import Self

import pandas as pd
from pydantic import BaseModel, Field

from src.apps.courses.models.column_map import Column
from src.apps.courses.models.group import Group
from src.core.base_document import BaseDocument


class CourseMetadata(BaseModel):
    semester: int = Field(..., ge=1, le=3)
    department: str
    subject: str
    credit_points: int


class Course(BaseDocument, CourseMetadata):
    lectures: list[Group] = Field(default_factory=list)
    exercises: list[Group] = Field(default_factory=list)

    @property
    def metadata(self) -> CourseMetadata:
        return CourseMetadata(**dict(self))

    @classmethod
    def from_row(cls, row: pd.Series) -> Self:
        return cls(
            semester=row[Column.Semester],
            department=row[Column.Department],
            subject=row[Column.Subject],
            credit_points=row[Column.Credits],
        )

    @property
    def number_of_lectures(self) -> int:
        return len(self.lectures)

    @property
    def number_of_exercises(self) -> int:
        return len(self.exercises)
