# Import necessary modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

from Pages.RuleConfigurationPage import RuleConfigurationPage
from Pages.LoginPage import LoginPage

class TestLoginFunctionality:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    def test_empty_fields_validation(self):
        self.login_page.navigate_to_login()
        self.login_page.enter_email("")
        self.login_page.enter_password("")
        self.login_page.click_login()
        assert self.login_page.get_error_message() == "Mandatory fields are required"

    def test_remember_me_functionality(self):
        self.login_page.navigate_to_login()
        self.login_page.enter_email("")

    def test_TC_Login_03_empty_email(self):
        """
        TC_Login_03: Leave email empty, enter valid password, click login, verify error 'Email required'.
        """
        self.login_page.navigate_to_login()
        error_message = self.login_page.login_with_empty_email("ValidPassword123")
        assert error_message == "Email required", f"Expected 'Email required', got '{error_message}'"

    def test_TC_Login_04_empty_password(self):
        """
        TC_Login_04: Enter valid email, leave password empty, click login, verify error 'Password required'.
        """
        self.login_page.navigate_to_login()
        error_message = self.login_page.login_with_empty_password("user@example.com")
        assert error_message == "Password required", f"Expected 'Password required', got '{error_message}'"

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
        minimal_schema = self.rule_config_page.prepare_minimal_rule_schema()
        is_valid = self.rule_config_page.validate_rule_schema(minimal_schema)
        assert is_valid, "Minimal rule schema should be valid"
        response = self.rule_config_page.submit_rule_schema_api(minimal_schema, api_url, headers)
        assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}"
        response_json = response.json()
        assert "ruleId" in response_json, "ruleId should be present in response"

    def test_TC_SCRUM158_10_unsupported_trigger_schema(self):
        api_url = "http://localhost:8000/rules"
        headers = {"Content-Type": "application/json"}
        unsupported_schema = self.rule_config_page.prepare_unsupported_trigger_schema()
        is_valid = self.rule_config_page.validate_rule_schema(unsupported_schema)
        assert is_valid, "Unsupported trigger schema should pass local validation (if that's expected)"
        response = self.rule_config_page.submit_rule_schema_api(unsupported_schema, api_url, headers)
        assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"
        response_json = response.json()
        assert "error" in response_json, "Error should be present in response when trigger type is unsupported"

    def test_TC_SCRUM158_05_invalid_trigger(self):
        """
        Test case TC_SCRUM158_05: Prepare schema with invalid trigger, validate, submit, and verify error.
        """
        api_url = "http://localhost:8000/rules"
        headers = {"Content-Type": "application/json"}
        schema = self.rule_config_page.prepare_invalid_trigger_schema()
        is_valid, error_msg = self.rule_config_page.validate_rule_schema(str(schema))
        assert not is_valid, f"Schema should be invalid for unknown trigger. Error: {error_msg}"
        status_code, response = self.rule_config_page.submit_rule_schema_api(schema, api_url, headers)
        assert status_code == 400, f"API should return 400 Bad Request for invalid trigger, got {status_code}. Response: {response}"
        assert 'invalid' in str(response).lower() or 'error' in str(response).lower(), "Expected error about invalid trigger in response."

    def test_TC_SCRUM158_06_missing_condition(self):
        """
        Test case TC_SCRUM158_06: Prepare schema with missing condition parameters, validate, submit, and verify error.
        """
        api_url = "http://localhost:8000/rules"
        headers = {"Content-Type": "application/json"}
        schema = self.rule_config_page.prepare_missing_condition_schema()
        is_valid, error_msg = self.rule_config_page.validate_rule_schema(str(schema))
        assert not is_valid, f"Schema should be invalid for missing condition parameters. Error: {error_msg}"
        status_code, response = self.rule_config_page.submit_rule_schema_api(schema, api_url, headers)
        assert status_code == 400, f"API should return 400 Bad Request for incomplete condition, got {status_code}. Response: {response}"
        assert 'incomplete' in str(response).lower() or 'error' in str(response).lower(), "Expected error about incomplete condition in response."
