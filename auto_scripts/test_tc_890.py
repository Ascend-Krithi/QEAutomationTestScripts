# TC_ID 890
import requests
import json

def test_tc_890():
    url = 'https://example.com/api/forgot-username'
    payload = {"email": "user@example.com"}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['username_sent'] is True

if __name__ == "__main__":
    test_tc_890()
