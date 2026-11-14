from fastapi import APIRouter

from app.core.deps import CurrentUser
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead, summary="Datele utilizatorului logat")
def me(user: CurrentUser):
    return user
