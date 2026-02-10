import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from LoginPage import LoginPage
from RuleConfigurationPage import RuleConfigurationPage

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

    def wait_for_element(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            pytest.fail(f"Element {locator} not found after {timeout} seconds.")

    def test_TC_SCRUM_158_001_create_and_validate_rule(self):
        """
        TC-SCRUM-158-001: Create a rule, add trigger, condition, action, save, retrieve, and validate.
        """
        try:
            self.rule_page.navigate_to_rule_configuration()
            self.wait_for_element((By.ID, "create-rule-btn"))
            self.rule_page.click_create_rule()

            self.wait_for_element((By.ID, "rule-name-input"))
            self.rule_page.enter_rule_name("AutoTestRule001")
            self.rule_page.enter_rule_description("Automated test rule creation.")

            self.rule_page.add_trigger(trigger_type="OnEvent", trigger_value="UserLogin")
            self.rule_page.add_condition(condition_type="UserType", condition_value="Admin")
            self.rule_page.add_action(action_type="SendNotification", action_value="Email")

            self.rule_page.save_rule()
            self.wait_for_element((By.XPATH, "//div[contains(text(), 'Rule saved successfully')]") )

            self.rule_page.search_rule("AutoTestRule001")
            self.wait_for_element((By.XPATH, "//td[contains(text(), 'AutoTestRule001')]") )
            rule_details = self.rule_page.get_rule_details("AutoTestRule001")

            assert rule_details['name'] == "AutoTestRule001"
            assert rule_details['trigger'] == "OnEvent:UserLogin"
            assert rule_details['condition'] == "UserType:Admin"
            assert rule_details['action'] == "SendNotification:Email"
        except Exception as e:
            pytest.fail(f"TC-SCRUM-158-001 failed: {str(e)}")

    def test_TC_SCRUM_158_002_rule_duplicate_validation(self):
        """
        TC-SCRUM-158-002: Attempt to create a rule with a duplicate name and validate error handling.
        """
        try:
            self.rule_page.navigate_to_rule_configuration()
            self.wait_for_element((By.ID, "create-rule-btn"))
            self.rule_page.click_create_rule()

            self.wait_for_element((By.ID, "rule-name-input"))
            self.rule_page.enter_rule_name("AutoTestRule001")  # Duplicate name
            self.rule_page.enter_rule_description("Duplicate rule test.")

            self.rule_page.add_trigger(trigger_type="OnEvent", trigger_value="UserLogin")
            self.rule_page.add_condition(condition_type="UserType", condition_value="Admin")
            self.rule_page.add_action(action_type="SendNotification", action_value="Email")

            self.rule_page.save_rule()
            error_message = self.rule_page.get_error_message()
            assert error_message == "A rule with this name already exists"
        except Exception as e:
            pytest.fail(f"TC-SCRUM-158-002 failed: {str(e)}")
