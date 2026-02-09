# RuleConfigurationPage.py
"""
PageClass for Rule Configuration Page
Covers: TC_SCRUM158_05 (invalid trigger), TC_SCRUM158_06 (missing condition parameter), TC_SCRUM158_07 (max conditions/actions), TC_SCRUM158_08 (empty conditions/actions)
Ensures schema validation, rule creation, persistence validation, and error handling for rules API.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json

class RuleConfigurationPage:
    """
    Page Object Model for Rule Configuration Page.
    Covers negative and positive scenarios:
    - TC_SCRUM158_05: Invalid trigger value in rule schema.
    - TC_SCRUM158_06: Missing required parameters in condition.
    - TC_SCRUM158_07: Max conditions/actions, POST/GET persistence.
    - TC_SCRUM158_08: Empty conditions/actions, schema validation and API response.
    """

    # Locators from Locators.json
    JSON_SCHEMA_EDITOR = (By.CSS_SELECTOR, ".monaco-editor")
    VALIDATE_SCHEMA_BTN = (By.ID, "btn-verify-json")
    SCHEMA_ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")

    def __init__(self, driver: WebDriver, api_base_url=None, api_token=None):
        """
        Initializes the RuleConfigurationPage with a WebDriver instance.
        :param driver: Selenium WebDriver instance
        :param api_base_url: API base URL for direct API calls
        :param api_token: API token for authentication
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.api_base_url = api_base_url
        self.api_token = api_token

    def enter_json_schema(self, schema: str):
        """
        Enters the JSON schema in the schema editor.
        :param schema: JSON string
        """
        editor = self.wait.until(EC.visibility_of_element_located(self.JSON_SCHEMA_EDITOR))
        editor.clear()
        editor.send_keys(schema)

    def click_validate_schema(self):
        """
        Clicks the validate schema button.
        """
        validate_btn = self.wait.until(EC.element_to_be_clickable(self.VALIDATE_SCHEMA_BTN))
        validate_btn.click()

    def get_schema_error_message(self) -> str:
        """
        Returns the error message displayed for invalid schema.
        :return: Error message text
        """
        error_elem = self.wait.until(EC.visibility_of_element_located(self.SCHEMA_ERROR_MESSAGE))
        return error_elem.text

    def get_success_message(self) -> str:
        """
        Returns the success message displayed for valid schema.
        :return: Success message text
        """
        elem = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
        return elem.text

    def validate_invalid_trigger(self):
        """
        Test case: TC_SCRUM158_05
        Prepare a rule schema with an invalid trigger value and validate error handling.
        """
        invalid_schema = '{"trigger": "unknown_trigger", "conditions": [{"type": "amount_above", "amount": 100}], "actions": [{"type": "transfer", "amount": 50}]}'
        self.enter_json_schema(invalid_schema)
        self.click_validate_schema()
        return self.get_schema_error_message().strip()

    def validate_missing_condition_parameter(self):
        """
        Test case: TC_SCRUM158_06
        Prepare a rule schema with a condition missing required parameters and validate error handling.
        """
        invalid_schema = '{"trigger": "after_deposit", "conditions": [{"type": "amount_above"}], "actions": [{"type": "transfer", "amount": 50}]}'
        self.enter_json_schema(invalid_schema)
        self.click_validate_schema()
        return self.get_schema_error_message().strip()

    # --- NEW FUNCTIONS FOR TC_SCRUM158_07 and TC_SCRUM158_08 ---

    def prepare_rule_schema(self, conditions, actions, trigger="after_deposit"):
        """
        Prepares a rule schema JSON string.
        :param conditions: List of condition dicts
        :param actions: List of action dicts
        :param trigger: Trigger type
        :return: JSON string
        """
        schema = {
            "trigger": trigger,
            "conditions": conditions,
            "actions": actions
        }
        return json.dumps(schema)

    def submit_rule_schema_api(self, schema_json):
        """
        Submits the rule schema via POST /rules API.
        :param schema_json: JSON string
        :return: (status_code, response_json)
        """
        assert self.api_base_url and self.api_token, "API base URL and token required"
        url = f"{self.api_base_url}/rules"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        resp = requests.post(url, headers=headers, data=schema_json)
        return resp.status_code, resp.json()

    def retrieve_rule_api(self, rule_id):
        """
        Retrieves a rule by ID via GET /rules/<rule_id> API.
        :param rule_id: Rule ID
        :return: (status_code, response_json)
        """
        assert self.api_base_url and self.api_token, "API base URL and token required"
        url = f"{self.api_base_url}/rules/{rule_id}"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        resp = requests.get(url, headers=headers)
        return resp.status_code, resp.json()

    def validate_rule_persistence(self, rule_id, expected_conditions, expected_actions):
        """
        Validates that all conditions and actions are persisted for the given rule ID.
        :param rule_id: Rule ID
        :param expected_conditions: List of expected condition dicts
        :param expected_actions: List of expected action dicts
        :return: True if persisted data matches, else False
        """
        code, data = self.retrieve_rule_api(rule_id)
        if code != 200:
            return False
        conditions_ok = data.get("conditions") == expected_conditions
        actions_ok = data.get("actions") == expected_actions
        return conditions_ok and actions_ok

    def validate_empty_conditions_actions_schema(self):
        """
        Prepares a rule schema with empty conditions/actions, validates via UI and API.
        :return: Tuple (ui_result, api_result)
        """
        empty_schema = self.prepare_rule_schema([], [])
        self.enter_json_schema(empty_schema)
        self.click_validate_schema()
        # UI validation may display error or success
        try:
            ui_result = self.get_success_message()
        except Exception:
            ui_result = self.get_schema_error_message()
        # API validation
        api_status, api_resp = self.submit_rule_schema_api(empty_schema)
        return ui_result, (api_status, api_resp)
