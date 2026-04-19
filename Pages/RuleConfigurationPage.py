# imports
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import time

class RuleConfigurationPage:
    SUPPORTED_TRIGGER_TYPES = ["date", "recurring", "after_deposit"]  # Example supported triggers

    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Rule Form Locators
        self.rule_id_input = driver.find_element(By.ID, 'rule-id-field')
        self.rule_name_input = driver.find_element(By.NAME, 'rule-name')
        self.save_rule_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        # Trigger Locators
        self.trigger_type_dropdown = driver.find_element(By.ID, 'trigger-type-select')
        self.date_picker = driver.find_element(By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = driver.find_element(By.ID, 'interval-value')
        self.after_deposit_toggle = driver.find_element(By.ID, 'trigger-after-deposit')
        # Condition Locators
        self.add_condition_btn = driver.find_element(By.ID, 'add-condition-link')
        self.condition_type_dropdown = driver.find_element(By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = driver.find_element(By.NAME, 'balance-limit')
        self.transaction_source_dropdown = driver.find_element(By.ID, 'source-provider-select')
        self.operator_dropdown = driver.find_element(By.CSS_SELECTOR, '.condition-operator-select')
        # Action Locators
        self.action_type_dropdown = driver.find_element(By.ID, 'action-type-select')
        self.transfer_amount_input = driver.find_element(By.NAME, 'fixed-amount')
        self.percentage_input = driver.find_element(By.ID, 'deposit-percentage')
        self.destination_account_input = driver.find_element(By.ID, 'target-account-id')
        # Validation Locators
        self.json_schema_editor = driver.find_element(By.CSS_SELECTOR, '.monaco-editor')
        self.validate_schema_btn = driver.find_element(By.ID, 'btn-verify-json')
        self.success_message = driver.find_element(By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = driver.find_element(By.CSS_SELECTOR, "[data-testid='error-feedback-text']")
        self.ui_error_message = driver.find_element(By.CSS_SELECTOR, '.alert-danger') if self._element_exists(By.CSS_SELECTOR, '.alert-danger') else None

    def _element_exists(self, by, value):
        try:
            self.driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False

    # ... [existing methods remain unchanged] ...

    # --- NEW TEST AUTOMATION FUNCTIONS FOR TC_SCRUM158_05 and TC_SCRUM158_06 ---
    def test_invalid_trigger_value(self, rule_id: str, rule_name: str, invalid_trigger: str, actions: list, schema_text: str):
        """
        Test Case TC_SCRUM158_05: Submit a rule schema with an invalid trigger value.
        Expects JSON schema validation to fail and API to return 400 Bad Request.
        """
        self.fill_rule_form(rule_id, rule_name)
        try:
            self.select_trigger_type(invalid_trigger)
        except ValueError as ve:
            # Expected: UI validation for unsupported trigger type
            print(f"Expected trigger error: {ve}")
        self.add_multiple_actions(actions)
        self.edit_json_schema(schema_text)
        try:
            self.validate_schema()
        except ValueError as ve:
            print(f"Schema validation failed as expected: {ve}")
            assert "invalid" in str(ve).lower()
        # Simulate API call and check for 400 Bad Request (not implemented in UI test)

    def test_condition_missing_required_parameters(self, rule_id: str, rule_name: str, trigger: str, incomplete_condition: dict, actions: list, schema_text: str):
        """
        Test Case TC_SCRUM158_06: Submit a rule schema with a condition missing required parameters.
        Expects JSON schema validation to fail and API to return 400 Bad Request.
        """
        self.fill_rule_form(rule_id, rule_name)
        self.select_trigger_type(trigger)
        self.add_condition()
        if 'type' in incomplete_condition:
            self.select_condition_type(incomplete_condition['type'])
        # Do NOT fill required fields (to simulate missing params)
        self.add_multiple_actions(actions)
        self.edit_json_schema(schema_text)
        try:
            self.validate_schema()
        except ValueError as ve:
            print(f"Schema validation failed as expected: {ve}")
            assert "incomplete" in str(ve).lower() or "invalid" in str(ve).lower()
        # Simulate API call and check for 400 Bad Request (not implemented in UI test)
