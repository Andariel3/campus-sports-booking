from datetime import UTC, datetime, timedelta

import jwt
import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings

REGISTER = "/api/v1/auth/register"
LOGIN = "/api/v1/auth/login"
ME = "/api/v1/users/me"

STUDENT = {
    "email": "ion.popescu@student.usv.ro",
    "password": "parola-buna-123",
    "firstName": "Ion",
    "lastName": "Popescu",
}


def register(client: TestClient, **overrides):
    return client.post(REGISTER, json={**STUDENT, **overrides})


def login_token(client: TestClient, email: str, password: str) -> str:
    response = client.post(LOGIN, json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return response.json()["accessToken"]


def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_register_student(client: TestClient) -> None:
    response = register(client)

    assert response.status_code == 201, response.text
    body = response.json()
    assert body["email"] == "ion.popescu@student.usv.ro"
    assert body["role"] == "Student"
    assert body["blockedUntil"] is None
    assert "password" not in body and "passwordHash" not in body


def test_usm_email_gets_professor_role(client: TestClient) -> None:
    response = register(client, email="maria.ionescu@usm.ro")
    assert response.json()["role"] == "Professor"


def test_email_is_saved_lowercase(client: TestClient) -> None:
    response = register(client, email="Ion.Popescu@Student.USV.ro")
    assert response.json()["email"] == "ion.popescu@student.usv.ro"


@pytest.mark.parametrize(
    "email",
    ["ion@gmail.com", "ion@usv.ro", "ion@student.usv.ro.evil.com", "nu-e-email"],
)
def test_register_rejects_non_usv_emails(client: TestClient, email: str) -> None:
    response = register(client, email=email)
    assert response.status_code == 422
    assert isinstance(response.json()["detail"], str)


def test_register_rejects_short_password(client: TestClient) -> None:
    assert register(client, password="1234567").status_code == 422


def test_register_same_email_twice_returns_409(client: TestClient) -> None:
    register(client)
    response = register(client, email="ION.POPESCU@student.usv.ro")

    assert response.status_code == 409
    assert response.json() == {"detail": "Exista deja un cont cu acest email"}


def test_login_returns_bearer_token(client: TestClient) -> None:
    register(client)
    response = client.post(LOGIN, json={"email": STUDENT["email"], "password": STUDENT["password"]})

    assert response.status_code == 200
    assert response.json()["tokenType"] == "bearer"
    assert response.json()["accessToken"]


def test_login_wrong_password_returns_401(client: TestClient) -> None:
    register(client)
    response = client.post(LOGIN, json={"email": STUDENT["email"], "password": "gresita-123"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Email sau parola gresita"}


def test_login_unknown_email_returns_same_401(client: TestClient) -> None:
    response = client.post(LOGIN, json={"email": "nimeni@student.usv.ro", "password": "orice-123"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Email sau parola gresita"}


def test_me_returns_logged_user(client: TestClient) -> None:
    register(client)
    token = login_token(client, STUDENT["email"], STUDENT["password"])

    response = client.get(ME, headers=auth(token))

    assert response.status_code == 200
    assert response.json()["email"] == STUDENT["email"]
    assert response.json()["firstName"] == "Ion"


def test_me_without_token_returns_401(client: TestClient) -> None:
    response = client.get(ME)
    assert response.status_code == 401
    assert response.json() == {"detail": "Nu sunteti autentificat"}


def test_me_with_bad_token_returns_401(client: TestClient) -> None:
    assert client.get(ME, headers=auth("nu.e.token")).status_code == 401


def test_me_with_expired_token_returns_401(client: TestClient) -> None:
    register(client)
    settings = get_settings()
    expired = jwt.encode(
        {"sub": "1", "exp": datetime.now(UTC) - timedelta(minutes=1)},
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    assert client.get(ME, headers=auth(expired)).status_code == 401


def test_me_with_token_signed_by_other_secret_returns_401(client: TestClient) -> None:
    register(client)
    forged = jwt.encode({"sub": "1"}, "alt-secret-de-cel-putin-32-caractere!!", algorithm="HS256")
    assert client.get(ME, headers=auth(forged)).status_code == 401


def test_me_for_deleted_user_returns_401(client: TestClient) -> None:
    settings = get_settings()
    token = jwt.encode({"sub": "999"}, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    assert client.get(ME, headers=auth(token)).status_code == 401
