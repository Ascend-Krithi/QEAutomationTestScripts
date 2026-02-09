# TC_ID 877
import requests
import json

def test_tc_877():
    url = 'https://example.com/api/login'
    payload = {"username": "admin", "password": "password123"}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'token' in data

if __name__ == "__main__":
    test_tc_877()
