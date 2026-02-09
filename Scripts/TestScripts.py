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

    def test_define_ten_percent_deposit_rule_and_transfer(self):
        """
        TC-FT-005: Define a rule for 10% of deposit action. Simulate deposit of 500 units. Validate that transfer of 50 units is executed.
        """
        rule_id = "TCFT005"
        rule_name = "TenPercentDepositRule"
        trigger = {"type": "after_deposit"}
        action = {"type": "percentage_of_deposit", "percentage": 10}
        conditions = []
        # Step 1: Define rule
        result, msg = self.rule_page.tc_define_10_percent_deposit_rule(rule_id, rule_name)
        assert result, f"Rule was not accepted: {msg}"
        # Step 2: Simulate deposit
        deposit_amount = 500
        expected_transfer = 50
        result, msg = self.rule_page.tc_simulate_deposit_and_verify_transfer(deposit_amount, expected_transfer)
        assert result, f"Transfer was not executed as expected: {msg}"

    def test_define_currency_conversion_rule_and_verify_existing(self):
        """
        TC-FT-006: Define a rule with future rule type 'currency_conversion' (currency: EUR), fixed amount 100. System should accept or gracefully reject with a clear message, without affecting existing rules. Verify existing rules continue to execute as before.
        """
        rule_id = "TCFT006"
        rule_name = "CurrencyConversionRule"
        trigger = {"type": "currency_conversion", "currency": "EUR"}
        action = {"type": "fixed_amount", "amount": 100}
        conditions = []
        # Step 1: Define future rule type
        result, msg = self.rule_page.tc_define_currency_conversion_rule(rule_id, rule_name)
        # Accept or gracefully reject
        assert result or "gracefully" in msg.lower() or "error" in msg.lower(), f"System did not handle future rule gracefully: {msg}"
        # Step 2: Verify existing rules
        result, msg = self.rule_page.tc_verify_existing_rules()
        assert result, f"Existing rules did not execute as expected: {msg}"
