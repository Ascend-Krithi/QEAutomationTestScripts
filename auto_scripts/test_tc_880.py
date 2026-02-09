# TC_ID 880
import requests
import json

def test_tc_880():
    url = 'https://example.com/api/update'
    payload = {"item_id": 111, "new_value": "updated"}
    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['updated'] is True

if __name__ == "__main__":
    test_tc_880()
