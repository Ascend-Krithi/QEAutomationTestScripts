import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PageClasses.LoginPage import LoginPage
from PageClasses.RuleConfigurationPage import RuleConfigurationPage
from PageClasses.ProfilePage import ProfilePage

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

class TestRuleConfiguration:
    def __init__(self, driver):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver)
        self.profile_page = ProfilePage(driver)

    def test_TC_SCRUM_158_001_create_and_verify_rule_with_date_trigger(self):
        """
        TC-SCRUM-158-001:
        - Create rule with specific date trigger
        - Set balance threshold
        - Set fixed transfer action
        - Save rule
        - Retrieve and verify rule
        """
        self.rule_page.navigate_to_rule_configuration()
        self.rule_page.click_create_new_rule()
        self.rule_page.set_rule_name("AutoTransferRule_Date")
        self.rule_page.set_trigger_type("SpecificDate")
        self.rule_page.set_trigger_date("2024-07-01")
        self.rule_page.set_condition_balance_threshold(1000)
        self.rule_page.set_action_transfer_fixed_amount(200)
        self.rule_page.save_rule()
        assert self.rule_page.verify_rule_saved("AutoTransferRule_Date")
        rule_data = self.rule_page.retrieve_rule("AutoTransferRule_Date")
        assert rule_data['trigger_type'] == "SpecificDate"
        assert rule_data['trigger_date'] == "2024-07-01"
        assert rule_data['condition_balance_threshold'] == 1000
        assert rule_data['action_transfer_amount'] == 200

    def test_TC_SCRUM_158_002_create_rule_with_balance_condition_and_verify_execution(self):
        """
        TC-SCRUM-158-002:
        - Create rule with specific date trigger
        - Set balance condition
        - Set transfer action
        - Set account balance
        - Wait for trigger
        - Verify execution and log
        """
        self.rule_page.navigate_to_rule_configuration()
        self.rule_page.click_create_new_rule()
        self.rule_page.set_rule_name("AutoTransferRule_Balance")
        self.rule_page.set_trigger_type("SpecificDate")
        self.rule_page.set_trigger_date("2024-07-02")
        self.rule_page.set_condition_balance_threshold(500)
        self.rule_page.set_action_transfer_fixed_amount(100)
        self.rule_page.save_rule()
        assert self.rule_page.verify_rule_saved("AutoTransferRule_Balance")
        # Set account balance
        self.profile_page.navigate_to_profile()
        self.profile_page.set_account_balance(600)
        # Simulate waiting for rule trigger
        self.rule_page.wait_for_rule_trigger("AutoTransferRule_Balance", timeout=120)
        # Verify execution
        assert self.rule_page.verify_rule_executed("AutoTransferRule_Balance")
        log_entry = self.rule_page.get_rule_execution_log("AutoTransferRule_Balance")
        assert log_entry is not None
        assert log_entry['status'] == 'Success'
        assert log_entry['transfer_amount'] == 100
