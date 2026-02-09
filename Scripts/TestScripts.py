# Existing imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Pages.RuleConfigurationPage import RuleConfigurationPage
from Pages.DepositSimulationPage import DepositSimulationPage

class TestLoginFunctionality:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('')

# New test methods for Rule Configuration
import datetime
import json

class TestRuleConfiguration:
    def __init__(self, driver):
        self.page = RuleConfigurationPage(driver)
        self.deposit_page = DepositSimulationPage(driver)

    def test_define_specific_date_rule(self):
        """
        TC-FT-001: Define JSON rule with trigger type 'specific_date', execute fixed amount transfer.
        """
        # ...existing code...

    def test_define_recurring_rule(self):
        """
        TC-FT-002: Define JSON rule with trigger type 'recurring', execute percentage transfer.
        """
        # ...existing code...

    def test_define_multi_condition_rule_and_deposit_simulation(self):
        """
        TC-FT-003: Define a rule with multiple conditions (balance >= 1000, source = 'salary'), simulate deposit from 'salary' with balance 900 (expect no transfer), simulate deposit from 'salary' with balance 1200 (expect transfer).
        """
        # ...existing code...

    def test_error_handling_missing_trigger_and_unsupported_action(self):
        """
        TC-FT-004: Submit rule with missing trigger type (expect error), submit rule with unsupported action type (expect error).
        """
        # ...existing code...

    def test_define_percentage_of_deposit_rule_and_simulate_deposit(self):
        """
        TC-FT-005: Step 1 - Define a rule for 10% of deposit action.
                  Step 2 - Simulate deposit of 500 units.
                  Expected: Rule is accepted, transfer of 50 units executed.
        """
        # Step 1: Define rule for 10% of deposit
        result = self.page.define_percentage_of_deposit_rule(10)
        assert 'success' in result.lower(), f"Rule creation failed: {result}"
        # Step 2: Simulate deposit of 500 units
        deposit_result = self.deposit_page.simulate_deposit(500)
        assert '50' in deposit_result, f"Expected transfer of 50 units, got: {deposit_result}"

    def test_currency_conversion_rule_and_verify_existing_rule(self):
        """
        TC-FT-006: Step 1 - Define a rule with type 'currency_conversion' (EUR, 100).
                  Step 2 - Verify existing rules continue to execute as before.
                  Expected: System accepts or gracefully rejects with a clear message, existing rules are not affected.
        """
        # Step 1: Define currency conversion rule
        result = self.page.define_currency_conversion_rule('EUR', 100)
        assert 'success' in result.lower() or 'error' in result.lower(), f"Unexpected response: {result}"
        # Step 2: Verify existing rule execution
        rule_verified = self.page.verify_existing_rule_execution('percentage_of_deposit')
        assert rule_verified, "Existing rule 'percentage_of_deposit' not found or not functioning as expected."
