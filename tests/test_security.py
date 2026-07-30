from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_generate_password():

    response = client.get(
        "/api/v1/security/generate-password"
    )

    assert response.status_code == 200

    assert "password" in response.json()