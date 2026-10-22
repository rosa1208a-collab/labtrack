import os
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.engine import make_url

from app.config import Settings
from app.db import Base, make_engine
from app.main import create_app
from app.models import User
from app.security import password_hasher

PASSWORD = "labtrack-test-password-2026"
ROOT = Path(__file__).resolve().parent.parent
TARGETS = ["sqlite"] + (["postgresql"] if os.environ.get("TEST_DATABASE_URL") else [])


def migration_config(url):
    config = Config(str(ROOT / "alembic.ini"))
    config.attributes["database_url"] = url
    return config


@pytest.fixture(params=TARGETS)
def database_url(request, tmp_path):
    if request.param == "sqlite":
        url = f"sqlite:///{tmp_path / 'test.db'}"
    else:
        url = os.environ["TEST_DATABASE_URL"]
        # Esta fixture elimina tablas: nunca debe apuntar a la base de la app.
        if not (make_url(url).database or "").endswith("_test"):
            pytest.fail("TEST_DATABASE_URL debe usar una base cuyo nombre termine en _test")
    engine = make_engine(url)
    Base.metadata.drop_all(engine)
    from sqlalchemy import text

    with engine.begin() as connection:
        connection.execute(text("DROP TABLE IF EXISTS alembic_version"))
    command.upgrade(migration_config(url), "head")
    yield url
    engine.dispose()


@pytest.fixture
def app(database_url):
    application = create_app(
        Settings(_env_file=None, database_url=database_url, allowed_origins=["http://testserver"])
    )
    with application.state.session_factory() as db:
        db.add_all(
            [
                User(email=f"{name}@example.com", password_hash=password_hasher.hash(PASSWORD))
                for name in ["ana", "luis"]
            ]
        )
        db.commit()
    yield application
    application.state.engine.dispose()


@pytest.fixture
def client(app):
    with TestClient(app, headers={"Origin": "http://testserver"}) as browser:
        yield browser


def login(client, name="ana"):
    response = client.post(
        "/api/auth/login", json={"email": f"{name}@example.com", "password": PASSWORD}
    )
    assert response.status_code == 200, response.text
    client.headers["X-CSRF-Token"] = response.json()["csrf_token"]
    return response


@pytest.fixture
def authenticated(client):
    login(client)
    return client
