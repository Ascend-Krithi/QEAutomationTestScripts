# TC_874_Test_Case_TC_SCRUM158_01.py
import requests
import json

def test_create_valid_rule():
    url = 'http://localhost:8000/rules'  # Update with actual API endpoint
    headers = {'Content-Type': 'application/json'}
    payload = {
        "ruleId": "R001",
        "trigger": "onBalance",
        "conditions": [
            {"type": "amount", "operator": ">", "value": 1000}
        ],
        "actions": [
            {"type": "transfer", "destination": "AccountB"}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    resp_json = response.json()
    assert resp_json.get('ruleId') == 'R001', f"Expected ruleId R001, got {resp_json.get('ruleId')}"
    print('Test passed: Valid rule creation')

if __name__ == "__main__":
    test_create_valid_rule()
