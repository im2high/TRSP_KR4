import pytest
from faker import Faker
from httpx import ASGITransport, AsyncClient

from app.main import app

faker = Faker()

pytestmark = pytest.mark.asyncio


def make_user() -> dict:
    return {"username": faker.user_name(), "age": faker.random_int(min=19, max=90)}


async def _client() -> AsyncClient:
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


class TestUsersAsync:
    async def test_create_user(self):
        async with await _client() as ac:
            payload = make_user()
            resp = await ac.post("/users", json=payload)
            assert resp.status_code == 201
            data = resp.json()
            assert data["id"] >= 1
            assert data["username"] == payload["username"]
            assert data["age"] == payload["age"]

    async def test_get_existing_user(self):
        async with await _client() as ac:
            created = (await ac.post("/users", json=make_user())).json()
            resp = await ac.get(f"/users/{created['id']}")
            assert resp.status_code == 200
            assert resp.json() == created

    async def test_get_missing_user(self):
        async with await _client() as ac:
            resp = await ac.get("/users/999999")
            assert resp.status_code == 404
            assert resp.json()["detail"] == "User not found"

    async def test_delete_existing_user(self):
        async with await _client() as ac:
            created = (await ac.post("/users", json=make_user())).json()
            resp = await ac.delete(f"/users/{created['id']}")
            assert resp.status_code == 204

    async def test_delete_twice_returns_404(self):
        async with await _client() as ac:
            created = (await ac.post("/users", json=make_user())).json()
            first = await ac.delete(f"/users/{created['id']}")
            second = await ac.delete(f"/users/{created['id']}")
            assert first.status_code == 204
            assert second.status_code == 404
