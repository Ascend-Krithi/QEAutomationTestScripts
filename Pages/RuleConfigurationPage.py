# RuleConfigurationPage.py
"""
Selenium PageClass for Automated Transfers Rule Configuration Page.
Covers rule form, triggers, conditions, actions, validation logic, and security validation.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Rule Form
        self.rule_id_input = driver.find_element(By.ID, 'rule-id-field')
        self.rule_name_input = driver.find_element(By.NAME, 'rule-name')
        self.save_rule_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
        # Triggers
        self.trigger_type_dropdown = driver.find_element(By.ID, 'trigger-type-select')
        self.date_picker = driver.find_element(By.CSS_SELECTOR, "input[type='date']")
        self.recurring_interval_input = driver.find_element(By.ID, 'interval-value')
        self.after_deposit_toggle = driver.find_element(By.ID, 'trigger-after-deposit')
        # Conditions
        self.add_condition_btn = driver.find_element(By.ID, 'add-condition-link')
        self.condition_type_dropdown = driver.find_element(By.CSS_SELECTOR, 'select.condition-type')
        self.balance_threshold_input = driver.find_element(By.CSS_SELECTOR, "input[name='balance-limit']")
        self.transaction_source_dropdown = driver.find_element(By.ID, 'source-provider-select')
        self.operator_dropdown = driver.find_element(By.CSS_SELECTOR, '.condition-operator-select')
        # Actions
        self.action_type_dropdown = driver.find_element(By.ID, 'action-type-select')
        self.transfer_amount_input = driver.find_element(By.NAME, 'fixed-amount')
        self.percentage_input = driver.find_element(By.ID, 'deposit-percentage')
        self.destination_account_input = driver.find_element(By.ID, 'target-account-id')
        # Validation
        self.json_schema_editor = driver.find_element(By.CSS_SELECTOR, '.monaco-editor')
        self.validate_schema_btn = driver.find_element(By.ID, 'btn-verify-json')
        self.success_message = driver.find_element(By.CSS_SELECTOR, '.alert-success')
        self.schema_error_message = driver.find_element(By.CSS_SELECTOR, '[data-testid="error-feedback-text"]')

    def enter_rule_details(self, rule_id: str, rule_name: str):
        self.rule_id_input.clear()
        self.rule_id_input.send_keys(rule_id)
        self.rule_name_input.clear()
        self.rule_name_input.send_keys(rule_name)

    def select_trigger_type(self, trigger_type: str):
        self.trigger_type_dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//option[contains(text(), '{trigger_type}')]")
        option.click()

    def set_specific_date_trigger(self, date_str: str):
        self.date_picker.clear()
        self.date_picker.send_keys(date_str)

    def set_recurring_interval(self, interval_value: str):
        self.recurring_interval_input.clear()
        self.recurring_interval_input.send_keys(interval_value)

    def toggle_after_deposit(self, enable: bool):
        if self.after_deposit_toggle.is_selected() != enable:
            self.after_deposit_toggle.click()

    def add_balance_threshold_condition(self, operator: str, amount: float):
        self.add_condition_btn.click()
        self.condition_type_dropdown.click()
        option = self.driver.find_element(By.XPATH, "//option[contains(text(), 'balance_threshold')]")
        option.click()
        self.balance_threshold_input.clear()
        self.balance_threshold_input.send_keys(str(amount))
        self.operator_dropdown.click()
        operator_option = self.driver.find_element(By.XPATH, f"//option[contains(text(), '{operator}')]")
        operator_option.click()

    def add_transaction_source_condition(self, source_provider: str):
        self.add_condition_btn.click()
        self.condition_type_dropdown.click()
        option = self.driver.find_element(By.XPATH, "//option[contains(text(), 'transaction_source')]")
        option.click()
        self.transaction_source_dropdown.click()
        source_option = self.driver.find_element(By.XPATH, f"//option[contains(text(), '{source_provider}')]")
        source_option.click()

    def add_fixed_transfer_action(self, amount: float, destination_account: str):
        self.action_type_dropdown.click()
        option = self.driver.find_element(By.XPATH, "//option[contains(text(), 'fixed_amount')]")
        option.click()
        self.transfer_amount_input.clear()
        self.transfer_amount_input.send_keys(str(amount))
        self.destination_account_input.clear()
        self.destination_account_input.send_keys(destination_account)

    def add_percentage_transfer_action(self, percentage: float, destination_account: str):
        self.action_type_dropdown.click()
        option = self.driver.find_element(By.XPATH, "//option[contains(text(), 'percentage')]")
        option.click()
        self.percentage_input.clear()
        self.percentage_input.send_keys(str(percentage))
        self.destination_account_input.clear()
        self.destination_account_input.send_keys(destination_account)

    def enter_json_schema(self, schema: str):
        self.json_schema_editor.clear()
        self.json_schema_editor.send_keys(schema)

    def validate_json_schema(self):
        self.validate_schema_btn.click()
        try:
            self.wait.until(EC.visibility_of(self.success_message))
            return True
        except Exception:
            return False

    def get_schema_error_message(self):
        if self.schema_error_message.is_displayed():
            return self.schema_error_message.text
        return None

    def save_rule(self):
        self.save_rule_button.click()
        self.wait.until(EC.visibility_of(self.success_message))
        return self.success_message.text

    def simulate_deposit(self, source: str, amount: float):
        pass

    def get_rule_id(self):
        return self.rule_id_input.get_attribute('value')

    def is_success_message_displayed(self):
        return self.success_message.is_displayed()

    # New for TC_SCRUM158_009
    def prepare_sql_injection_payload(self, payload: str):
        self.transaction_source_dropdown.click()
        source_option = self.driver.find_element(By.XPATH, f"//option[contains(text(), '{payload}')]")
        source_option.click()

    def verify_input_sanitization(self):
        # Placeholder: actual implementation depends on system
        return not self.schema_error_message.is_displayed()

