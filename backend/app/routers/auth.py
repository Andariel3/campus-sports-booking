from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.user import Token, UserLogin, UserRead, UserRegister
from app.services import auth_service
from app.services.auth_service import EmailAlreadyUsedError

router = APIRouter(prefix="/auth", tags=["auth"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Creare cont cu email institutional",
)
def register(data: UserRegister, db: DbSession):
    try:
        return auth_service.register_user(db, data)
    except EmailAlreadyUsedError:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Exista deja un cont cu acest email"
        ) from None


@router.post("/login", response_model=Token, summary="Login, intoarce tokenul JWT")
def login(data: UserLogin, db: DbSession):
    user = auth_service.authenticate(db, data.email, data.password)
    if user is None:
        # acelasi mesaj si pentru email inexistent, ca sa nu se poata afla ce conturi exista
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Email sau parola gresita")
    return Token(access_token=create_access_token(user.id))
