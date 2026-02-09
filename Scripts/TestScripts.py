# Existing imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from Pages.RuleConfigurationPage import RuleConfigurationPage

# Existing TestRuleConfiguration class definition
class TestRuleConfiguration:
    # ... [existing methods here] ...

    def test_TC_FT_009_create_and_validate_specific_date_rule(self, driver):
        """
        TC-FT-009: Create and store a valid rule with trigger type 'specific_date', action type 'fixed_amount', amount 100, and empty conditions.
        Retrieve the rule and validate it matches the input.
        """
        rule_page = RuleConfigurationPage(driver)
        rule_data = {
            'trigger_type': 'specific_date',
            'action_type': 'fixed_amount',
            'amount': 100,
            'conditions': []
        }
        # Step 1: Create rule
        rule_page.open()
        rule_page.create_rule(
            trigger_type=rule_data['trigger_type'],
            action_type=rule_data['action_type'],
            amount=rule_data['amount'],
            conditions=rule_data['conditions']
        )
        rule_page.save_rule()

        # Step 2: Retrieve and validate rule
        saved_rule = rule_page.get_rule_by_trigger('specific_date')
        assert saved_rule['trigger_type'] == rule_data['trigger_type'], 'Trigger type does not match.'
        assert saved_rule['action_type'] == rule_data['action_type'], 'Action type does not match.'
        assert saved_rule['amount'] == rule_data['amount'], 'Amount does not match.'
        assert saved_rule['conditions'] == rule_data['conditions'], 'Conditions should be empty.'

    def test_TC_FT_010_unconditional_transfer_on_deposit(self, driver):
        """
        TC-FT-010: Define a rule with empty conditions and trigger it with a deposit of 1000.
        Validate that the transfer is executed unconditionally.
        """
        rule_page = RuleConfigurationPage(driver)
        rule_data = {
            'trigger_type': 'deposit',
            'action_type': 'transfer',
            'amount': 1000,
            'conditions': []
        }
        # Step 1: Create rule with empty conditions
        rule_page.open()
        rule_page.create_rule(
            trigger_type=rule_data['trigger_type'],
            action_type=rule_data['action_type'],
            amount=rule_data['amount'],
            conditions=rule_data['conditions']
        )
        rule_page.save_rule()

        # Step 2: Trigger deposit and validate transfer
        rule_page.trigger_deposit(amount=rule_data['amount'])
        transfer_executed = rule_page.verify_transfer_executed(amount=rule_data['amount'])
        assert transfer_executed, f"Transfer of {rule_data['amount']} should be executed unconditionally."
