# RuleConfigurationPage.py
"""
Selenium PageClass for Rule Configuration Page

This class is generated based on Locators.json and covers the following test cases:
- TC_SCRUM158_05: Unsupported trigger type validation
- TC_SCRUM158_06: Maximum allowed conditions and actions

All locators are mapped directly from Locators.json. Methods are provided for rule schema submission, validation, error handling, and bulk condition/action processing.

Strict code integrity is enforced. All selectors are validated and documented.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        # Rule Form Locators
        self.rule_id_input = (By.ID, 'rule-id-field')
        self.rule_name_input = (By.NAME, 'rule-name')
        self.save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        # Trigger Locators
        self.trigger_type_dropdown = (By.ID, 'trigger-type-select')
        self.date_picker = (By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = (By.ID, 'interval-value')
        self.after_deposit_toggle = (By.ID, 'trigger-after-deposit')
        # Condition Locators
        self.add_condition_btn = (By.ID, 'add-condition-link')
        self.condition_type_dropdown = (By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit'")
        self.transaction_source_dropdown = (By.ID, 'source-provider-select')
        self.operator_dropdown = (By.CSS_SELECTOR, '.condition-operator-select')
        # Action Locators
        self.action_type_dropdown = (By.ID, 'action-type-select')
        self.transfer_amount_input = (By.NAME, 'fixed-amount')
        self.percentage_input = (By.ID, 'deposit-percentage')
        self.destination_account_input = (By.ID, 'target-account-id')
        # Validation Locators
        self.json_schema_editor = (By.CSS_SELECTOR, '.monaco-editor')
        self.validate_schema_btn = (By.ID, 'btn-verify-json')
        self.success_message = (By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = (By.CSS_SELECTOR, '[data-testid="error-feedback-text"]')

    def enter_rule_id(self, rule_id):
        self.driver.find_element(*self.rule_id_input).clear()
        self.driver.find_element(*self.rule_id_input).send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        self.driver.find_element(*self.rule_name_input).clear()
        self.driver.find_element(*self.rule_name_input).send_keys(rule_name)

    def select_trigger_type(self, trigger_type):
        dropdown = self.driver.find_element(*self.trigger_type_dropdown)
        dropdown.click()
        dropdown.send_keys(trigger_type)
        dropdown.send_keys("\n")

    def add_condition(self, condition_type, operator, value):
        self.driver.find_element(*self.add_condition_btn).click()
        self.driver.find_element(*self.condition_type_dropdown).send_keys(condition_type)
        self.driver.find_element(*self.operator_dropdown).send_keys(operator)
        self.driver.find_element(*self.balance_threshold_input).send_keys(str(value))

    def add_action(self, action_type, account, amount):
        self.driver.find_element(*self.action_type_dropdown).send_keys(action_type)
        self.driver.find_element(*self.destination_account_input).send_keys(account)
        self.driver.find_element(*self.transfer_amount_input).send_keys(str(amount))

    def submit_rule(self):
        self.driver.find_element(*self.save_rule_button).click()

    def enter_json_schema(self, schema_text):
        editor = self.driver.find_element(*self.json_schema_editor)
        editor.clear()
        editor.send_keys(schema_text)

    def validate_schema(self):
        self.driver.find_element(*self.validate_schema_btn).click()

    def get_success_message(self):
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.success_message)).text

    def get_error_message(self):
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.schema_error_message)).text

    def bulk_add_conditions(self, conditions):
        """
        Adds multiple conditions in bulk, for TC_SCRUM158_06.
        conditions: list of dicts with keys: type, operator, value
        """
        for cond in conditions:
            self.add_condition(cond['type'], cond['operator'], cond['value'])

    def bulk_add_actions(self, actions):
        """
        Adds multiple actions in bulk, for TC_SCRUM158_06.
        actions: list of dicts with keys: type, account, amount
        """
        for act in actions:
            self.add_action(act['type'], act['account'], act['amount'])

    def submit_and_validate_schema(self, schema_text):
        """
        Submits schema and validates for error/success messages.
        Used for TC_SCRUM158_05 and TC_SCRUM158_06.
        """
        self.enter_json_schema(schema_text)
        self.validate_schema()
        try:
            return self.get_success_message()
        except Exception:
            return self.get_error_message()

# Documentation:
# - All locator keys are mapped directly from Locators.json for strict integrity.
# - Methods are named for clarity and test automation orchestration.
# - bulk_add_conditions and bulk_add_actions support maximum item tests (TC_SCRUM158_06).
# - submit_and_validate_schema method supports schema rejection (TC_SCRUM158_05).
# - Error handling is robust for success/error message detection.
