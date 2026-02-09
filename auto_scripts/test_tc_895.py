# TC_ID 895
import requests
import json

def test_tc_895():
    url = 'https://example.com/api/permissions/update'
    payload = {"user_id": 1, "permission": "read", "value": True}
    headers = {'Authorization': 'Bearer testtoken', 'Content-Type': 'application/json'}
    response = requests.put(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['updated'] is True

if __name__ == "__main__":
    test_tc_895()
