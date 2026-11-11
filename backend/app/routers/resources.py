from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.resource import ResourceType
from app.schemas.resource import ResourceCreate, ResourceRead, ResourceUpdate
from app.services import resource_service
from app.services.resource_service import DuplicateResourceNameError, ResourceNotFoundError

router = APIRouter(prefix="/resources", tags=["resources"])

# the contract names the path parameter resourceId
ResourceId = Annotated[int, Path(alias="resourceId")]
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[ResourceRead], summary="Lista resurselor sportive")
def list_resources(
    db: DbSession,
    sport: Annotated[str | None, Query(description="Filtrare dupa sport")] = None,
    resource_type: Annotated[ResourceType | None, Query(alias="type")] = None,
):
    return resource_service.list_resources(db, sport, resource_type)


@router.post(
    "",
    response_model=ResourceRead,
    status_code=status.HTTP_201_CREATED,
    summary="Adaugare resursa (admin)",
)
def create_resource(data: ResourceCreate, db: DbSession):
    try:
        return resource_service.create_resource(db, data)
    except DuplicateResourceNameError:
        raise _duplicate_name() from None


@router.get("/{resourceId}", response_model=ResourceRead, summary="Detalii resursa")
def get_resource(resource_id: ResourceId, db: DbSession):
    try:
        return resource_service.get_resource(db, resource_id)
    except ResourceNotFoundError:
        raise _not_found(resource_id) from None


@router.patch("/{resourceId}", response_model=ResourceRead, summary="Modificare resursa (admin)")
def update_resource(resource_id: ResourceId, data: ResourceUpdate, db: DbSession):
    try:
        return resource_service.update_resource(db, resource_id, data)
    except ResourceNotFoundError:
        raise _not_found(resource_id) from None
    except DuplicateResourceNameError:
        raise _duplicate_name() from None
    except ValueError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from None


@router.delete(
    "/{resourceId}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Stergere resursa (admin)",
)
def delete_resource(resource_id: ResourceId, db: DbSession) -> None:
    try:
        resource_service.delete_resource(db, resource_id)
    except ResourceNotFoundError:
        raise _not_found(resource_id) from None


def _not_found(resource_id: int) -> HTTPException:
    return HTTPException(status.HTTP_404_NOT_FOUND, f"Resursa {resource_id} nu exista")


def _duplicate_name() -> HTTPException:
    return HTTPException(status.HTTP_409_CONFLICT, "Exista deja o resursa cu acest nume")
