# TC_ID 891
import requests
import json

def test_tc_891():
    url = 'https://example.com/api/roles'
    headers = {'Authorization': 'Bearer testtoken'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data['roles'], list)

if __name__ == "__main__":
    test_tc_891()
