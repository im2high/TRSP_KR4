import pytest

from app.routers import users as users_module


@pytest.fixture(autouse=True)
def clean_inmemory_db():
    """Изоляция состояния between tests (задание 11.2, п.5)."""
    users_module.db.clear()
    yield
    users_module.db.clear()
