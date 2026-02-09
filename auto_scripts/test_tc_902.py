# TC_ID 902
import requests
import json

def test_tc_902():
    url = 'https://example.com/api/maintenance'
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['maintenance'] in [True, False]

if __name__ == "__main__":
    test_tc_902()
