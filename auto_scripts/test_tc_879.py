# TC_ID 879
import requests
import json

def test_tc_879():
    url = 'https://example.com/api/delete'
    payload = {"item_id": 54321}
    headers = {'Content-Type': 'application/json'}
    response = requests.delete(url, data=json.dumps(payload), headers=headers)
    assert response.status_code == 204

if __name__ == "__main__":
    test_tc_879()
