# TC_ID 881
import requests
import json

def test_tc_881():
    url = 'https://example.com/api/search'
    payload = {"query": "test"}
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, params=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data['results']) > 0

if __name__ == "__main__":
    test_tc_881()
