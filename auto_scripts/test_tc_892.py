# TC_ID 892
import requests
import json

def test_tc_892():
    url = 'https://example.com/api/roles/assign'
    payload = {"user_id": 1, "role": "admin"}
    headers = {'Authorization': 'Bearer testtoken', 'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['assigned'] is True

if __name__ == "__main__":
    test_tc_892()
