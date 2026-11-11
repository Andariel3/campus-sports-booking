"""Resource schemas, matching the Swagger contract on Confluence (API REST (Swagger)).

JSON fields are camelCase (pricePerHour, openHour, closeHour); Python attributes stay snake_case.
"""

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

from app.models.resource import ResourceType

HOUR_PATTERN = r"^([01]\d|2[0-3]):[0-5]\d$"


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ResourceCreate(CamelModel):
    name: str = Field(min_length=2, max_length=100, examples=["Teren tenis 1"])
    type: ResourceType
    sport: str = Field(min_length=2, max_length=50, examples=["tenis"])
    description: str | None = Field(default=None, max_length=2000)
    price_per_hour: float | None = Field(default=None, ge=0, examples=[40])
    open_hour: str | None = Field(default=None, pattern=HOUR_PATTERN, examples=["08:00"])
    close_hour: str | None = Field(default=None, pattern=HOUR_PATTERN, examples=["22:00"])

    @model_validator(mode="after")
    def check_hours(self) -> Self:
        check_open_before_close(self.open_hour, self.close_hour)
        return self


class ResourceUpdate(CamelModel):
    """Same fields as ResourceCreate, all optional: only the fields sent are changed."""

    name: str | None = Field(default=None, min_length=2, max_length=100)
    type: ResourceType | None = None
    sport: str | None = Field(default=None, min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=2000)
    price_per_hour: float | None = Field(default=None, ge=0)
    open_hour: str | None = Field(default=None, pattern=HOUR_PATTERN)
    close_hour: str | None = Field(default=None, pattern=HOUR_PATTERN)

    @model_validator(mode="after")
    def check_hours(self) -> Self:
        check_open_before_close(self.open_hour, self.close_hour)
        return self


class ResourceRead(ResourceCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


def check_open_before_close(open_hour: str | None, close_hour: str | None) -> None:
    # "HH:MM" strings compare correctly as text
    if open_hour and close_hour and open_hour >= close_hour:
        raise ValueError("openHour must be before closeHour")
