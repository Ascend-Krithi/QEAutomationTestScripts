# TC_ID 889
import requests
import json

def test_tc_889():
    url = 'https://example.com/api/verify-email'
    payload = {"email": "newuser@example.com", "code": "123456"}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['verified'] is True

if __name__ == "__main__":
    test_tc_889()
