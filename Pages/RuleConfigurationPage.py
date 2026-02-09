"""
RuleConfigurationPage.py

Selenium PageClass for Rule Configuration Page.
Handles rule schema creation, validation, and metadata operations as per TC_SCRUM158_03, TC_SCRUM158_04, TC_SCRUM158_05, and TC_SCRUM158_06.

Author: Automation Orchestration Agent
Created: 2024-06-XX
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    """
    Page Object for Rule Configuration Page.
    Implements locators and methods for rule schema creation, validation, and metadata handling.
    """

    # Locators from Locators.json
    rule_id_input = (By.ID, "rule-id-field")
    rule_name_input = (By.NAME, "rule-name")
    save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")

    trigger_type_dropdown = (By.ID, "trigger-type-select")
    date_picker = (By.CSS_SELECTOR, "input[type='date']")
    recurring_interval_input = (By.ID, "interval-value")
    after_deposit_toggle = (By.ID, "trigger-after-deposit")

    add_condition_btn = (By.ID, "add-condition-link")
    condition_type_dropdown = (By.CSS_SELECTOR, "select.condition-type")
    balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit']")
    transaction_source_dropdown = (By.ID, "source-provider-select")
    operator_dropdown = (By.CSS_SELECTOR, ".condition-operator-select")

    action_type_dropdown = (By.ID, "action-type-select")
    transfer_amount_input = (By.NAME, "fixed-amount")
    percentage_input = (By.ID, "deposit-percentage")
    destination_account_input = (By.ID, "target-account-id")

    json_schema_editor = (By.CSS_SELECTOR, ".monaco-editor")
    validate_schema_btn = (By.ID, "btn-verify-json")
    success_message = (By.CSS_SELECTOR, ".alert-success")
    schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def enter_rule_id(self, rule_id):
        elem = self.wait.until(EC.visibility_of_element_located(self.rule_id_input))
        elem.clear()
        elem.send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        elem = self.wait.until(EC.visibility_of_element_located(self.rule_name_input))
        elem.clear()
        elem.send_keys(rule_name)

    def select_trigger_type(self, trigger_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.trigger_type_dropdown))
        dropdown.click()
        dropdown.send_keys(trigger_type)

    def set_recurring_interval(self, interval):
        elem = self.wait.until(EC.visibility_of_element_located(self.recurring_interval_input))
        elem.clear()
        elem.send_keys(str(interval))

    def toggle_after_deposit(self, enable=True):
        toggle = self.wait.until(EC.element_to_be_clickable(self.after_deposit_toggle))
        if (toggle.is_selected() != enable):
            toggle.click()

    def add_condition(self, condition_type, balance_threshold=None, transaction_source=None, operator=None):
        self.wait.until(EC.element_to_be_clickable(self.add_condition_btn)).click()
        self.wait.until(EC.element_to_be_clickable(self.condition_type_dropdown)).send_keys(condition_type)
        if balance_threshold is not None:
            self.wait.until(EC.visibility_of_element_located(self.balance_threshold_input)).send_keys(str(balance_threshold))
        if transaction_source is not None:
            self.wait.until(EC.element_to_be_clickable(self.transaction_source_dropdown)).send_keys(transaction_source)
        if operator is not None:
            self.wait.until(EC.element_to_be_clickable(self.operator_dropdown)).send_keys(operator)

    def select_action_type(self, action_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.action_type_dropdown))
        dropdown.click()
        dropdown.send_keys(action_type)

    def enter_transfer_amount(self, amount):
        elem = self.wait.until(EC.visibility_of_element_located(self.transfer_amount_input))
        elem.clear()
        elem.send_keys(str(amount))

    def enter_percentage(self, percentage):
        elem = self.wait.until(EC.visibility_of_element_located(self.percentage_input))
        elem.clear()
        elem.send_keys(str(percentage))

    def enter_destination_account(self, account_id):
        elem = self.wait.until(EC.visibility_of_element_located(self.destination_account_input))
        elem.clear()
        elem.send_keys(account_id)

    def enter_json_schema(self, schema_text):
        editor = self.wait.until(EC.visibility_of_element_located(self.json_schema_editor))
        # Monaco editor may require JS injection; placeholder for actual implementation
        self.driver.execute_script("arguments[0].innerText = arguments[1];", editor, schema_text)

    def validate_schema(self):
        self.wait.until(EC.element_to_be_clickable(self.validate_schema_btn)).click()

    def get_success_message(self):
        try:
            msg = self.wait.until(EC.visibility_of_element_located(self.success_message))
            return msg.text
        except:
            return None

    def get_schema_error_message(self):
        try:
            msg = self.wait.until(EC.visibility_of_element_located(self.schema_error_message))
            return msg.text
        except:
            return None

    def save_rule(self):
        self.wait.until(EC.element_to_be_clickable(self.save_rule_button)).click()

    def create_rule_with_metadata(self, rule_id, rule_name, metadata, schema_text):
        """
        Composite method for TC_SCRUM158_03:
        - Enter rule ID, rule name
        - Enter JSON schema with metadata
        - Validate schema
        - Save rule
        """
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        self.enter_json_schema(schema_text)
        self.validate_schema()
        success = self.get_success_message()
        if not success:
            raise Exception("Schema validation failed: " + str(self.get_schema_error_message()))
        self.save_rule()

    def create_rule_missing_trigger(self, rule_id, rule_name, schema_text):
        """
        Composite method for TC_SCRUM158_04:
        - Enter rule ID, rule name
        - Enter JSON schema missing trigger
        - Validate schema
        - Expect error message
        """
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        self.enter_json_schema(schema_text)
        self.validate_schema()
        error = self.get_schema_error_message()
        if not error:
            raise Exception("Expected schema error, but none found.")

    def submit_rule_with_invalid_trigger(self, rule_id, rule_name, schema_text):
        """
        TC_SCRUM158_05:
        - Prepare rule schema with invalid trigger value.
        - Submit schema.
        - Validate that error message is shown for invalid trigger.
        """
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        self.enter_json_schema(schema_text)
        self.validate_schema()
        error = self.get_schema_error_message()
        if not error or "invalid value" not in error.lower():
            raise Exception("Expected error about invalid trigger value, got: " + str(error))

    def submit_rule_with_incomplete_condition(self, rule_id, rule_name, schema_text):
        """
        TC_SCRUM158_06:
        - Prepare rule schema with condition missing required parameters.
        - Submit schema.
        - Validate that error message is shown for incomplete condition.
        """
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        self.enter_json_schema(schema_text)
        self.validate_schema()
        error = self.get_schema_error_message()
        if not error or "incomplete condition" not in error.lower():
            raise Exception("Expected error about incomplete condition, got: " + str(error))

    def retrieve_rule_metadata(self, rule_id):
        """
        Placeholder for API interaction to retrieve rule and verify metadata.
        Actual implementation would use requests or similar library for GET /rules/<rule_id>.
        """
        pass  # To be implemented in integration tests

# End of RuleConfigurationPage.py

"""
Documentation:

Executive Summary:
This PageClass automates rule schema creation, validation, and metadata handling for the Rule Configuration Page, supporting test cases TC_SCRUM158_03, TC_SCRUM158_04, TC_SCRUM158_05, and TC_SCRUM158_06. It leverages locators from Locators.json and provides robust methods for end-to-end Selenium automation.

Implementation Guide:
- Place this file in the Pages folder.
- Instantiate RuleConfigurationPage with a Selenium WebDriver.
- Use composite methods for test case automation:
    - create_rule_with_metadata() for valid schema with metadata.
    - create_rule_missing_trigger() for invalid schema missing trigger.
    - submit_rule_with_invalid_trigger() for invalid trigger value.
    - submit_rule_with_incomplete_condition() for incomplete condition.
- Extend retrieve_rule_metadata() with API calls for full validation.

Quality Assurance Report:
- All locators strictly follow Locators.json.
- Methods are atomic and composable, supporting robust test case coverage.
- Composite methods encapsulate test case logic for maintainability.
- Exception handling ensures failures are reported with actionable messages.

Troubleshooting Guide:
- If element not found, verify Locators.json matches UI.
- For Monaco editor, JS injection is used; adapt as needed for your environment.
- API retrieval is a placeholder; implement with requests for integration.

Future Considerations:
- Add API integration for rule retrieval/validation.
- Parameterize composite methods for broader coverage.
- Enhance Monaco editor interaction for dynamic schema editing.
- Implement logging and reporting for advanced QA analytics.

"""
