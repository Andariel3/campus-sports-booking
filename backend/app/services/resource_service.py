from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.resource import Resource, ResourceType
from app.schemas.resource import ResourceCreate, ResourceUpdate, _check_open_before_close


class ResourceNotFoundError(Exception):
    pass


class DuplicateResourceNameError(Exception):
    pass


def list_resources(
    db: Session, sport: str | None = None, resource_type: ResourceType | None = None
) -> list[Resource]:
    query = select(Resource).order_by(Resource.name)
    if sport:
        query = query.where(func.lower(Resource.sport) == sport.lower())
    if resource_type is not None:
        query = query.where(Resource.type == resource_type)
    return list(db.scalars(query))


def get_resource(db: Session, resource_id: int) -> Resource:
    resource = db.get(Resource, resource_id)
    if resource is None:
        raise ResourceNotFoundError(resource_id)
    return resource


def create_resource(db: Session, data: ResourceCreate) -> Resource:
    resource = Resource(**data.model_dump())
    db.add(resource)
    _commit(db)
    db.refresh(resource)
    return resource


def update_resource(db: Session, resource_id: int, data: ResourceUpdate) -> Resource:
    resource = get_resource(db, resource_id)
    changes = data.model_dump(exclude_unset=True)
    # the new hours may be checked against the ones already saved
    _check_open_before_close(
        changes.get("open_hour", resource.open_hour),
        changes.get("close_hour", resource.close_hour),
    )
    for field, value in changes.items():
        setattr(resource, field, value)
    _commit(db)
    db.refresh(resource)
    return resource


def delete_resource(db: Session, resource_id: int) -> None:
    resource = get_resource(db, resource_id)
    db.delete(resource)
    db.commit()


def _commit(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateResourceNameError from exc
