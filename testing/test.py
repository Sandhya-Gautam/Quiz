import pytest
import requests


@pytest.fixture
def setup_data():
    body = {"email": "test@gmail.com", "password": "123"}
    yield body
    del body


def test_login():
    url = "http://127.0.0.1:8000/app/login/"
    body = {"email": "test@gmail.com", "password": "123"}
    response = requests.post(url, data=body)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    data = response.json()
    assert "token" in data
    assert "msg" in data
    assert data["msg"] == "user login sucessful"


def test_register():
    url = "http://127.0.0.1:8000/app/register/"
    data = {"email": "pqtrs@gmail.com", "username": "pqtrs", "password": "pqt"}
    response = requests.post(url, data=data)
    assert response.status_code == 201
    data = response.json()
    assert "msg" in data


def test_getQuestion(benchmark):
    url = "http://127.0.0.1:8000/app/get_question/"
    headers = {"Authorization": "Token 18f1a487fbd3a79af99897a421143e34a76eca9d"}
    response = benchmark(lambda: requests.get(url, headers=headers))
    assert response.status_code == 200
    data = response.json()
    assert "question" in data
    assert "answers" in data


def test_checkQuestion(benchmark):
    url = "http://127.0.0.1:8000/app/check_answer/"
    body = {"id": "2"}
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Token 18f1a487fbd3a79af99897a421143e34a76eca9d",
    }
    response = benchmark(lambda: requests.put(url, headers=headers, json=body))
    assert response.status_code == 200
    data = response.json()
    assert "msg" in data
