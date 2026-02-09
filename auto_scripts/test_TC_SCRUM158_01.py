# TC_ID: 874
# TC_Name: Test Case TC_SCRUM158_01
# Steps:
# 1. Prepare a JSON rule with all supported trigger, condition, and action types filled with valid values.
# 2. Submit the JSON rule to the system.
# 3. Retrieve the rule from backend.
# Expected Results:
# - JSON rule is valid according to schema.
# - Rule is accepted and stored.
# - Rule data matches input.

import unittest
from selenium import webdriver
import requests
import json

class TestSCRUM158_01(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://your-system-url.com"  # Replace with actual URL
        self.api_url = f"{self.base_url}/api/rules"
        self.headers = {'Content-Type': 'application/json'}
        self.valid_rule = {
            "trigger": {"type": "onTransfer", "params": {"amount": ">1000"}},
            "condition": {"type": "countryCheck", "params": {"country": "US"}},
            "action": {"type": "notify", "params": {"email": "test@example.com"}}
        }

    def test_submit_and_retrieve_valid_rule(self):
        # Step 1: Prepare JSON rule (already done in setUp)
        rule_json = json.dumps(self.valid_rule)
        # Step 2: Submit the JSON rule
        response = requests.post(self.api_url, headers=self.headers, data=rule_json)
        self.assertEqual(response.status_code, 201, "Rule should be accepted and stored.")
        rule_id = response.json().get('id')
        self.assertIsNotNone(rule_id, "Rule ID should be returned.")
        # Step 3: Retrieve the rule from backend
        get_response = requests.get(f"{self.api_url}/{rule_id}", headers=self.headers)
        self.assertEqual(get_response.status_code, 200, "Should retrieve the rule.")
        retrieved_rule = get_response.json()
        # Expected: Rule data matches input
        for key in self.valid_rule:
            self.assertEqual(retrieved_rule[key], self.valid_rule[key], f"{key} should match input.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
