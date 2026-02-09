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

    def test_TC_SCRUM158_05_invalid_trigger_schema(self):
        """
        TC_SCRUM158_05: Prepare a rule schema with an invalid trigger value (e.g., 'unknown_trigger'), validate (should fail), submit (API should return 400 Bad Request with error about invalid value)
        """
        api_url = "http://localhost:8000/rules"
        headers = {"Content-Type": "application/json"}
        # Prepare invalid trigger schema
        invalid_trigger_schema = self.rule_config_page.prepare_rule_schema_with_trigger("unknown_trigger")
        is_valid = self.rule_config_page.validate_rule_schema(invalid_trigger_schema)
        assert not is_valid, "Schema with invalid trigger should fail validation"
        response = self.rule_config_page.submit_rule_schema_api(invalid_trigger_schema, api_url, headers)
        assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"
        response_json = response.json()
        assert "error" in response_json, "Error should be present in response when trigger value is invalid"
        assert "invalid trigger" in response_json["error"].lower(), f"Expected error about invalid trigger, got '{response_json['error']}'"

    def test_TC_SCRUM158_06_missing_condition_parameter_schema(self):
        """
        TC_SCRUM158_06: Prepare a rule schema with a condition missing required parameters, validate (should fail), submit (API should return 400 Bad Request with error about incomplete condition)
        """
        api_url = "http://localhost:8000/rules"
        headers = {"Content-Type": "application/json"}
        # Prepare condition missing required parameter
        incomplete_condition_schema = self.rule_config_page.prepare_rule_schema_with_incomplete_condition()
        is_valid = self.rule_config_page.validate_rule_schema(incomplete_condition_schema)
        assert not is_valid, "Schema with missing condition parameters should fail validation"
        response = self.rule_config_page.submit_rule_schema_api(incomplete_condition_schema, api_url, headers)
        assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"
        response_json = response.json()
        assert "error" in response_json, "Error should be present in response when condition is incomplete"
        assert "missing" in response_json["error"].lower() or "incomplete" in response_json["error"].lower(), f"Expected error about missing/incomplete condition, got '{response_json['error']}'"
