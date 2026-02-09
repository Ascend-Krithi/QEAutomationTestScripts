# TC_ID 901
import requests
import json

def test_tc_901():
    url = 'https://example.com/api/version'
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert 'version' in data

if __name__ == "__main__":
    test_tc_901()
