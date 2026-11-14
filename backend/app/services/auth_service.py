from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User, UserRole
from app.schemas.user import UserRegister


class EmailAlreadyUsedError(Exception):
    pass


def role_for_email(email: str) -> UserRole:
    """Rolul se stabileste dupa domeniu: @student.usv.ro e student, @usm.ro e profesor.

    Adminii nu se pot inregistra singuri, contul lor se creeaza direct in baza de date.
    """
    if email.endswith("@usm.ro"):
        return UserRole.PROFESSOR
    return UserRole.STUDENT


def register_user(db: Session, data: UserRegister) -> User:
    user = User(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        password_hash=hash_password(data.password),
        role=role_for_email(data.email),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise EmailAlreadyUsedError from exc
    db.refresh(user)
    return user


def authenticate(db: Session, email: str, password: str) -> User | None:
    user = db.scalar(select(User).where(User.email == email.lower()))
    if user is None or not verify_password(password, user.password_hash):
        return None
    return user
