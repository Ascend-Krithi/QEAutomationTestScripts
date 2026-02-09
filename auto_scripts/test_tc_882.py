# TC_ID 882
import requests
import json

def test_tc_882():
    url = 'https://example.com/api/logout'
    headers = {'Authorization': 'Bearer testtoken'}
    response = requests.post(url, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == 'Logged out successfully'

if __name__ == "__main__":
    test_tc_882()
