
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

if __name__ == '__main__':
    unittest.main()
