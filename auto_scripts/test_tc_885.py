# TC_ID 885
import requests
import json

def test_tc_885():
    url = 'https://example.com/api/settings'
    headers = {'Authorization': 'Bearer testtoken'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'settings' in data

if __name__ == "__main__":
    test_tc_885()
