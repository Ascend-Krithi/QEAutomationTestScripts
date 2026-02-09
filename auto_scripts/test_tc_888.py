# TC_ID 888
import requests
import json

def test_tc_888():
    url = 'https://example.com/api/register'
    payload = {"username": "newuser", "email": "newuser@example.com", "password": "pass1234"}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data['status'] == 'registered'

if __name__ == "__main__":
    test_tc_888()
