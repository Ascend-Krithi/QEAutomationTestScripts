# TC_ID 887
import requests
import json

def test_tc_887():
    url = 'https://example.com/api/password/reset'
    payload = {"email": "user@example.com"}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'reset_link_sent'

if __name__ == "__main__":
    test_tc_887()
