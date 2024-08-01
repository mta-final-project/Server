from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Query, status

from src.apps.courses.models import Course
from src.apps.schedule import service
from src.apps.schedule.api.schemas import SelectedGroupsSchema, UpdateScheduleSchema
from src.apps.schedule.models import CoursesSchedule, EnrichedGroup

router = APIRouter(prefix="/schedule", tags=["Schedule"])


async def _get_schedule(_id: PydanticObjectId) -> CoursesSchedule:
    schedule = await CoursesSchedule.get(_id)
    if schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Schedule does not exist"
        )

    return schedule


@router.get("/", status_code=status.HTTP_200_OK)
async def get_schedule(_id: PydanticObjectId) -> CoursesSchedule:
    return await _get_schedule(_id)


@router.get("/options/", status_code=status.HTTP_200_OK)
async def get_options(
    _id: PydanticObjectId | None = Query(default=None),
    courses_ids: list[PydanticObjectId] | None = Query(default=None),
) -> list[SelectedGroupsSchema]:
    courses_ids = courses_ids or []
    courses = [await Course.get(_id) for _id in courses_ids]
    schedule = await _get_schedule(_id)

    options = service.get_optional_combinations(courses, schedule)
    result = []
    for option in options:
        groups = [
            EnrichedGroup(**dict(group), course=course.metadata)
            for group, course in zip(option, courses)
        ]
        result.append(SelectedGroupsSchema(groups=groups))

    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_schedule() -> PydanticObjectId:
    schedule = CoursesSchedule()
    await schedule.save()

    return schedule.id


@router.patch("/{_id}", status_code=status.HTTP_200_OK)
async def update_schedule(_id: PydanticObjectId, params: UpdateScheduleSchema) -> None:
    schedule = await _get_schedule(_id)
    schedule.add_groups(params.groups)

    if schedule.is_valid() is False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="One or more of the selected groups are overlapping "
            "with other lessons",
        )

    await schedule.save()


@router.delete("/{schedule_id}/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(schedule_id: PydanticObjectId, group_id: int) -> None:
    schedule = await _get_schedule(schedule_id)
    schedule.delete_group(group_id)

    await schedule.save()
