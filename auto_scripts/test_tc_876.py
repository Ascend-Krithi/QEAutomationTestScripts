# TC_ID 876
import requests
import json

def test_tc_876():
    url = 'https://example.com/api/endpoint2'
    payload = {"user": "testuser", "action": "create"}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data['status'] == 'created'

if __name__ == "__main__":
    test_tc_876()
