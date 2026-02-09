# TC_ID 875
import requests
import json

def test_tc_875():
    url = 'https://example.com/api/endpoint'
    payload = {"key1": "value1", "key2": "value2"}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['result'] == 'expected_value'

if __name__ == "__main__":
    test_tc_875()
