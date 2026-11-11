from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.facility import SportType
from app.schemas.facility import FacilityCreate, FacilityRead, FacilityUpdate
from app.services import facility_service
from app.services.facility_service import DuplicateFacilityNameError, FacilityNotFoundError

router = APIRouter(prefix="/api/facilities", tags=["facilities"])


@router.get("", response_model=list[FacilityRead])
def list_facilities(sport: SportType | None = None, db: Session = Depends(get_db)):
    return facility_service.list_facilities(db, sport)


@router.get("/{facility_id}", response_model=FacilityRead)
def get_facility(facility_id: int, db: Session = Depends(get_db)):
    try:
        return facility_service.get_facility(db, facility_id)
    except FacilityNotFoundError:
        raise _not_found(facility_id) from None


@router.post("", response_model=FacilityRead, status_code=status.HTTP_201_CREATED)
def create_facility(data: FacilityCreate, db: Session = Depends(get_db)):
    try:
        return facility_service.create_facility(db, data)
    except DuplicateFacilityNameError:
        raise _duplicate_name() from None


@router.patch("/{facility_id}", response_model=FacilityRead)
def update_facility(facility_id: int, data: FacilityUpdate, db: Session = Depends(get_db)):
    try:
        return facility_service.update_facility(db, facility_id, data)
    except FacilityNotFoundError:
        raise _not_found(facility_id) from None
    except DuplicateFacilityNameError:
        raise _duplicate_name() from None


@router.delete("/{facility_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_facility(facility_id: int, db: Session = Depends(get_db)) -> None:
    try:
        facility_service.delete_facility(db, facility_id)
    except FacilityNotFoundError:
        raise _not_found(facility_id) from None


def _not_found(facility_id: int) -> HTTPException:
    return HTTPException(status.HTTP_404_NOT_FOUND, f"Facility {facility_id} not found")


def _duplicate_name() -> HTTPException:
    return HTTPException(status.HTTP_409_CONFLICT, "A facility with this name already exists")
