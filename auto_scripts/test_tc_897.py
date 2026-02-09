# TC_ID 897
import requests
import json

def test_tc_897():
    url = 'https://example.com/api/audit/logs'
    headers = {'Authorization': 'Bearer testtoken'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data['logs'], list)

if __name__ == "__main__":
    test_tc_897()
