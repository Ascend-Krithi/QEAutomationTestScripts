
import unittest
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestScripts(unittest.TestCase):
    # Existing test methods...

    def test_TC_SCRUM158_01_rule_creation_and_retrieval(self):
        """TC_SCRUM158_01: Prepare a valid rule schema with trigger (interval/daily), condition (amount > 100), and action (transfer to A, amount 100); submit the schema and verify rule creation and retrieval."""
        rule_page = RuleConfigurationPage(self.driver)
        rule_schema = {
            "trigger": {"type": "interval", "frequency": "daily"},
            "conditions": [{"field": "amount", "operator": ">", "value": 100}],
            "actions": [{"type": "transfer", "target": "A", "amount": 100}]
        }
        # Create rule
        rule_id = rule_page.create_rule(rule_schema)
        self.assertIsNotNone(rule_id, "Rule creation failed, rule_id is None.")
        # Submit rule
        submission_result = rule_page.submit_rule(rule_id)
        self.assertTrue(submission_result, "Rule submission failed.")
        # Retrieve and verify rule
        retrieved_rule = rule_page.get_rule(rule_id)
        self.assertIsNotNone(retrieved_rule, "Rule retrieval failed.")
        self.assertEqual(retrieved_rule["trigger"], rule_schema["trigger"], "Trigger mismatch.")
        self.assertEqual(retrieved_rule["conditions"], rule_schema["conditions"], "Condition mismatch.")
        self.assertEqual(retrieved_rule["actions"], rule_schema["actions"], "Action mismatch.")

    def test_TC_SCRUM158_02_multiple_conditions_and_actions(self):
        """TC_SCRUM158_02: Prepare a schema with trigger (manual), two conditions (amount > 500, country == US), and two actions (transfer to B, amount 500; notify with message); submit the schema and verify all conditions/actions are stored."""
        rule_page = RuleConfigurationPage(self.driver)
        rule_schema = {
            "trigger": {"type": "manual"},
            "conditions": [
                {"field": "amount", "operator": ">", "value": 500},
                {"field": "country", "operator": "==", "value": "US"}
            ],
            "actions": [
                {"type": "transfer", "target": "B", "amount": 500},
                {"type": "notify", "message": "Threshold exceeded"}
            ]
        }
        # Create rule
        rule_id = rule_page.create_rule(rule_schema)
        self.assertIsNotNone(rule_id, "Rule creation failed, rule_id is None.")
        # Submit rule
        submission_result = rule_page.submit_rule(rule_id)
        self.assertTrue(submission_result, "Rule submission failed.")
        # Retrieve and verify rule
        retrieved_rule = rule_page.get_rule(rule_id)
        self.assertIsNotNone(retrieved_rule, "Rule retrieval failed.")
        self.assertEqual(retrieved_rule["trigger"], rule_schema["trigger"], "Trigger mismatch.")
        self.assertEqual(retrieved_rule["conditions"], rule_schema["conditions"], "Conditions mismatch.")
        self.assertEqual(retrieved_rule["actions"], rule_schema["actions"], "Actions mismatch.")

# If this file is executed directly, run the tests
if __name__ == "__main__":
    unittest.main()
