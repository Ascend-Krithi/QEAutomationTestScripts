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

    def test_TC_SCRUM158_01_create_rule_with_all_types(self):
        """
        Test Case TC_SCRUM158_01
        Steps:
        1. Prepare a JSON rule schema with all supported trigger, condition, and action types populated.
        2. Submit the rule schema to the API endpoint for rule creation.
        3. Retrieve the created rule from the database.
        4. Validate the rule matches the submitted schema.
        """
        self.rule_config_page.enter_rule_name('TestRule_AllTypes')
        self.rule_config_page.click_save()
        # Add assertions and API/DB calls as appropriate for your environment
        # This is a UI-level simulation
        # assert rule_created_in_db == expected_schema

    def test_TC_SCRUM158_02_create_rule_with_multiple_conditions_actions(self):
        """
        Test Case TC_SCRUM158_02
        Steps:
        1. Prepare a rule schema with two conditions and two actions.
        2. Submit the schema to the API endpoint.
        3. Verify rule logic via simulation.
        4. Validate all conditions and actions are evaluated as expected.
        """
        self.rule_config_page.enter_rule_name('TestRule_MultiCondAct')
        self.rule_config_page.click_save()
        # Add assertions and API/DB calls as appropriate for your environment
        # This is a UI-level simulation
        # assert rule_evaluation == expected_result

    def test_TC_SCRUM158_05_invalid_trigger_schema(self):
        """
        Test Case TC_SCRUM158_05
        Steps:
        1. Prepare a rule schema with an invalid trigger value.
        2. Validate the schema using the UI.
        3. Submit the schema via API.
        4. Assert API returns 400 Bad Request with error about invalid value.
        """
        api_url = "http://localhost:8000/rules"
        headers = {"Content-Type": "application/json"}
        schema = self.rule_config_page.prepare_invalid_trigger_schema()
        is_valid, error_msg = self.rule_config_page.validate_rule_schema(str(schema))
        assert not is_valid, f"Schema should be invalid but validation passed. Error: {error_msg}"
        status_code, response = self.rule_config_page.submit_rule_schema_api(schema, api_url, headers)
        assert status_code == 400, f"API should return 400 Bad Request, got {status_code}. Response: {response}"
        assert 'invalid value' in str(response), "Expected error about invalid value in response."

    def test_TC_SCRUM158_06_condition_missing_params_schema(self):
        """
        Test Case TC_SCRUM158_06
        Steps:
        1. Prepare a rule schema with a condition missing required parameters.
        2. Validate the schema using the UI.
        3. Submit the schema via API.
        4. Assert API returns 400 Bad Request with error about incomplete condition.
        """
        api_url = "http://localhost:8000/rules"
        headers = {"Content-Type": "application/json"}
        schema = self.rule_config_page.prepare_condition_missing_params_schema()
        is_valid, error_msg = self.rule_config_page.validate_rule_schema(str(schema))
        assert not is_valid, f"Schema should be invalid but validation passed. Error: {error_msg}"
        status_code, response = self.rule_config_page.submit_rule_schema_api(schema, api_url, headers)
        assert status_code == 400, f"API should return 400 Bad Request, got {status_code}. Response: {response}"
        assert 'incomplete condition' in str(response), "Expected error about incomplete condition in response."
