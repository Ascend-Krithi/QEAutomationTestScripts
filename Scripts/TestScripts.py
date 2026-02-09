# Existing imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Pages.RuleConfigurationPage import RuleConfigurationPage

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

    def test_define_specific_date_rule(self):
        """
        TC-FT-001: Define JSON rule with trigger type 'specific_date', execute fixed amount transfer.
        """
        rule_id = 'TC-FT-001-Rule'
        rule_name = 'Specific Date Transfer Rule'
        trigger_type = 'specific_date'
        date_str = '2024-07-01'
        action_type = 'fixed_amount'
        amount = 100
        destination_account = '123456789'
        json_rule = json.dumps({
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"},
            "action": {"type": "fixed_amount", "amount": 100},
            "conditions": []
        })

        self.page.enter_rule_id(rule_id)
        self.page.enter_rule_name(rule_name)
        self.page.select_trigger_type(trigger_type)
        self.page.set_specific_date(date_str)
        self.page.select_action_type(action_type)
        self.page.set_transfer_amount(amount)
        self.page.set_destination_account(destination_account)
        self.page.enter_json_schema(json_rule)
        self.page.validate_schema()
        assert self.page.is_success_message_displayed(), "Rule was not accepted by the system."
        self.page.save_rule()
        # Simulate system time reaching the trigger date (pseudo, as actual time manipulation is not possible in Selenium)
        # Verify transfer action executed (would require backend validation or UI confirmation)

    def test_define_recurring_rule(self):
        """
        TC-FT-002: Define JSON rule with trigger type 'recurring', execute percentage transfer.
        """
        rule_id = 'TC-FT-002-Rule'
        rule_name = 'Recurring Transfer Rule'
        trigger_type = 'recurring'
        interval = 'weekly'
        action_type = 'percentage_of_deposit'
        percentage = 10
        destination_account = '987654321'
        json_rule = json.dumps({
            "trigger": {"type": "recurring", "interval": "weekly"},
            "action": {"type": "percentage_of_deposit", "percentage": 10},
            "conditions": []
        })

        self.page.enter_rule_id(rule_id)
        self.page.enter_rule_name(rule_name)
        self.page.select_trigger_type(trigger_type)
        self.page.set_recurring_interval(interval)
        self.page.select_action_type(action_type)
        self.page.set_percentage(percentage)
        self.page.set_destination_account(destination_account)
        self.page.enter_json_schema(json_rule)
        self.page.validate_schema()
        assert self.page.is_success_message_displayed(), "Rule was not accepted by the system."
        self.page.save_rule()
        # Simulate passing of several weeks (pseudo, as actual time manipulation is not possible in Selenium)
        # Verify transfer action executed at each interval (would require backend validation or UI confirmation)
