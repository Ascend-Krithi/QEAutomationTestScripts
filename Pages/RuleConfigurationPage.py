# RuleConfigurationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- Form Locators ---
    RULE_ID_INPUT = (By.ID, 'rule-id-field')
    RULE_NAME_INPUT = (By.NAME, 'rule-name')
    SAVE_RULE_BUTTON = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")

    # --- Trigger Locators ---
    TRIGGER_TYPE_DROPDOWN = (By.ID, 'trigger-type-select')
    DATE_PICKER = (By.CSS_SELECTOR, "input[type='date']")
    RECURRING_INTERVAL_INPUT = (By.ID, 'interval-value')
    AFTER_DEPOSIT_TOGGLE = (By.ID, 'trigger-after-deposit')

    # --- Condition Locators ---
    ADD_CONDITION_BTN = (By.ID, 'add-condition-link')
    CONDITION_TYPE_DROPDOWN = (By.CSS_SELECTOR, 'select.condition-type')
    BALANCE_THRESHOLD_INPUT = (By.CSS_SELECTOR, "input[name='balance-limit']")
    TRANSACTION_SOURCE_DROPDOWN = (By.ID, 'source-provider-select')
    OPERATOR_DROPDOWN = (By.CSS_SELECTOR, '.condition-operator-select')

    # --- Action Locators ---
    ACTION_TYPE_DROPDOWN = (By.ID, 'action-type-select')
    TRANSFER_AMOUNT_INPUT = (By.NAME, 'fixed-amount')
    PERCENTAGE_INPUT = (By.ID, 'deposit-percentage')
    DESTINATION_ACCOUNT_INPUT = (By.ID, 'target-account-id')

    # --- Validation Locators ---
    JSON_SCHEMA_EDITOR = (By.CSS_SELECTOR, '.monaco-editor')
    VALIDATE_SCHEMA_BTN = (By.ID, 'btn-verify-json')
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, '.alert-success')
    SCHEMA_ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-testid="error-feedback-text"]')

    # --- Methods ---
    def enter_rule_id(self, rule_id):
        elem = self.wait.until(EC.presence_of_element_located(self.RULE_ID_INPUT))
        elem.clear()
        elem.send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        elem = self.wait.until(EC.presence_of_element_located(self.RULE_NAME_INPUT))
        elem.clear()
        elem.send_keys(rule_name)

    def save_rule(self):
        self.wait.until(EC.element_to_be_clickable(self.SAVE_RULE_BUTTON)).click()

    def select_trigger_type(self, trigger_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.TRIGGER_TYPE_DROPDOWN))
        dropdown.click()
        # Add logic to select trigger_type from dropdown

    def set_date(self, date_value):
        date_picker = self.wait.until(EC.element_to_be_clickable(self.DATE_PICKER))
        date_picker.clear()
        date_picker.send_keys(date_value)

    def set_recurring_interval(self, interval):
        interval_input = self.wait.until(EC.presence_of_element_located(self.RECURRING_INTERVAL_INPUT))
        interval_input.clear()
        interval_input.send_keys(interval)

    def toggle_after_deposit(self, enable=True):
        toggle = self.wait.until(EC.element_to_be_clickable(self.AFTER_DEPOSIT_TOGGLE))
        if toggle.is_selected() != enable:
            toggle.click()

    def add_condition(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_CONDITION_BTN)).click()

    def select_condition_type(self, condition_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.CONDITION_TYPE_DROPDOWN))
        dropdown.click()
        # Add logic to select condition_type

    def set_balance_threshold(self, threshold):
        input_elem = self.wait.until(EC.presence_of_element_located(self.BALANCE_THRESHOLD_INPUT))
        input_elem.clear()
        input_elem.send_keys(threshold)

    def select_transaction_source(self, source):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.TRANSACTION_SOURCE_DROPDOWN))
        dropdown.click()
        # Add logic to select source

    def select_operator(self, operator):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.OPERATOR_DROPDOWN))
        dropdown.click()
        # Add logic to select operator

    def select_action_type(self, action_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.ACTION_TYPE_DROPDOWN))
        dropdown.click()
        # Add logic to select action_type

    def set_transfer_amount(self, amount):
        input_elem = self.wait.until(EC.presence_of_element_located(self.TRANSFER_AMOUNT_INPUT))
        input_elem.clear()
        input_elem.send_keys(amount)

    def set_percentage(self, percentage):
        input_elem = self.wait.until(EC.presence_of_element_located(self.PERCENTAGE_INPUT))
        input_elem.clear()
        input_elem.send_keys(percentage)

    def set_destination_account(self, account_id):
        input_elem = self.wait.until(EC.presence_of_element_located(self.DESTINATION_ACCOUNT_INPUT))
        input_elem.clear()
        input_elem.send_keys(account_id)

    def enter_json_schema(self, schema_text):
        editor = self.wait.until(EC.presence_of_element_located(self.JSON_SCHEMA_EDITOR))
        editor.clear()
        editor.send_keys(schema_text)

    def validate_schema(self):
        self.wait.until(EC.element_to_be_clickable(self.VALIDATE_SCHEMA_BTN)).click()

    def get_success_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE)).text

    def get_schema_error_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.SCHEMA_ERROR_MESSAGE)).text
