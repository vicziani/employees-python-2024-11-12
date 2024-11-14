import pytest

from employees import app


@pytest.fixture(name="client")
def fixture_client():
    with app.test_client() as client:
        yield client


def test_find_all(client, mocker):
    mocker.patch("employees.repo.init")

    mocker.patch(
        "employees.repo.find_all",
        return_value=[
            {"id": 1, "name": "Jack Doe"},
            {"id": 2, "name": "Jane Doe"},
        ],
    )

    response = client.get("/api/employees")
    json_data = response.get_json()
    assert response.status_code == 200
    assert len(json_data) == 2
