from enum import StrEnum

from sqlalchemy import Enum, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ResourceType(StrEnum):
    TEREN = "teren"
    BAZIN = "bazin"


class Resource(Base):
    """A bookable sports resource: a field/court ("teren") or the pool ("bazin")."""

    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    type: Mapped[ResourceType] = mapped_column(
        Enum(ResourceType, name="resource_type", values_callable=lambda e: [m.value for m in e])
    )
    sport: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text, default=None)
    price_per_hour: Mapped[float | None] = mapped_column(Float, default=None)
    open_hour: Mapped[str | None] = mapped_column(String(5), default=None)
    close_hour: Mapped[str | None] = mapped_column(String(5), default=None)
