from datetime import datetime

from pydantic import ConfigDict, EmailStr, Field, field_validator

from app.models.user import UserRole
from app.schemas.resource import CamelModel

# doar adresele institutionale au voie sa-si faca cont
ALLOWED_DOMAINS = ("student.usv.ro", "usm.ro")


class UserRegister(CamelModel):
    email: EmailStr = Field(examples=["ion.popescu@student.usv.ro"])
    password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(min_length=1, max_length=100, examples=["Ion"])
    last_name: str = Field(min_length=1, max_length=100, examples=["Popescu"])

    @field_validator("email")
    @classmethod
    def check_usv_email(cls, email: str) -> str:
        email = email.lower()
        if email.rsplit("@", 1)[1] not in ALLOWED_DOMAINS:
            raise ValueError("Se accepta doar adrese @student.usv.ro sau @usm.ro")
        return email


class UserLogin(CamelModel):
    email: EmailStr
    password: str


class UserRead(CamelModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    first_name: str
    last_name: str
    role: UserRole
    blocked_until: datetime | None
    created_at: datetime


class Token(CamelModel):
    access_token: str
    token_type: str = "bearer"
