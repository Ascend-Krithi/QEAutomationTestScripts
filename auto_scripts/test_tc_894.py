# TC_ID 894
import requests
import json

def test_tc_894():
    url = 'https://example.com/api/permissions'
    headers = {'Authorization': 'Bearer testtoken'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data['permissions'], list)

if __name__ == "__main__":
    test_tc_894()
