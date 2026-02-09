# TC_ID 900
import requests
import json

def test_tc_900():
    url = 'https://example.com/api/health'
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'healthy'

if __name__ == "__main__":
    test_tc_900()
