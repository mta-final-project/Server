from pydantic import BaseModel

from src.apps.shcedule.models import EnrichedGroup


class SelectedGroupsSchema(BaseModel):
    groups: list[EnrichedGroup]


class UpdateScheduleSchema(BaseModel):
    groups: list[EnrichedGroup]
