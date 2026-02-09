import unittest
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestScripts(unittest.TestCase):
    # Existing test methods...
    # (full content from previous step)

    def test_TC_SCRUM158_07_create_rule_with_required_fields(self):
        ...
    def test_TC_SCRUM158_08_create_rule_with_large_metadata(self):
        ...
    def test_TC_SCRUM158_09_submit_schema_with_malicious_metadata(self):
        ...

    def test_TC_SCRUM158_05_validate_unsupported_trigger_schema(self):
        """Test that a schema with an unsupported trigger type is rejected and an error message is shown."""
        schema = {
            "trigger": {"type": "unsupported_type"},
            "conditions": [{"type": "amount", "operator": "<", "value": 10}],
            "actions": [{"type": "transfer", "account": "E", "amount": 10}]
        }
        page = RuleConfigurationPage(self.driver)
        error_message = page.validate_unsupported_trigger_schema(schema)
        self.assertIsNotNone(error_message, "Error message should be shown for unsupported trigger type.")
        self.assertIn("unsupported", error_message.lower(), "Error message should indicate unsupported trigger type.")

    def test_TC_SCRUM158_06_create_rule_with_max_conditions_actions(self):
        """Test creating a rule with 10 conditions and 10 actions, and verify storage and counts."""
        schema = {
            "trigger": {"type": "manual"},
            "conditions": [
                {"type": "amount", "operator": "==", "value": 1},
                {"type": "amount", "operator": "==", "value": 2},
                {"type": "amount", "operator": "==", "value": 3},
                {"type": "amount", "operator": "==", "value": 4},
                {"type": "amount", "operator": "==", "value": 5},
                {"type": "amount", "operator": "==", "value": 6},
                {"type": "amount", "operator": "==", "value": 7},
                {"type": "amount", "operator": "==", "value": 8},
                {"type": "amount", "operator": "==", "value": 9},
                {"type": "amount", "operator": "==", "value": 10}
            ],
            "actions": [
                {"type": "transfer", "account": "F1", "amount": 1},
                {"type": "transfer", "account": "F2", "amount": 2},
                {"type": "transfer", "account": "F3", "amount": 3},
                {"type": "transfer", "account": "F4", "amount": 4},
                {"type": "transfer", "account": "F5", "amount": 5},
                {"type": "transfer", "account": "F6", "amount": 6},
                {"type": "transfer", "account": "F7", "amount": 7},
                {"type": "transfer", "account": "F8", "amount": 8},
                {"type": "transfer", "account": "F9", "amount": 9},
                {"type": "transfer", "account": "F10", "amount": 10}
            ]
        }
        page = RuleConfigurationPage(self.driver)
        success = page.create_rule_with_max_conditions_actions(schema)
        self.assertTrue(success, "Rule should be created successfully with max conditions and actions.")
        stored_counts = page.verify_rule_storage_max_items(schema)
        self.assertEqual(stored_counts["conditions"], 10, "Should store 10 conditions.")
        self.assertEqual(stored_counts["actions"], 10, "Should store 10 actions.")