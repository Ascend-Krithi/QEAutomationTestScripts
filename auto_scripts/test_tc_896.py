# TC_ID 896
import requests
import json

def test_tc_896():
    url = 'https://example.com/api/permissions/remove'
    payload = {"user_id": 1, "permission": "read"}
    headers = {'Authorization': 'Bearer testtoken', 'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['removed'] is True

if __name__ == "__main__":
    test_tc_896()
