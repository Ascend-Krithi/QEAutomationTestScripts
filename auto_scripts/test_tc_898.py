# TC_ID 898
import requests
import json

def test_tc_898():
    url = 'https://example.com/api/audit/export'
    headers = {'Authorization': 'Bearer testtoken'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/octet-stream'

if __name__ == "__main__":
    test_tc_898()
