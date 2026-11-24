import jwt
import pytest
from fastapi.testclient import TestClient

from app.db.connection import get_db
from app.main import app
from app.security.tokens import create_access_token
from app.services import user_service
from app.services.user_service import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    authenticate_user,
    register_user,
)


class FakeUserRepository:
    def __init__(self) -> None:
        self.users: dict[str, dict] = {}
        self.next_id = 1

    def get_user_by_email(self, connection, email: str) -> dict | None:
        return self.users.get(email)

    def create_user(self, connection, email: str, password_hash: str, role: str) -> dict:
        user = {"id": self.next_id, "email": email, "password_hash": password_hash, "role": role}
        self.users[email] = user
        self.next_id += 1
        return {"id": user["id"], "email": email, "role": role}


@pytest.fixture(autouse=True)
def jwt_secret(monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "segredo-de-teste")


@pytest.fixture
def repo(monkeypatch):
    fake = FakeUserRepository()
    monkeypatch.setattr(user_service, "user_repository", fake)
    return fake


@pytest.fixture
def client(repo):
    app.dependency_overrides[get_db] = lambda: None
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_register_normalizes_email_and_sets_user_role(repo):
    user = register_user(None, "Ana@Mail.com", "senha12345")

    assert user["email"] == "ana@mail.com"
    assert user["role"] == "user"


def test_register_rejects_duplicate_email(repo):
    register_user(None, "ana@mail.com", "senha12345")

    with pytest.raises(EmailAlreadyExistsError):
        register_user(None, "ANA@mail.com", "outra-senha")


def test_authenticate_accepts_correct_password(repo):
    register_user(None, "ana@mail.com", "senha12345")

    user = authenticate_user(None, "ana@mail.com", "senha12345")

    assert user["email"] == "ana@mail.com"
    assert "password_hash" not in user


def test_authenticate_rejects_wrong_password(repo):
    register_user(None, "ana@mail.com", "senha12345")

    with pytest.raises(InvalidCredentialsError):
        authenticate_user(None, "ana@mail.com", "senha-errada")


def test_authenticate_rejects_unknown_email(repo):
    with pytest.raises(InvalidCredentialsError):
        authenticate_user(None, "ninguem@mail.com", "senha12345")


def test_token_contains_role():
    token = create_access_token({"id": 1, "email": "admin@mail.com", "role": "admin"})

    payload = jwt.decode(token, "segredo-de-teste", algorithms=["HS256"])

    assert payload["role"] == "admin"
    assert payload["sub"] == "1"


def test_register_route_ignores_role_sent_by_client(client):
    response = client.post(
        "/auth/register",
        json={"email": "nova@mail.com", "password": "senha12345", "role": "admin"},
    )

    assert response.status_code == 201
    assert response.json()["role"] == "user"


def test_register_route_returns_409_for_duplicate_email(client):
    payload = {"email": "ana@mail.com", "password": "senha12345"}
    client.post("/auth/register", json=payload)

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 409


def test_login_route_returns_token(client):
    client.post("/auth/register", json={"email": "ana@mail.com", "password": "senha12345"})

    response = client.post("/auth/login", json={"email": "ana@mail.com", "password": "senha12345"})

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert "access_token" in response.json()


def test_login_route_returns_401_for_wrong_password(client):
    client.post("/auth/register", json={"email": "ana@mail.com", "password": "senha12345"})

    response = client.post("/auth/login", json={"email": "ana@mail.com", "password": "errada"})

    assert response.status_code == 401