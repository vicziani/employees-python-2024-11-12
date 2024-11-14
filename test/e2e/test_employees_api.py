import requests
import os


def test_create():
    DEFAULT_URL = "http://localhost:5000"
    url = os.getenv("EMPLOYEES_URL", DEFAULT_URL)

    response = requests.post(url + "/api/employees", json={"name": "John Doe"})

    assert response.status_code == 201
    json_data = response.json()
    assert json_data["name"] == "John Doe"
