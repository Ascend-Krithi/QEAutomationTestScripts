# TC_ID 893
import requests
import json

def test_tc_893():
    url = 'https://example.com/api/roles/remove'
    payload = {"user_id": 1, "role": "admin"}
    headers = {'Authorization': 'Bearer testtoken', 'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['removed'] is True

if __name__ == "__main__":
    test_tc_893()
