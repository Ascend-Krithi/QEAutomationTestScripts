import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.LoginPage import LoginPage
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
        await self.login_page.fill_email('user@example.com')
        await self.login_page.fill_password('securepassword')
        await self.login_page.toggle_remember_me()
        await self.login_page.submit_login('user@example.com', 'securepassword')
        # Add assertion for successful login and remember me
        assert await self.login_page.is_logged_in()

class TestRuleConfiguration:
    def __init__(self, driver):
        self.driver = driver
        self.rule_page = RuleConfigurationPage(driver)

    def test_create_rule_with_invalid_trigger(self):
        """
        Test Case 1351: Attempt to create a rule with an invalid trigger value.
        Expectation: API returns 400 Bad Request and displays an error message.
        """
        self.rule_page.navigate_to_rule_configuration()
        self.rule_page.click_create_rule()
        # Fill in rule details with invalid trigger
        self.rule_page.enter_rule_name('Invalid Trigger Rule')
        self.rule_page.select_trigger('invalid_trigger_value')
        self.rule_page.add_condition({'type': 'valid_type', 'params': {'key': 'value'}})
        self.rule_page.add_action({'type': 'valid_action', 'params': {'key': 'value'}})
        self.rule_page.submit_rule()
        # Wait for error feedback
        error_message = self.rule_page.get_error_message()
        assert error_message is not None, 'Expected error message for invalid trigger'
        assert '400' in error_message or 'Bad Request' in error_message or 'invalid trigger' in error_message.lower()

    def test_create_rule_with_missing_condition_params(self):
        """
        Test Case 1352: Attempt to create a rule where a condition is missing required parameters.
        Expectation: API returns 400 Bad Request and displays an error message.
        """
        self.rule_page.navigate_to_rule_configuration()
        self.rule_page.click_create_rule()
        # Fill in rule details with missing condition params
        self.rule_page.enter_rule_name('Missing Condition Params Rule')
        self.rule_page.select_trigger('valid_trigger')
        self.rule_page.add_condition({'type': 'some_type', 'params': {}})  # Missing required params
        self.rule_page.add_action({'type': 'valid_action', 'params': {'key': 'value'}})
        self.rule_page.submit_rule()
        # Wait for error feedback
        error_message = self.rule_page.get_error_message()
        assert error_message is not None, 'Expected error message for missing condition parameters'
        assert '400' in error_message or 'Bad Request' in error_message or 'missing' in error_message.lower()
