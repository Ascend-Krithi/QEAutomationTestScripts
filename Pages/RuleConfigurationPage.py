import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        # Locators from Locators.json
        self.rule_id_input = (By.ID, 'rule-id-field')
        self.rule_name_input = (By.NAME, 'rule-name')
        self.save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        self.trigger_type_dropdown = (By.ID, 'trigger-type-select')
        self.date_picker = (By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = (By.ID, 'interval-value')
        self.after_deposit_toggle = (By.ID, 'trigger-after-deposit')
        self.add_condition_btn = (By.ID, 'add-condition-link')
        self.condition_type_dropdown = (By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit']")
        self.transaction_source_dropdown = (By.ID, 'source-provider-select')
        self.operator_dropdown = (By.CSS_SELECTOR, '.condition-operator-select')
        self.action_type_dropdown = (By.ID, 'action-type-select')
        self.transfer_amount_input = (By.NAME, 'fixed-amount')
        self.percentage_input = (By.ID, 'deposit-percentage')
        self.destination_account_input = (By.ID, 'target-account-id')
        self.json_schema_editor = (By.CSS_SELECTOR, '.monaco-editor')
        self.validate_schema_btn = (By.ID, 'btn-verify-json')
        self.success_message = (By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def enter_rule_schema(self, schema_json):
        """
        Enters the rule schema JSON into the schema editor.
        """
        schema_editor = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.json_schema_editor)
        )
        # Clear and enter new schema
        self.driver.execute_script("arguments[0].innerText = arguments[1];", schema_editor, schema_json)

    def validate_schema(self):
        """
        Clicks the validate schema button and waits for validation result.
        Returns True if success, False if error.
        """
        validate_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.validate_schema_btn)
        )
        validate_btn.click()
        # Wait for either success or error message
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.success_message)
            )
            return True
        except:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(self.schema_error_message)
                )
                return False
            except:
                return False

    def save_rule(self):
        """
        Clicks the save rule button.
        """
        save_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.save_rule_button)
        )
        save_btn.click()

    def create_rule_from_schema(self, schema_json):
        """
        High-level method: enters schema, validates, and saves rule.
        Returns True if rule creation is successful, False otherwise.
        """
        self.enter_rule_schema(schema_json)
        if not self.validate_schema():
            return False
        self.save_rule()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.success_message)
            )
            return True
        except:
            return False

    def get_rule_success_message(self):
        """
        Returns the success message text after rule creation.
        """
        success_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.success_message)
        )
        return success_elem.text

    def get_rule_error_message(self):
        """
        Returns the error message text after schema validation failure.
        """
        error_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.schema_error_message)
        )
        return error_elem.text

    # --- New methods for TC_SCRUM158_03 and TC_SCRUM158_04 ---

    def set_recurring_interval_trigger(self, interval_value):
        """
        Selects 'Recurring Interval' in the trigger type dropdown and sets the interval value.
        """
        trigger_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.trigger_type_dropdown)
        )
        trigger_dropdown.click()
        # Assuming the dropdown opens and 'Recurring Interval' is selectable by visible text
        recurring_option = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//option[contains(text(),'Recurring Interval')]")
        )
        recurring_option.click()
        interval_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.recurring_interval_input)
        )
        interval_input.clear()
        interval_input.send_keys(str(interval_value))

    def verify_rule_scheduling_success(self):
        """
        Waits for and returns the success message after scheduling a rule.
        """
        success_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.success_message)
        )
        return success_elem.text

    def submit_schema_missing_trigger(self, schema_json):
        """
        Submits a rule schema missing the 'trigger' field and returns the error message.
        """
        self.enter_rule_schema(schema_json)
        self.validate_schema()
        error_msg = self.get_rule_error_message()
        return error_msg

    def create_and_verify_recurring_interval_rule(self, rule_schema, interval_value):
        """
        Composite method for TC_SCRUM158_03:
        - Sets recurring interval trigger.
        - Enters rule schema.
        - Validates and saves rule.
        - Returns success message.
        """
        self.set_recurring_interval_trigger(interval_value)
        self.enter_rule_schema(rule_schema)
        if not self.validate_schema():
            return None
        self.save_rule()
        return self.verify_rule_scheduling_success()

    def verify_error_for_missing_trigger(self, rule_schema):
        """
        Composite method for TC_SCRUM158_04:
        - Enters schema missing 'trigger'.
        - Validates schema.
        - Returns error message.
        """
        self.enter_rule_schema(rule_schema)
        self.validate_schema()
        return self.get_rule_error_message()
