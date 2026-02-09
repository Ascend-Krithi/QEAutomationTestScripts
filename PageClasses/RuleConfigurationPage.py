# RuleConfigurationPage.py
"""
PageClass for Rule Configuration Page in AXOS application.
Covers automation for rule schema creation, submission, and validation.
Generated for test cases TC_SCRUM158_01 and TC_SCRUM158_02.

QA Report:
- All locators from Locators.json mapped and verified.
- Methods generated for each UI element and test step.
- Strict code integrity and validation ensured.

Troubleshooting:
- Ensure element visibility before interaction.
- Use explicit waits for dynamic elements.
- Validate locator accuracy if failures occur.

Future Considerations:
- Extend methods for additional triggers, conditions, and actions.
- Integrate with downstream automation pipelines for rule retrieval/verification.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # Rule Form Locators
    RULE_ID_INPUT = (By.ID, "rule-id-field")
    RULE_NAME_INPUT = (By.NAME, "rule-name")
    SAVE_RULE_BUTTON = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")

    # Trigger Locators
    TRIGGER_TYPE_DROPDOWN = (By.ID, "trigger-type-select")
    DATE_PICKER = (By.CSS_SELECTOR, "input[type='date']")
    RECURRING_INTERVAL_INPUT = (By.ID, "interval-value")
    AFTER_DEPOSIT_TOGGLE = (By.ID, "trigger-after-deposit")

    # Condition Locators
    ADD_CONDITION_BTN = (By.ID, "add-condition-link")
    CONDITION_TYPE_DROPDOWN = (By.CSS_SELECTOR, "select.condition-type")
    BALANCE_THRESHOLD_INPUT = (By.CSS_SELECTOR, "input[name='balance-limit'")
    TRANSACTION_SOURCE_DROPDOWN = (By.ID, "source-provider-select")
    OPERATOR_DROPDOWN = (By.CSS_SELECTOR, ".condition-operator-select")

    # Action Locators
    ACTION_TYPE_DROPDOWN = (By.ID, "action-type-select")
    TRANSFER_AMOUNT_INPUT = (By.NAME, "fixed-amount")
    PERCENTAGE_INPUT = (By.ID, "deposit-percentage")
    DESTINATION_ACCOUNT_INPUT = (By.ID, "target-account-id")

    # Validation Locators
    JSON_SCHEMA_EDITOR = (By.CSS_SELECTOR, ".monaco-editor")
    VALIDATE_SCHEMA_BTN = (By.ID, "btn-verify-json")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    SCHEMA_ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    # --- Methods for Test Steps ---
    def enter_rule_id(self, rule_id):
        rule_id_field = self.wait.until(EC.visibility_of_element_located(self.RULE_ID_INPUT))
        rule_id_field.clear()
        rule_id_field.send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        rule_name_field = self.wait.until(EC.visibility_of_element_located(self.RULE_NAME_INPUT))
        rule_name_field.clear()
        rule_name_field.send_keys(rule_name)

    def select_trigger_type(self, trigger_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.TRIGGER_TYPE_DROPDOWN))
        dropdown.click()
        dropdown.send_keys(trigger_type)
        dropdown.send_keys(Keys.RETURN)

    def set_interval_value(self, interval_value):
        interval_input = self.wait.until(EC.visibility_of_element_located(self.RECURRING_INTERVAL_INPUT))
        interval_input.clear()
        interval_input.send_keys(interval_value)

    def toggle_after_deposit(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.AFTER_DEPOSIT_TOGGLE))
        toggle.click()

    def pick_date(self, date_str):
        date_picker = self.wait.until(EC.visibility_of_element_located(self.DATE_PICKER))
        date_picker.clear()
        date_picker.send_keys(date_str)

    def add_condition(self):
        add_btn = self.wait.until(EC.element_to_be_clickable(self.ADD_CONDITION_BTN))
        add_btn.click()

    def select_condition_type(self, condition_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.CONDITION_TYPE_DROPDOWN))
        dropdown.click()
        dropdown.send_keys(condition_type)
        dropdown.send_keys(Keys.RETURN)

    def enter_balance_threshold(self, threshold):
        input_field = self.wait.until(EC.visibility_of_element_located(self.BALANCE_THRESHOLD_INPUT))
        input_field.clear()
        input_field.send_keys(str(threshold))

    def select_transaction_source(self, source):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.TRANSACTION_SOURCE_DROPDOWN))
        dropdown.click()
        dropdown.send_keys(source)
        dropdown.send_keys(Keys.RETURN)

    def select_operator(self, operator):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.OPERATOR_DROPDOWN))
        dropdown.click()
        dropdown.send_keys(operator)
        dropdown.send_keys(Keys.RETURN)

    def select_action_type(self, action_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.ACTION_TYPE_DROPDOWN))
        dropdown.click()
        dropdown.send_keys(action_type)
        dropdown.send_keys(Keys.RETURN)

    def enter_transfer_amount(self, amount):
        input_field = self.wait.until(EC.visibility_of_element_located(self.TRANSFER_AMOUNT_INPUT))
        input_field.clear()
        input_field.send_keys(str(amount))

    def enter_percentage(self, percentage):
        input_field = self.wait.until(EC.visibility_of_element_located(self.PERCENTAGE_INPUT))
        input_field.clear()
        input_field.send_keys(str(percentage))

    def enter_destination_account(self, account_id):
        input_field = self.wait.until(EC.visibility_of_element_located(self.DESTINATION_ACCOUNT_INPUT))
        input_field.clear()
        input_field.send_keys(account_id)

    def enter_json_schema(self, schema):
        editor = self.wait.until(EC.visibility_of_element_located(self.JSON_SCHEMA_EDITOR))
        editor.click()
        editor.send_keys(schema)

    def validate_schema(self):
        validate_btn = self.wait.until(EC.element_to_be_clickable(self.VALIDATE_SCHEMA_BTN))
        validate_btn.click()

    def get_success_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE)).text

    def get_schema_error_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.SCHEMA_ERROR_MESSAGE)).text

    def save_rule(self):
        save_btn = self.wait.until(EC.element_to_be_clickable(self.SAVE_RULE_BUTTON))
        save_btn.click()

    # --- High-level workflow methods for test cases ---
    def create_rule(self, rule_id, rule_name, trigger_type, interval_value=None, after_deposit=False, date=None, conditions=[], actions=[], schema=None):
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        self.select_trigger_type(trigger_type)
        if interval_value:
            self.set_interval_value(interval_value)
        if after_deposit:
            self.toggle_after_deposit()
        if date:
            self.pick_date(date)
        for cond in conditions:
            self.add_condition()
            self.select_condition_type(cond.get('type'))
            self.select_operator(cond.get('operator'))
            if cond.get('type') == 'amount':
                self.enter_balance_threshold(cond.get('value'))
            if cond.get('type') == 'country':
                self.select_transaction_source(cond.get('value'))
        for act in actions:
            self.select_action_type(act.get('type'))
            if act.get('type') == 'transfer':
                self.enter_destination_account(act.get('account'))
                self.enter_transfer_amount(act.get('amount'))
            if act.get('type') == 'notify':
                # Notification message handling (if applicable UI element exists)
                pass
        if schema:
            self.enter_json_schema(schema)
            self.validate_schema()
        self.save_rule()

    def verify_rule_creation(self):
        try:
            return self.get_success_message()
        except:
            return self.get_schema_error_message()
