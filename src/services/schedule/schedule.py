from collections import defaultdict

from pydantic import BaseModel, Field

from src.models.lesson import TimeSlot


class Schedule(BaseModel):
    lessons: dict[int, list[TimeSlot]] = Field(
        default_factory=lambda: defaultdict(list)
    )

    def is_available(self, time_slot: TimeSlot) -> bool:
        for lesson in self.lessons[time_slot.day]:
            if lesson.start_time <= time_slot.start_time < lesson.end_time:
                return False
            if lesson.start_time < time_slot.end_time <= lesson.end_time:
                return False

        return True

    def add_item(self, time_slot: TimeSlot) -> None:
        if not self.is_available(time_slot):
            raise ValueError("Time slot is not available")

        self.lessons[time_slot.day].append(time_slot)
