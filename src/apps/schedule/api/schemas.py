from pydantic import BaseModel

from src.apps.schedule.models import EnrichedGroup


class SelectedGroupsSchema(BaseModel):
    groups: list[EnrichedGroup]


class UpdateScheduleSchema(BaseModel):
    groups: list[EnrichedGroup]
