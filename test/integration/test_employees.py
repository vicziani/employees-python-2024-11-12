import pytest

from employees import app


@pytest.fixture(name="client")
def fixture_client():
    with app.test_client() as client:
        yield client


def test_find_all(client):
    response = client.post("/api/employees", json={"name": "John Doe"})
    json_data = response.get_json()
    assert response.status_code == 201
    assert json_data["name"] == "John Doe"
