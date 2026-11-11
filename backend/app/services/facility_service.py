from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.facility import Facility, SportType
from app.schemas.facility import FacilityCreate, FacilityUpdate


class FacilityNotFoundError(Exception):
    pass


class DuplicateFacilityNameError(Exception):
    pass


def list_facilities(db: Session, sport: SportType | None = None) -> list[Facility]:
    query = select(Facility).order_by(Facility.name)
    if sport is not None:
        query = query.where(Facility.sport == sport)
    return list(db.scalars(query))


def get_facility(db: Session, facility_id: int) -> Facility:
    facility = db.get(Facility, facility_id)
    if facility is None:
        raise FacilityNotFoundError(facility_id)
    return facility


def create_facility(db: Session, data: FacilityCreate) -> Facility:
    facility = Facility(**data.model_dump())
    db.add(facility)
    _commit(db)
    db.refresh(facility)
    return facility


def update_facility(db: Session, facility_id: int, data: FacilityUpdate) -> Facility:
    facility = get_facility(db, facility_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(facility, field, value)
    _commit(db)
    db.refresh(facility)
    return facility


def delete_facility(db: Session, facility_id: int) -> None:
    facility = get_facility(db, facility_id)
    db.delete(facility)
    db.commit()


def _commit(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateFacilityNameError from exc
