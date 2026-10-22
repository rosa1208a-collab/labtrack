from datetime import timedelta

import pytest
from sqlalchemy import select

from app.models import AuthSession, User, utcnow
from app.security import COOKIE_NAME
from tests.conftest import PASSWORD, login


def test_health_and_frontend(client):
    assert client.get("/health").json() == {"status": "ok"}
    response = client.get("/")
    assert response.status_code == 200
    assert "LabTrack" in response.text
    assert "frame-ancestors 'none'" in response.headers["content-security-policy"]


@pytest.mark.parametrize(
    "path", ["/api/projects", "/api/summary", "/api/auth/me", "/api/experiments/1"]
)
def test_requires_login(client, path):
    assert client.get(path).status_code == 401


def test_cookie_logout_and_revocation(client, app):
    response = login(client)
    assert "httponly" in response.headers["set-cookie"].lower()
    token = client.cookies.get(COOKIE_NAME)
    assert client.get("/api/auth/me").json()["email"] == "ana@example.com"
    with app.state.session_factory() as db:
        assert db.scalar(select(AuthSession)).token_hash != token
        assert db.scalar(select(User)).password_hash != PASSWORD
    assert client.post("/api/auth/logout").status_code == 204
    client.cookies.set(COOKIE_NAME, token)
    assert client.get("/api/auth/me").status_code == 401


def test_csrf_origin_and_expiry(authenticated, app):
    client = authenticated
    assert (
        client.post(
            "/api/projects", json={"name": "A"}, headers={"X-CSRF-Token": "wrong"}
        ).status_code
        == 403
    )
    assert (
        client.post(
            "/api/projects", json={"name": "A"}, headers={"Origin": "https://other.example"}
        ).status_code
        == 403
    )
    with app.state.session_factory() as db:
        db.scalar(select(AuthSession)).expires_at = utcnow() - timedelta(seconds=1)
        db.commit()
    assert client.get("/api/auth/me").status_code == 401


def test_login_origin_and_generic_error(client):
    payload = {"email": "ana@example.com", "password": "bad"}
    assert (
        client.post(
            "/api/auth/login", json=payload, headers={"Origin": "https://other.example"}
        ).status_code
        == 403
    )
    known = client.post("/api/auth/login", json=payload)
    payload["email"] = "unknown@example.com"
    unknown = client.post("/api/auth/login", json=payload)
    assert known.status_code == unknown.status_code == 401
    assert known.json() == unknown.json()


def test_login_throttle(client):
    payload = {"email": "ana@example.com", "password": "bad"}
    for _ in range(5):
        assert client.post("/api/auth/login", json=payload).status_code == 401
    assert client.post("/api/auth/login", json=payload).status_code == 429


def test_login_rotates_session(client):
    login(client)
    old = client.cookies.get(COOKIE_NAME)
    login(client)
    client.cookies.clear()
    client.cookies.set(COOKIE_NAME, old)
    assert client.get("/api/auth/me").status_code == 401
