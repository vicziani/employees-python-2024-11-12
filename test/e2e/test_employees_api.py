import os

import requests


def test_create():
    default_url = "http://localhost:5000"
    url = os.getenv("EMPLOYEES_URL", default_url)

    response = requests.post(
        url + "/api/employees", json={"name": "John Doe"}, timeout=5
    )  # 5sec

    assert response.status_code == 201
    json_data = response.json()
    assert json_data["name"] == "John Doe"
