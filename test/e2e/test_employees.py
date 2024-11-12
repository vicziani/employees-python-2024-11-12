import requests
import os

def test_create():
    # When
    DEFAULT_HOST = 'http://localhost:5000'
    HOST = os.environ.get("EMPLOYEES_URL", DEFAULT_HOST)

    response = requests.post(HOST + "/api/employees", json={"name": "John Doe"})    
    # Then
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["name"] == "John Doe"
