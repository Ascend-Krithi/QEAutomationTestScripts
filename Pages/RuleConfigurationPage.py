import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class RuleConfigurationPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- Locators ---
    rule_id_input = (By.ID, 'rule-id-field')
    rule_name_input = (By.NAME, 'rule-name')
    save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")

    trigger_type_dropdown = (By.ID, 'trigger-type-select')
    date_picker = (By.CSS_SELECTOR, "input[type='date']")
    recurring_interval_input = (By.ID, 'interval-value')
    after_deposit_toggle = (By.ID, 'trigger-after-deposit')

    add_condition_btn = (By.ID, 'add-condition-link')
    condition_type_dropdown = (By.CSS_SELECTOR, 'select.condition-type')
    balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit'")
    transaction_source_dropdown = (By.ID, 'source-provider-select')
    operator_dropdown = (By.CSS_SELECTOR, '.condition-operator-select')

    action_type_dropdown = (By.ID, 'action-type-select')
    transfer_amount_input = (By.NAME, 'fixed-amount')
    percentage_input = (By.ID, 'deposit-percentage')
    destination_account_input = (By.ID, 'target-account-id')

    json_schema_editor = (By.CSS_SELECTOR, '.monaco-editor')
    validate_schema_btn = (By.ID, 'btn-verify-json')
    success_message = (By.CSS_SELECTOR, '.alert-success')
    schema_error_message = (By.CSS_SELECTOR, '[data-testid="error-feedback-text"]')

    # --- Page Actions ---
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
        dropdown.send_keys(Keys.RETURN)

    def set_specific_date_trigger(self, date_str):
        self.select_trigger_type('specific_date')
        date_input = self.wait.until(EC.visibility_of_element_located(self.date_picker))
        date_input.clear()
        date_input.send_keys(date_str)

    def set_recurring_trigger(self, interval):
        self.select_trigger_type('recurring')
        interval_input = self.wait.until(EC.visibility_of_element_located(self.recurring_interval_input))
        interval_input.clear()
        interval_input.send_keys(interval)

    def set_after_deposit_trigger(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.after_deposit_toggle))
        toggle.click()

    def add_condition(self, condition_type, operator=None, value=None, source=None):
        add_btn = self.wait.until(EC.element_to_be_clickable(self.add_condition_btn))
        add_btn.click()
        type_dropdown = self.wait.until(EC.visibility_of_element_located(self.condition_type_dropdown))
        type_dropdown.click()
        type_dropdown.send_keys(condition_type)
        type_dropdown.send_keys(Keys.RETURN)
        if operator:
            operator_dropdown = self.wait.until(EC.visibility_of_element_located(self.operator_dropdown))
            operator_dropdown.click()
            operator_dropdown.send_keys(operator)
            operator_dropdown.send_keys(Keys.RETURN)
        if value:
            if condition_type == 'balance_threshold':
                value_input = self.wait.until(EC.visibility_of_element_located(self.balance_threshold_input))
                value_input.clear()
                value_input.send_keys(str(value))
        if source:
            source_dropdown = self.wait.until(EC.visibility_of_element_located(self.transaction_source_dropdown))
            source_dropdown.click()
            source_dropdown.send_keys(source)
            source_dropdown.send_keys(Keys.RETURN)

    def select_action_type(self, action_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.action_type_dropdown))
        dropdown.click()
        dropdown.send_keys(action_type)
        dropdown.send_keys(Keys.RETURN)

    def set_fixed_amount_action(self, amount, destination_account):
        self.select_action_type('fixed_amount')
        amount_input = self.wait.until(EC.visibility_of_element_located(self.transfer_amount_input))
        amount_input.clear()
        amount_input.send_keys(str(amount))
        dest_input = self.wait.until(EC.visibility_of_element_located(self.destination_account_input))
        dest_input.clear()
        dest_input.send_keys(destination_account)

    def set_percentage_of_deposit_action(self, percentage, destination_account):
        self.select_action_type('percentage_of_deposit')
        perc_input = self.wait.until(EC.visibility_of_element_located(self.percentage_input))
        perc_input.clear()
        perc_input.send_keys(str(percentage))
        dest_input = self.wait.until(EC.visibility_of_element_located(self.destination_account_input))
        dest_input.clear()
        dest_input.send_keys(destination_account)

    def enter_json_rule(self, rule_json):
        editor = self.wait.until(EC.visibility_of_element_located(self.json_schema_editor))
        editor.click()
        editor.clear()
        editor.send_keys(rule_json)

    def validate_rule_schema(self):
        validate_btn = self.wait.until(EC.element_to_be_clickable(self.validate_schema_btn))
        validate_btn.click()

    def is_success_message_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.success_message))
            return True
        except:
            return False

    def is_schema_error_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.schema_error_message))
            return True
        except:
            return False

    def save_rule(self):
        save_btn = self.wait.until(EC.element_to_be_clickable(self.save_rule_button))
        save_btn.click()

    # --- Composite Test Flows ---
    def create_rule_with_specific_date_trigger(self, rule_id, rule_name, date_str, amount, destination_account, rule_json):
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        self.set_specific_date_trigger(date_str)
        self.set_fixed_amount_action(amount, destination_account)
        self.enter_json_rule(rule_json)
        self.validate_rule_schema()
        self.save_rule()

    def create_rule_with_recurring_trigger(self, rule_id, rule_name, interval, percentage, destination_account, rule_json):
        self.enter_rule_id(rule_id)
        self.enter_rule_name(rule_name)
        self.set_recurring_trigger(interval)
        self.set_percentage_of_deposit_action(percentage, destination_account)
        self.enter_json_rule(rule_json)
        self.validate_rule_schema()
        self.save_rule()
