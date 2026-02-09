# Existing imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from Pages.RulePage import RulePage
from Pages.DepositPage import DepositPage

class TestScripts:
    def test_rule_creation_valid(self, driver):
        rule_page = RulePage(driver)
        rule_page.navigate()
        rule_page.define_rule('Minimum Deposit', 'amount > 100')
        assert rule_page.is_rule_defined('Minimum Deposit')

    def test_deposit_simulation(self, driver):
        deposit_page = DepositPage(driver)
        deposit_page.navigate()
        deposit_page.simulate_deposit(account_id='ACC123', amount=150)
        assert deposit_page.is_transfer_executed(account_id='ACC123')

    # TC-FT-003: Define rule with multiple conditions, simulate deposit, validate transfer execution
    def test_rule_with_multiple_conditions_deposit(self, driver):
        rule_page = RulePage(driver)
        rule_page.navigate()
        # Define a rule with multiple conditions
        rule_conditions = [
            {'field': 'amount', 'operator': '>', 'value': 100},
            {'field': 'currency', 'operator': '==', 'value': 'USD'}
        ]
        rule_page.define_rule('USD High Deposit', rule_conditions)
        assert rule_page.is_rule_defined('USD High Deposit')

        deposit_page = DepositPage(driver)
        deposit_page.navigate()
        # Simulate deposit that meets all conditions
        deposit_page.simulate_deposit(account_id='ACC456', amount=200, currency='USD')
        assert deposit_page.is_transfer_executed(account_id='ACC456')

    # TC-FT-004: Error handling for missing/unsupported fields during rule definition
    def test_rule_definition_error_handling(self, driver):
        rule_page = RulePage(driver)
        rule_page.navigate()
        # Attempt to define a rule with a missing field
        invalid_conditions = [
            {'field': '', 'operator': '>', 'value': 50},
            {'field': 'unsupported_field', 'operator': '==', 'value': 'XYZ'}
        ]
        rule_page.define_rule('Invalid Rule', invalid_conditions)
        error_messages = rule_page.get_error_messages()
        assert 'Field is required' in error_messages
        assert 'unsupported_field is not supported' in error_messages
