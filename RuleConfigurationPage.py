# RuleConfigurationPage.py
"""
PageClass for Rule Configuration Page
Covers: TC_SCRUM158_05 (invalid trigger), TC_SCRUM158_06 (missing condition parameter)
Ensures schema validation and error handling for rules API.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    """
    Page Object Model for Rule Configuration Page.
    Covers negative scenarios:
    - TC_SCRUM158_05: Invalid trigger value in rule schema.
    - TC_SCRUM158_06: Missing required parameters in condition.
    """

    # Locators from Locators.json
    JSON_SCHEMA_EDITOR = (By.CSS_SELECTOR, ".monaco-editor")
    VALIDATE_SCHEMA_BTN = (By.ID, "btn-verify-json")
    SCHEMA_ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def __init__(self, driver: WebDriver):
        """
        Initializes the RuleConfigurationPage with a WebDriver instance.
        :param driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

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
