from src.apps.courses.models import Course, Group
from src.apps.schedule.models import CoursesSchedule
from src.apps.schedule.schedule import Schedule

type SelectedGroups = list[Group]
type Option = tuple[SelectedGroups, Schedule]


def get_optional_combinations(
    courses: list[Course], base_schedule: CoursesSchedule | None = None
) -> list[SelectedGroups]:
    options = [
        ([], _build_schedule(base_schedule))
    ]  # add a single option with no groups and unmodified / empty schedule

    for course in courses:
        options = _update_options(options, course.lectures)
        options = _update_options(options, course.exercises)

    return [selected_groups for selected_groups, _ in options]


def _build_schedule(base_schedule: CoursesSchedule | None = None):
    schedule = Schedule()

    if base_schedule:
        for _, items in base_schedule.schedule.items():
            for item in items:
                schedule.add_item(item.time_slot)

    return schedule


def _update_options(options: list[Option], groups: list[Group]) -> list[Option]:
    if not groups:
        return options

    new_schedules, new_groups = [], []
    for option, schedule in options:
        new_schedule = schedule.copy(deep=True)
        for group in groups:
            try:
                _add_group_to_schedule(new_schedule, group)
                new_schedules.append(new_schedule)
                new_groups.append(option + [group])
            except ValueError:
                continue

    return list(zip(new_groups, new_schedules))


def _add_group_to_schedule(schedule: Schedule, group: Group) -> None:
    for lesson in group.lessons:
        schedule.add_item(lesson.time_slot)
