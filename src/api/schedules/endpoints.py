from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from src.api.common.deps import UsersServiceDep
from src.api.schedules.schemas import SelectedGroupsSchema, UpdateScheduleSchema
from src.core.auth import cognito_auth
from src.models import Course, CoursesSchedule, EnrichedGroup
from src.services import schedule as service

router = APIRouter(
    prefix="/schedule", tags=["Schedule"], dependencies=[Depends(cognito_auth)]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_schedule(
    request: Request, user_service: UsersServiceDep
) -> CoursesSchedule:
    user = await user_service.get_user_by_request(request)
    return user.schedule


@router.get("/options/", status_code=status.HTTP_200_OK)
async def get_options(
    request: Request,
    user_service: UsersServiceDep,
    courses_ids: list[PydanticObjectId] | None = Query(default=None),
) -> list[SelectedGroupsSchema]:
    courses_ids = courses_ids or []
    courses = [await Course.get(_id) for _id in courses_ids]
    user = await user_service.get_user_by_request(request)
    schedule = user.schedule

    options = service.get_optional_combinations(courses, schedule)
    result = []
    for option in options:
        groups = [
            EnrichedGroup(**dict(group), course=course.metadata)
            for group, course in zip(option, courses)
        ]
        result.append(SelectedGroupsSchema(groups=groups))

    return result


@router.patch("/{_id}", status_code=status.HTTP_200_OK)
async def update_schedule(
    request: Request, user_service: UsersServiceDep, params: UpdateScheduleSchema
) -> None:
    user = await user_service.get_user_by_request(request)
    schedule = user.schedule
    schedule.add_groups(params.groups)

    if schedule.is_valid() is False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="One or more of the selected groups are overlapping "
            "with other lessons",
        )

    await user.save()


@router.delete("/{schedule_id}/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    request: Request,
    group_id: int,
    user_service: UsersServiceDep,
) -> None:
    user = await user_service.get_user_by_request(request)
    schedule = user.schedule
    schedule.delete_group(group_id)

    await user.save()
