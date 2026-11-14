from collections.abc import Generator
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.schema import CreateTable

from app.db.base import Base
from app.models import (
    MaintenanceBlock,
    Reservation,
    ReservationStatus,
    Resource,
    ResourceType,
    User,
    UserRole,
)

START = datetime(2026, 11, 20, 18, 0, tzinfo=UTC)


@pytest.fixture
def db() -> Generator[Session, None, None]:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


def add_user_and_resource(db: Session) -> tuple[User, Resource]:
    user = User(
        email="ion.popescu@student.usv.ro",
        first_name="Ion",
        last_name="Popescu",
        password_hash="x",
    )
    resource = Resource(name="Teren tenis 1", type=ResourceType.TEREN, sport="tenis")
    db.add_all([user, resource])
    db.commit()
    return user, resource


def test_new_user_is_student_by_default(db: Session) -> None:
    user, _ = add_user_and_resource(db)
    assert user.role == UserRole.STUDENT
    assert user.blocked_until is None


def test_new_reservation_is_confirmed_and_unpaid(db: Session) -> None:
    user, resource = add_user_and_resource(db)
    reservation = Reservation(
        user_id=user.id,
        resource_id=resource.id,
        start_time=START,
        end_time=START + timedelta(hours=1),
        amount=Decimal("40.00"),
    )
    db.add(reservation)
    db.commit()

    assert reservation.status == ReservationStatus.CONFIRMED
    assert reservation.is_paid is False
    assert reservation.cancelled_at is None


def test_reservation_end_must_be_after_start(db: Session) -> None:
    user, resource = add_user_and_resource(db)
    db.add(
        Reservation(
            user_id=user.id,
            resource_id=resource.id,
            start_time=START,
            end_time=START,
            amount=Decimal("0"),
        )
    )
    with pytest.raises(IntegrityError):
        db.commit()


def test_maintenance_end_must_be_after_start(db: Session) -> None:
    _, resource = add_user_and_resource(db)
    db.add(
        MaintenanceBlock(
            resource_id=resource.id,
            start_time=START,
            end_time=START - timedelta(hours=1),
        )
    )
    with pytest.raises(IntegrityError):
        db.commit()


def test_overlap_constraint_only_on_postgres() -> None:
    table = Reservation.__table__
    postgres_ddl = str(CreateTable(table).compile(dialect=postgresql.dialect()))
    sqlite_ddl = str(CreateTable(table).compile(dialect=sqlite.dialect()))

    assert "EXCLUDE USING gist" in postgres_ddl
    assert "status != 'Cancelled'" in postgres_ddl
    assert "EXCLUDE" not in sqlite_ddl
