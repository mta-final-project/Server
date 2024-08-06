from pydantic import BaseModel

from src.models import EnrichedGroup


class SelectedGroupsSchema(BaseModel):
    groups: list[EnrichedGroup]


class UpdateScheduleSchema(BaseModel):
    groups: list[EnrichedGroup]
