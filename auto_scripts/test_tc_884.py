# TC_ID 884
import requests
import json

def test_tc_884():
    url = 'https://example.com/api/notifications'
    headers = {'Authorization': 'Bearer testtoken'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data['notifications'], list)

if __name__ == "__main__":
    test_tc_884()
