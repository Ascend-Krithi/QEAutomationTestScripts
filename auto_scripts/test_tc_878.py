# TC_ID 878
import requests
import json

def test_tc_878():
    url = 'https://example.com/api/items'
    payload = {"item_id": 12345}
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, params=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['item']['id'] == 12345

if __name__ == "__main__":
    test_tc_878()
