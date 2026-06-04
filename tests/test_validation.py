from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID = {
    "username": "john_doe",
    "age": 25,
    "email": "john@example.com",
    "password": "secret123",
    "phone": "+79990000000",
}


class TestUserValidation:
    def test_valid_user(self):
        resp = client.post("/users/validate", json=VALID)
        assert resp.status_code == 201
        assert resp.json()["status"] == "ok"

    def test_phone_is_optional(self):
        payload = {k: v for k, v in VALID.items() if k != "phone"}
        resp = client.post("/users/validate", json=payload)
        assert resp.status_code == 201
        assert resp.json()["user"]["phone"] == "Unknown"

    def test_age_must_be_gt_18(self):
        payload = {**VALID, "age": 18}
        resp = client.post("/users/validate", json=payload)
        assert resp.status_code == 422
        body = resp.json()
        assert body["error"] == "ValidationError"
        assert "errors" in body["details"]

    def test_invalid_email(self):
        payload = {**VALID, "email": "not-an-email"}
        resp = client.post("/users/validate", json=payload)
        assert resp.status_code == 422

    def test_short_password(self):
        payload = {**VALID, "password": "123"}
        resp = client.post("/users/validate", json=payload)
        assert resp.status_code == 422


class TestCustomExceptions:
    def test_custom_exception_a(self):
        resp = client.get("/demo/check/0")
        assert resp.status_code == 400
        assert resp.json()["error"] == "BusinessRuleViolation"

    def test_custom_exception_b(self):
        resp = client.get("/demo/resource/999")
        assert resp.status_code == 404
        assert resp.json()["error"] == "ResourceNotFound"

    def test_resource_found(self):
        resp = client.get("/demo/resource/1")
        assert resp.status_code == 200
        assert resp.json()["name"] == "alpha"
