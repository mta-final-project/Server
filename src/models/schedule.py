from pydantic import Field

from src.core.base_document import BaseDocument
from src.models.course import CourseMetadata
from src.models.group import Group, GroupMetadata
from src.models.lesson import Lesson


class EnrichedGroup(Group):
    course: CourseMetadata


class ScheduleItem(Lesson):
    course: CourseMetadata
    group: GroupMetadata


class CoursesSchedule(BaseDocument):
    schedule: dict[int, list[ScheduleItem]] = Field(default_factory=dict)

    def get_day(self, day: int) -> list[ScheduleItem]:
        if day not in self.schedule:
            self.schedule[day] = []

        return self.schedule[day]

    def is_valid(self) -> bool:
        for day, schedule in self.schedule.items():
            for item1, item2 in zip(schedule, schedule[1:]):
                if item1.day != day or item2.day != day:
                    return False
                if item2.start_time < item1.end_time:
                    return False

        return True

    def sort_items(self):
        for _, schedule_day in self.schedule.items():
            schedule_day.sort(key=lambda item: item.start_time)

    def add_groups(self, groups: list[EnrichedGroup]):
        for group in groups:
            for lesson in group.lessons:
                schedule_day = self.get_day(lesson.day)
                schedule_day.append(
                    ScheduleItem(
                        course=group.course, group=group.metadata, **dict(lesson)
                    )
                )
        self.sort_items()

    def remove_group(self, group_id: int) -> None:
        for day, schedule_day in self.schedule.items():
            self.schedule[day] = [
                item for item in schedule_day if item.group_id != group_id
            ]
