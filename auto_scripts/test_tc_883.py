# TC_ID 883
import requests
import json

def test_tc_883():
    url = 'https://example.com/api/profile'
    headers = {'Authorization': 'Bearer testtoken'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'profile' in data

if __name__ == "__main__":
    test_tc_883()
