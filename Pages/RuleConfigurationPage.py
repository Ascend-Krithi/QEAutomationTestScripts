import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
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
        self.schema_error_message = driver.find_element(By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    def navigate_to_rule_creation(self):
        # Assumes navigation is handled externally; placeholder for interface checks
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(self.save_rule_button)
        )

    def set_rule_id_and_name(self, rule_id, rule_name):
        self.rule_id_input.clear()
        self.rule_id_input.send_keys(rule_id)
        self.rule_name_input.clear()
        self.rule_name_input.send_keys(rule_name)

    def select_trigger_type(self, trigger_type):
        self.trigger_type_dropdown.click()
        self.trigger_type_dropdown.send_keys(trigger_type)

    def set_specific_date_trigger(self, date_str):
        self.select_trigger_type('specific_date')
        self.date_picker.clear()
        self.date_picker.send_keys(date_str)

    def set_recurring_interval_trigger(self, interval_value):
        self.select_trigger_type('recurring')
        self.recurring_interval_input.clear()
        self.recurring_interval_input.send_keys(interval_value)

    def enable_after_deposit_trigger(self):
        if not self.after_deposit_toggle.is_selected():
            self.after_deposit_toggle.click()

    def add_balance_threshold_condition(self, operator, amount):
        self.add_condition_btn.click()
        self.condition_type_dropdown.click()
        self.condition_type_dropdown.send_keys('balance_threshold')
        self.operator_dropdown.click()
        self.operator_dropdown.send_keys(operator)
        self.balance_threshold_input.clear()
        self.balance_threshold_input.send_keys(str(amount))

    def add_transaction_source_condition(self, source):
        self.add_condition_btn.click()
        self.condition_type_dropdown.click()
        self.condition_type_dropdown.send_keys('transaction_source')
        self.transaction_source_dropdown.click()
        self.transaction_source_dropdown.send_keys(source)

    def add_fixed_transfer_action(self, amount, currency, destination_account):
        self.action_type_dropdown.click()
        self.action_type_dropdown.send_keys('fixed_transfer')
        self.transfer_amount_input.clear()
        self.transfer_amount_input.send_keys(str(amount))
        self.destination_account_input.clear()
        self.destination_account_input.send_keys(destination_account)

    def add_percentage_transfer_action(self, percentage, destination_account):
        self.action_type_dropdown.click()
        self.action_type_dropdown.send_keys('percentage_transfer')
        self.percentage_input.clear()
        self.percentage_input.send_keys(str(percentage))
        self.destination_account_input.clear()
        self.destination_account_input.send_keys(destination_account)

    def validate_json_schema(self):
        self.validate_schema_btn.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(self.success_message)
        )
        return self.success_message.text

    def get_schema_error_message(self):
        return self.schema_error_message.text

    def save_rule(self):
        self.save_rule_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(self.success_message)
        )
        return self.success_message.text

    def get_rule_id(self):
        return self.rule_id_input.get_attribute('value')

    def retrieve_rule(self, rule_id):
        self.rule_id_input.clear()
        self.rule_id_input.send_keys(rule_id)
        self.save_rule_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(self.success_message)
        )
        return self.success_message.text
