import requests
import json


def test_login():
    url = "http://127.0.0.1:8000/app/login/"
    data = {"email": "test@gmail.com", "password": "123"}
    response = requests.post(url, data=data)
    assert response.status_code == 200


def test_register():
    url='http://127.0.0.1:8000/app/register/'
    data={"email":"pqt@gmail.com","username":"pqt","password":"pqt"}
    response=requests.post(url,data=data)
    assert response.status_code==201


def test_getQuestion():
    url = "http://127.0.0.1:8000/app/get_question/"
    headers = {"Authorization": "Token 18f1a487fbd3a79af99897a421143e34a76eca9d"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200


def test_checkQuestion():
    url = "http://127.0.0.1:8000/app/check_answer/"
    body = {"id": "2"}
    headers = {"accept": "application/json", "Content-Type": "application/json","Authorization": "Token 18f1a487fbd3a79af99897a421143e34a76eca9d"}
    response = requests.put(url, headers=headers, data=json.dumps(body))
    assert response.status_code == 200
