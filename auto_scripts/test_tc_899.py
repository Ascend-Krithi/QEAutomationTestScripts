# TC_ID 899
import requests
import json

def test_tc_899():
    url = 'https://example.com/api/audit/clear'
    headers = {'Authorization': 'Bearer testtoken'}
    response = requests.post(url, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['cleared'] is True

if __name__ == "__main__":
    test_tc_899()
