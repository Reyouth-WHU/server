from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_username, random_lower_string


def test_create_user(client: TestClient) -> None:
    username = random_username()
    password = random_lower_string()
    data = {"username": username, "password": password}
    # 这里必须指定为 json 参数
    r = client.post(
        f"{settings.API_VERSION}/users/", json=data,
    )
    new_user = r.json()
    assert new_user
    assert new_user["is_active"] is True
    assert new_user["is_superuser"] is False
    assert new_user.get("password") is None
    assert new_user["username"] == username
    assert 200 <= r.status_code < 300


def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_VERSION}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is True
    assert current_user["username"] == settings.FIRST_SUPERUSER
    assert current_user.get("password") is None
    assert 200 <= r.status_code < 300


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_VERSION}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert 200 <= r.status_code < 300
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["username"] == settings.USERNAME_TEST_USER


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_username()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_id = user.id
    r = client.get(
        f"{settings.API_VERSION}/users/{user_id}", headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.user.get_by_username(db, username=username)
    assert existing_user
    assert existing_user.username == api_user["username"]


def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_username()
    # username = username
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    crud.user.create(db, obj_in=user_in)
    data = {"username": username, "password": password}
    r = client.post(
        f"{settings.API_VERSION}/users/", headers=superuser_token_headers, json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "username" not in created_user


if __name__ == '__main__':
    from app.main import app
    client = TestClient(app)
    test_create_user(client)
