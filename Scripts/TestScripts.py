# Import necessary modules
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json
import time

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

# --- New Test Methods for Rule Configuration ---
class TestRuleConfiguration:
    def __init__(self, driver):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver)

    def test_specific_date_rule_transfer(self):
        """
        TC-FT-001: Define a JSON rule with 'specific_date' trigger, validate acceptance, simulate system time, and validate transfer action.
        """
        rule_id = "TCFT001"
        rule_name = "SpecificDateRule"
        date_iso = "2024-07-01T10:00:00Z"
        amount = 100
        # Step 1: Set up rule configuration
        self.rule_page.set_rule_id(rule_id)
        self.rule_page.set_rule_name(rule_name)
        self.rule_page.select_trigger_type('specific_date')
        self.rule_page.set_trigger_date(date_iso)
        self.rule_page.select_action_type('fixed_amount')
        self.rule_page.set_transfer_amount(amount)
        self.rule_page.save_rule()
        # Step 2: Validate rule acceptance
        success_message = self.rule_page.get_success_message()
        assert success_message is not None and 'accepted' in success_message.lower(), "Rule was not accepted by the system"
        # Step 3: Simulate system time
        self.rule_page.simulate_system_time(date_iso)
        # Step 4: Validate transfer action
        transfer_result = self.rule_page.validate_transfer_action()
        assert transfer_result is not None, "Transfer action was not executed"

    def test_recurring_weekly_rule_transfer(self):
        """
        TC-FT-002: Define a JSON rule with 'recurring' weekly trigger, validate acceptance, simulate time, and validate transfer action.
        """
        rule_id = "TCFT002"
        rule_name = "RecurringWeeklyRule"
        interval = "weekly"
        percentage = 10
        # Step 1: Set up rule configuration
        self.rule_page.set_rule_id(rule_id)
        self.rule_page.set_rule_name(rule_name)
        self.rule_page.select_trigger_type('recurring')
        self.rule_page.set_recurring_interval(interval)
        self.rule_page.select_action_type('percentage_of_deposit')
        self.rule_page.set_percentage(percentage)
        self.rule_page.save_rule()
        # Step 2: Validate rule acceptance
        success_message = self.rule_page.get_success_message()
        assert success_message is not None and 'accepted' in success_message.lower(), "Rule was not accepted by the system"
        # Step 3: Simulate several weeks
        for week in range(3):
            future_date = f"2024-07-0{week+2}T10:00:00Z"
            self.rule_page.simulate_system_time(future_date)
            transfer_result = self.rule_page.validate_transfer_action()
            assert transfer_result is not None, f"Transfer action was not executed for week {week+1}"

    def test_percentage_of_deposit_rule(self):
        """
        TC-FT-005: Define a rule for 10% of deposit, simulate deposit of 500 units, verify transfer of 50 units.
        """
        rule_id = "TCFT005"
        rule_name = "TenPercentDepositRule"
        trigger_type = "after_deposit"
        action_type = "percentage_of_deposit"
        percentage = 10
        deposit_amount = 500
        expected_transfer = 50
        # Step 1: Define the rule
        self.rule_page.define_rule(rule_id, rule_name, trigger_type, action_type, percentage=percentage)
        # Step 2: Validate rule acceptance
        success_message = self.rule_page.validate_success_message()
        assert success_message is not None and 'accepted' in success_message.lower(), "Rule was not accepted"
        # Step 3: Simulate deposit
        self.rule_page.simulate_deposit(deposit_amount)
        # Step 4: Verify transfer
        self.rule_page.verify_transfer(expected_transfer)

    def test_currency_conversion_rule_and_existing_rule(self):
        """
        TC-FT-006: Define a rule with a new, future rule type ('currency_conversion'), verify acceptance or graceful rejection, and verify existing rules continue to execute as before.
        """
        rule_id = "TCFT006"
        rule_name = "CurrencyConversionRule"
        trigger_type = "currency_conversion"
        action_type = "fixed_amount"
        currency = "EUR"
        amount = 100
        # Step 1: Define the future rule type
        self.rule_page.define_rule(rule_id, rule_name, trigger_type, action_type, currency=currency, amount=amount)
        # Step 2: Validate acceptance or graceful rejection
        try:
            success_message = self.rule_page.validate_success_message()
            assert success_message is not None and ('accepted' in success_message.lower() or 'rejected' in success_message.lower()), "System did not provide clear acceptance/rejection message"
        except Exception:
            error_message = self.rule_page.validate_error_message()
            assert error_message is not None and len(error_message) > 0, "System did not provide error feedback for future rule type"
        # Step 3: Verify existing rules continue to execute
        # Re-use TC-FT-005 logic
        rule_id2 = "TCFT005"
        rule_name2 = "TenPercentDepositRule"
        trigger_type2 = "after_deposit"
        action_type2 = "percentage_of_deposit"
        percentage2 = 10
        deposit_amount2 = 500
        expected_transfer2 = 50
        self.rule_page.define_rule(rule_id2, rule_name2, trigger_type2, action_type2, percentage=percentage2)
        self.rule_page.simulate_deposit(deposit_amount2)
        self.rule_page.verify_transfer(expected_transfer2)
