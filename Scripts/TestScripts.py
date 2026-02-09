# Import necessary modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

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

class TestRuleConfiguration:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.rule_config_page = RuleConfigurationPage(self.driver)
        self.rule_config_page.wait_for_rule_configuration_page()

    def teardown_method(self):
        self.driver.quit()

    # ... (existing test methods)

    def test_TC_SCRUM158_09_minimal_rule_schema(self):
        api_url = "http://localhost:8000/rules"
        headers = {"Content-Type": "application/json"}
        # Prepare minimal valid rule schema
        minimal_schema = self.rule_config_page.prepare_minimal_rule_schema()
        # Validate rule schema
        is_valid = self.rule_config_page.validate_rule_schema(minimal_schema)
        assert is_valid, "Minimal rule schema should be valid"
        # Submit rule schema
        response = self.rule_config_page.submit_rule_schema_api(minimal_schema, api_url, headers)
        assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}"
        response_json = response.json()
        assert "ruleId" in response_json, "ruleId should be present in response"

    def test_TC_SCRUM158_10_unsupported_trigger_schema(self):
        api_url = "http://localhost:8000/rules"
        headers = {"Content-Type": "application/json"}
        # Prepare schema with unsupported trigger type
        unsupported_schema = self.rule_config_page.prepare_unsupported_trigger_schema()
        # Validate rule schema
        is_valid = self.rule_config_page.validate_rule_schema(unsupported_schema)
        assert is_valid, "Unsupported trigger schema should pass local validation (if that's expected)"
        # Submit rule schema
        response = self.rule_config_page.submit_rule_schema_api(unsupported_schema, api_url, headers)
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
        response_json = response.json()
        assert "error" in response_json, "Error should be present in response when trigger type is unsupported"
