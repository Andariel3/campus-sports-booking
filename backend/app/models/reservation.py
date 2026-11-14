from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ReservationStatus(StrEnum):
    # valorile din booking_status_enum (schema BD)
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    NO_SHOW = "NoShow"


class Reservation(Base):
    """O rezervare a unei resurse pe un interval. In baza de date tabela se numeste bookings."""

    __tablename__ = "bookings"
    __table_args__ = (
        CheckConstraint("start_time < end_time", name="check_booking_dates"),
        Index("idx_bookings_user_date", "user_id", "start_time"),
        Index("idx_bookings_resource_date", "resource_id", "start_time"),
        # doua rezervari active nu se pot suprapune pe aceeasi resursa.
        # e doar pe postgres (are nevoie de extensia btree_gist), in testele cu sqlite nu exista
        ExcludeConstraint(
            ("resource_id", "="),
            (text("tstzrange(start_time, end_time)"), "&&"),
            name="prevent_overlapping_bookings",
            using="gist",
            where=text("status != 'Cancelled'"),
        ).ddl_if(dialect="postgresql"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.id", ondelete="CASCADE"))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[ReservationStatus] = mapped_column(
        Enum(
            ReservationStatus,
            name="booking_status_enum",
            values_callable=lambda e: [m.value for m in e],
        ),
        default=ReservationStatus.CONFIRMED,
    )
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    is_open: Mapped[bool] = mapped_column(Boolean, default=False)
    max_participants: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancelled_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
