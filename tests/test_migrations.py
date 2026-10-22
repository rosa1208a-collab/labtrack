from alembic import command
from sqlalchemy import inspect

from app.db import make_engine
from tests.conftest import migration_config


def test_migrations_match_models_and_are_repeatable(database_url):
    config = migration_config(database_url)
    command.upgrade(config, "head")
    command.check(config)
    command.downgrade(config, "base")
    command.upgrade(config, "head")
    engine = make_engine(database_url)
    assert {"users", "projects", "experiments", "auth_sessions"}.issubset(
        inspect(engine).get_table_names()
    )
    engine.dispose()
