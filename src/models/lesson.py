from datetime import date, datetime, time, timedelta
from typing import Self

import pandas as pd
from pydantic import BaseModel, Field

from src.models.column_map import Column


class TimeSlot(BaseModel):
    day: int = Field(..., ge=1, le=7)
    start_time: time
    end_time: time

    @property
    def duration(self) -> timedelta:
        return datetime.combine(date.min, self.end_time) - datetime.combine(
            date.min, self.start_time
        )


class Lesson(TimeSlot):
    classroom: str

    @classmethod
    def from_row(cls, row: pd.Series) -> Self:
        return cls(
            group=row[Column.Group],
            day=row[Column.Day],
            lecturer=row[Column.Lecturer],
            start_time=row[Column.StartTime],
            end_time=row[Column.EndTime],
            classroom=row[Column.Classroom],
        )

    @property
    def time_slot(self) -> TimeSlot:
        return TimeSlot(**dict(self))
