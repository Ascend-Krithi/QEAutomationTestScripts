from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.RuleConfigurationPage import RuleConfigurationPage
from Pages.ProfilePage import ProfilePage
from Pages.SettingsPage import SettingsPage
import datetime

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

    def test_create_rule_with_specific_date_trigger_and_balance_condition(self):
        # Step 2: Navigate to rule creation interface
        self.rule_page.navigate_to_rule_creation()
        # Step 3: Define specific date trigger for 2024-12-31 at 10:00 AM
        self.rule_page.define_specific_date_trigger('2024-12-31')
        # Step 4: Add balance threshold condition: balance > $500
        self.rule_page.add_balance_threshold_condition('greater_than', 500)
        # Step 5: Add fixed amount transfer action: transfer $100 to savings account
        self.rule_page.add_fixed_transfer_action(100, 'SAV-001')
        # Step 6: Save rule
        self.rule_page.save_rule()
        # Step 7: Retrieve saved rule and validate
        self.rule_page.retrieve_saved_rule('RULE-XXXX')
        # Step 8: Validate schema
        self.rule_page.validate_schema()

    def test_create_rule_with_dynamic_date_and_balance_action(self):
        # Step 2: Create rule with specific date trigger (current date + 1 minute), balance > $300, transfer $50
        future_date = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime('%Y-%m-%d')
        self.rule_page.navigate_to_rule_creation()
        self.rule_page.define_specific_date_trigger(future_date)
        self.rule_page.add_balance_threshold_condition('greater_than', 300)
        self.rule_page.add_fixed_transfer_action(50, 'SAV-001')
        self.rule_page.save_rule()
        # Step 3: Set account balance to $400 (Assume method exists or is mocked)
        # Step 4: Wait for trigger time and verify rule evaluation (Assume wait logic, not implemented)
        # Step 5: Verify transfer action execution (Assume check, not implemented)
        # Step 6: Check rule execution log (Assume check, not implemented)
        self.rule_page.retrieve_saved_rule('RULE-XXXX')
        self.rule_page.validate_schema()

    def test_TC_SCRUM_158_001_create_rule_and_validate(self):
        """
        TC-SCRUM-158-001: Rule creation with specific date trigger, balance threshold condition, fixed transfer action, saving, retrieval, and validation.
        """
        # Step 1: Navigate to Profile and Settings (optional, for context)
        profile_page = ProfilePage(self.driver)
        settings_page = SettingsPage(self.driver)
        profile_page.click_profile()
        settings_page.open_settings()
        # Step 2: Navigate to rule creation interface
        self.rule_page.navigate_to_rule_creation()
        # Step 3: Define specific date trigger for 2024-12-31 at 10:00 AM
        self.rule_page.define_specific_date_trigger('2024-12-31 10:00')
        # Step 4: Add balance threshold condition: balance > $500
        self.rule_page.add_balance_threshold_condition('greater_than', 500)
        # Step 5: Add fixed amount transfer action: transfer $100 to savings account
        self.rule_page.add_fixed_transfer_action(100, 'SAV-001')
        # Step 6: Save rule
        rule_id = self.rule_page.save_rule()
        # Step 7: Retrieve saved rule and validate
        self.rule_page.retrieve_saved_rule(rule_id)
        # Step 8: Validate schema
        self.rule_page.validate_schema(rule_id)
        # Step 9: Assert rule exists and is correct
        assert self.rule_page.is_rule_present(rule_id)
        assert self.rule_page.is_rule_schema_valid(rule_id)

    def test_TC_SCRUM_158_002_dynamic_trigger_balance_transfer_and_log(self):
        """
        TC-SCRUM-158-002: Rule creation with dynamic trigger date, balance condition, transfer action, account balance update, waiting for trigger, verifying transfer, and checking execution log.
        """
        # Step 1: Navigate to Profile and Settings (optional)
        profile_page = ProfilePage(self.driver)
        settings_page = SettingsPage(self.driver)
        profile_page.click_profile()
        settings_page.open_settings()
        # Step 2: Create rule with dynamic date trigger (current date + 1 minute), balance > $300, transfer $50
        future_datetime = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M')
        self.rule_page.navigate_to_rule_creation()
        self.rule_page.define_specific_date_trigger(future_datetime)
        self.rule_page.add_balance_threshold_condition('greater_than', 300)
        self.rule_page.add_fixed_transfer_action(50, 'SAV-001')
        rule_id = self.rule_page.save_rule()
        # Step 3: Set account balance to $400
        self.rule_page.set_account_balance(400)
        # Step 4: Wait for trigger time and verify rule evaluation
        self.rule_page.wait_for_rule_trigger(rule_id)
        # Step 5: Verify transfer action execution
        assert self.rule_page.is_transfer_executed(rule_id, 50, 'SAV-001')
        # Step 6: Check rule execution log
        log = self.rule_page.get_rule_execution_log(rule_id)
        assert 'Transfer executed' in log
        # Step 7: Validate schema
        self.rule_page.validate_schema(rule_id)
        assert self.rule_page.is_rule_schema_valid(rule_id)
