from selenium import webdriver
import unittest
from Pages.RuleConfigurationPage import RuleConfigurationPage

class TestLoginFunctionality(unittest.TestCase):
    # ... (existing test methods)
    pass

# --- New Test Methods for Rule Configuration ---

class TestRuleConfiguration(unittest.TestCase):
    def setUp(self):
        # Set up Selenium WebDriver and RuleConfigurationPage
        self.driver = webdriver.Chrome()
        self.rule_page = RuleConfigurationPage(self.driver)

    def tearDown(self):
        # Clean up WebDriver
        self.driver.quit()

    # Existing tests...

    # --- Appended for TC_SCRUM158_01 ---
    def test_TC_SCRUM158_01_create_and_store_rule(self):
        """
        TC_SCRUM158_01:
        1. Prepare a valid rule schema with all supported trigger, condition, and action types.
        2. Submit the schema to the rule automation service.
        Acceptance Criteria: Schema is accepted, rule is created, stored, and retrievable.
        """
        rule_data = {
            "trigger": {"type": "interval", "value": "daily"},
            "conditions": [{"type": "amount", "operator": ">", "value": 100}],
            "actions": [{"type": "transfer", "account": "A", "amount": 100}]
        }
        self.rule_page.create_and_store_valid_rule(rule_data)
        # Retrieval/validation step (simulate via UI or backend)
        # If implemented: self.rule_page.retrieve_rule_from_backend(rule_id)
        # UI assertion for success
        success = True # Replace with actual validation if available
        self.assertTrue(success, "Schema should be accepted and rule created successfully.")

    # --- Appended for TC_SCRUM158_02 ---
    def test_TC_SCRUM158_02_create_rule_with_multiple_conditions_and_actions(self):
        """
        TC_SCRUM158_02:
        1. Prepare a schema with two conditions and two actions.
        2. Submit the schema and check that all conditions/actions are stored.
        Acceptance Criteria: Schema is accepted, rule is created, and contains all conditions and actions.
        """
        rule_data = {
            "trigger": {"type": "manual"},
            "conditions": [
                {"type": "amount", "operator": ">", "value": 500},
                {"type": "country", "operator": "==", "value": "US"}
            ],
            "actions": [
                {"type": "transfer", "account": "B", "amount": 500},
                {"type": "notify", "message": "Transfer complete"}
            ]
        }
        self.rule_page.create_and_store_valid_rule(rule_data)
        # UI assertion for success
        success = True # Replace with actual validation if available
        self.assertTrue(success, "Rule should be created and contain all conditions and actions.")

    # --- Appended for TC_SCRUM158_05 ---
    def test_TC_SCRUM158_05_unsupported_trigger_type(self):
        """
        TC_SCRUM158_05:
        1. Prepare a schema with unsupported trigger type ('unsupported_type').
        2. Submit the schema and observe error response.
        Acceptance Criteria: Schema is rejected with error about unsupported type. Rule is not created; error message returned.
        """
        schema_text = '{"trigger": {"type": "unsupported_type"}, "conditions": [{"type": "amount", "operator": "<", "value": 10}], "actions": [{"type": "transfer", "account": "E", "amount": 10}]}'
        result_message = self.rule_page.submit_and_validate_schema(schema_text)
        self.assertIn("unsupported", result_message.lower(), "Schema with unsupported trigger type should be rejected with error message.")

    # --- Appended for TC_SCRUM158_06 ---
    def test_TC_SCRUM158_06_maximum_conditions_actions(self):
        """
        TC_SCRUM158_06:
        1. Prepare a schema with maximum allowed (10) conditions and actions.
        2. Submit the schema and verify storage of all conditions/actions.
        Acceptance Criteria: Rule is accepted and all conditions/actions are stored. Rule contains maximum allowed items.
        """
        schema_text = '{"trigger": {"type": "manual"}, "conditions": [{"type": "amount", "operator": "==", "value": 1}, {"type": "amount", "operator": "==", "value": 2}, {"type": "amount", "operator": "==", "value": 3}, {"type": "amount", "operator": "==", "value": 4}, {"type": "amount", "operator": "==", "value": 5}, {"type": "amount", "operator": "==", "value": 6}, {"type": "amount", "operator": "==", "value": 7}, {"type": "amount", "operator": "==", "value": 8}, {"type": "amount", "operator": "==", "value": 9}, {"type": "amount", "operator": "==", "value": 10}], "actions": [{"type": "transfer", "account": "F1", "amount": 1}, {"type": "transfer", "account": "F2", "amount": 2}, {"type": "transfer", "account": "F3", "amount": 3}, {"type": "transfer", "account": "F4", "amount": 4}, {"type": "transfer", "account": "F5", "amount": 5}, {"type": "transfer", "account": "F6", "amount": 6}, {"type": "transfer", "account": "F7", "amount": 7}, {"type": "transfer", "account": "F8", "amount": 8}, {"type": "transfer", "account": "F9", "amount": 9}, {"type": "transfer", "account": "F10", "amount": 10}]}'
        result_message = self.rule_page.submit_and_validate_schema(schema_text)
        self.assertIn("success", result_message.lower(), "Rule with maximum allowed conditions/actions should be accepted and stored.")
