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
