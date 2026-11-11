from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.facility import SportType


class FacilityBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    sport: SportType
    location: str = Field(min_length=2, max_length=200)
    capacity: int = Field(gt=0, le=500)
    description: str | None = Field(default=None, max_length=2000)
    is_active: bool = True


class FacilityCreate(FacilityBase):
    pass


class FacilityUpdate(BaseModel):
    """All fields optional: only the fields sent are changed."""

    name: str | None = Field(default=None, min_length=2, max_length=100)
    sport: SportType | None = None
    location: str | None = Field(default=None, min_length=2, max_length=200)
    capacity: int | None = Field(default=None, gt=0, le=500)
    description: str | None = Field(default=None, max_length=2000)
    is_active: bool | None = None


class FacilityRead(FacilityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
