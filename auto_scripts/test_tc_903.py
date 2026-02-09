# TC_ID 903
import requests
import json

def test_tc_903():
    url = 'https://example.com/api/maintenance/toggle'
    payload = {"enable": True}
    headers = {'Authorization': 'Bearer testtoken', 'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['maintenance'] is True

if __name__ == "__main__":
    test_tc_903()
