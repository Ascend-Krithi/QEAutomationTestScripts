# TC_ID: 875
# TC_Name: Test Case TC_SCRUM158_02
# Steps:
# 1. Prepare a JSON rule missing the 'trigger' field.
# 2. Submit the incomplete rule.
# Expected Results:
# - Schema validation fails with missing field error.
# - Rule is rejected with appropriate error message.

import unittest
import requests
import json

class TestSCRUM158_02(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://your-system-url.com"  # Replace with actual URL
        self.api_url = f"{self.base_url}/api/rules"
        self.headers = {'Content-Type': 'application/json'}
        self.invalid_rule = {
            # 'trigger' field is missing
            "condition": {"type": "countryCheck", "params": {"country": "US"}},
            "action": {"type": "notify", "params": {"email": "test@example.com"}}
        }

    def test_submit_incomplete_rule(self):
        rule_json = json.dumps(self.invalid_rule)
        response = requests.post(self.api_url, headers=self.headers, data=rule_json)
        self.assertEqual(response.status_code, 400, "Schema validation should fail.")
        error_msg = response.json().get('error', '')
        self.assertIn('trigger', error_msg.lower(), "Error message should mention missing 'trigger' field.")

if __name__ == "__main__":
    unittest.main()
