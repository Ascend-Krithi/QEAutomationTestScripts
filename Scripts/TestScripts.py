
import unittest
from RuleConfigurationPage import RuleConfigurationPage

class TestRuleConfiguration(unittest.TestCase):

    # Existing test methods...

    def test_define_rule_with_multiple_conditions_TC_FT_003(self):
        """TC-FT-003: Define rule with multiple conditions (balance >= 1000, source = 'salary').
        - Simulate deposit from 'salary' when balance is 900 (expect transfer NOT executed).
        - Simulate deposit from 'salary' when balance is 1200 (expect transfer executed).
        """
        rule_page = RuleConfigurationPage()
        rule = {
            'trigger': 'deposit',
            'conditions': [
                {'field': 'balance', 'operator': '>=', 'value': 1000},
                {'field': 'source', 'operator': '==', 'value': 'salary'}
            ],
            'action': 'transfer'
        }
        rule_page.define_rule(rule)
        # Simulate deposit from 'salary' when balance is 900
        result_900 = rule_page.simulate_deposit(balance=900, source='salary')
        self.assertFalse(result_900['transfer_executed'], "Transfer should NOT be executed when balance is 900.")
        # Simulate deposit from 'salary' when balance is 1200
        result_1200 = rule_page.simulate_deposit(balance=1200, source='salary')
        self.assertTrue(result_1200['transfer_executed'], "Transfer should be executed when balance is 1200.")

    def test_submit_rule_with_missing_trigger_TC_FT_004(self):
        """TC-FT-004: Submit rule with missing trigger (expect error for missing required field)."""
        rule_page = RuleConfigurationPage()
        rule_missing_trigger = {
            # 'trigger' is missing
            'conditions': [
                {'field': 'balance', 'operator': '>=', 'value': 1000}
            ],
            'action': 'transfer'
        }
        with self.assertRaises(ValueError) as context:
            rule_page.define_rule(rule_missing_trigger)
        self.assertIn('missing required field', str(context.exception).lower())

    def test_submit_rule_with_unsupported_action_TC_FT_004(self):
        """TC-FT-004: Submit rule with unsupported action (expect error for unsupported action type)."""
        rule_page = RuleConfigurationPage()
        rule_unsupported_action = {
            'trigger': 'deposit',
            'conditions': [
                {'field': 'balance', 'operator': '>=', 'value': 1000}
            ],
            'action': 'unsupported_action_type'
        }
        with self.assertRaises(ValueError) as context:
            rule_page.define_rule(rule_unsupported_action)
        self.assertIn('unsupported action', str(context.exception).lower())

    def test_load_10000_rules_and_verify_performance_TC_FT_007(self):
        """TC-FT-007: Load 10,000 valid rules and verify performance. Trigger evaluation for all rules simultaneously."""
        rule_page = RuleConfigurationPage(self.driver)
        # Generate 10,000 valid rules
        rules = [{'id': f'rule_{i}', 'name': f'Rule {i}'} for i in range(1, 10001)]
        load_time = rule_page.load_rules_and_verify_performance(rules)
        self.assertLess(load_time, 60, "System should load 10,000 rules within 60 seconds.")
        rule_page.trigger_evaluation_for_all_rules()
        # Additional performance assertions can be added as needed

    def test_submit_rule_with_sql_injection_TC_FT_008(self):
        """TC-FT-008: Submit a rule with SQL injection in a field value and verify system rejection."""
        rule_page = RuleConfigurationPage(self.driver)
        sql_payload = "1000; DROP TABLE users;--"
        error_message = rule_page.submit_rule_with_sql_injection(sql_payload)
        self.assertIsNotNone(error_message, "System should reject rule with SQL injection.")
        self.assertIn("error", error_message.lower(), "Error message should indicate rejection.")

    # --- TC-FT-009 ---
    def test_create_and_store_rule_specific_date_TC_FT_009(self):
        """
        TC-FT-009: Create and store a valid rule with specific_date trigger and fixed_amount action, empty conditions.
        Then retrieve the rule from backend and verify it matches the original input.
        """
        driver = self.driver if hasattr(self, 'driver') else None
        rule_page = RuleConfigurationPage(driver)
        rule_data = {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        creation_result = rule_page.create_and_store_rule(rule_data)
        self.assertTrue(creation_result, "Rule should be created and stored successfully.")
        retrieval_result = rule_page.retrieve_rule(rule_data)
        self.assertTrue(retrieval_result, "Retrieved rule should match the original input.")

    # --- TC-FT-010 ---
    def test_define_and_trigger_rule_after_deposit_TC_FT_010(self):
        """
        TC-FT-010: Define a rule with after_deposit trigger, fixed_amount action, empty conditions.
        Then trigger the rule after deposit of 1000 and verify transfer execution.
        """
        driver = self.driver if hasattr(self, 'driver') else None
        rule_page = RuleConfigurationPage(driver)
        rule_data = {
            "trigger": {"type": "after_deposit"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        }
        definition_result = rule_page.define_rule_empty_conditions(rule_data)
        self.assertTrue(definition_result, "Rule with empty conditions should be accepted.")
        transfer_result = rule_page.trigger_rule_after_deposit(1000)
        self.assertTrue(transfer_result, "Transfer should be executed without checking any conditions.")

if __name__ == '__main__':
    unittest.main()
