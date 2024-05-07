from typing import Self

import pandas as pd
from pydantic import BaseModel, Field

from src.apps.courses.models.column_map import Column
from src.apps.courses.models.lesson import Lesson

GROUP_TYPE = {
    1: "שיעור עם מבחן",
    2: "שיעור בלי מבחן",
    3: "סדנה",
    6: "שיעור מתוגברת",
    7: "תרגול",
    15: "תרגול מתוגברת",
}


class GroupType(BaseModel):
    number: int
    description: str | None


class GroupMetadata(BaseModel):
    group_id: int
    description: str
    lecturer: str
    type: GroupType


class Group(GroupMetadata):
    lessons: list[Lesson] = Field(default_factory=list)

    @property
    def metadata(self) -> GroupMetadata:
        return GroupMetadata(**dict(self))

    @classmethod
    def from_row(cls, row: pd.Series) -> Self:
        group_type_number = row[Column.LessonType]
        group_type = GroupType(
            number=group_type_number, description=GROUP_TYPE.get(group_type_number)
        )
        return cls(
            group_id=row[Column.Group],
            description=row[Column.GroupDescription],
            lecturer=row[Column.Lecturer],
            type=group_type,
        )
