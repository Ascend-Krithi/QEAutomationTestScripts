# RuleConfigurationPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        # Form Locators
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
        self.balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit']")
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
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.rule_id_input)).send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.rule_name_input)).send_keys(rule_name)

    def select_trigger_type(self, trigger_type):
        dropdown = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.trigger_type_dropdown))
        dropdown.click()
        dropdown.send_keys(trigger_type)

    def set_date_trigger(self, date_str):
        date_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.date_picker))
        date_input.send_keys(date_str)

    def set_recurring_interval(self, interval):
        interval_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.recurring_interval_input))
        interval_input.send_keys(str(interval))

    def toggle_after_deposit(self):
        toggle = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.after_deposit_toggle))
        toggle.click()

    def add_condition(self):
        add_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.add_condition_btn))
        add_btn.click()

    def select_condition_type(self, condition_type):
        dropdown = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.condition_type_dropdown))
        dropdown.click()
        dropdown.send_keys(condition_type)

    def set_balance_threshold(self, threshold):
        threshold_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.balance_threshold_input))
        threshold_input.send_keys(str(threshold))

    def select_transaction_source(self, source):
        dropdown = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.transaction_source_dropdown))
        dropdown.click()
        dropdown.send_keys(source)

    def select_operator(self, operator):
        dropdown = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.operator_dropdown))
        dropdown.click()
        dropdown.send_keys(operator)

    def select_action_type(self, action_type):
        dropdown = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.action_type_dropdown))
        dropdown.click()
        dropdown.send_keys(action_type)

    def set_transfer_amount(self, amount):
        amount_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.transfer_amount_input))
        amount_input.send_keys(str(amount))

    def set_percentage(self, percentage):
        percentage_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.percentage_input))
        percentage_input.send_keys(str(percentage))

    def set_destination_account(self, account_id):
        account_input = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.destination_account_input))
        account_input.send_keys(account_id)

    def enter_json_schema(self, schema_text):
        editor = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.json_schema_editor))
        editor.clear()
        editor.send_keys(schema_text)

    def validate_schema(self):
        validate_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.validate_schema_btn))
        validate_btn.click()

    def is_success_message_displayed(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.success_message))
            return True
        except:
            return False

    def get_schema_error_message(self):
        try:
            error_element = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.schema_error_message))
            return error_element.text
        except:
            return None

    def save_rule(self):
        save_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.save_rule_button))
        save_btn.click()
