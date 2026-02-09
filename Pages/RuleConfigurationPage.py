# RuleConfigurationPage.py
# Selenium Page Object for Rule Configuration
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Locators from Locators.json
    rule_id_input = (By.ID, 'rule-id-field')
    rule_name_input = (By.NAME, 'rule-name')
    save_rule_button = (By.CSS_SELECTOR, "button[data-testid='save-rule-btn']")
    trigger_type_dropdown = (By.ID, 'trigger-type-select')
    date_picker = (By.CSS_SELECTOR, "input[type='date']")
    recurring_interval_input = (By.ID, 'interval-value')
    after_deposit_toggle = (By.ID, 'trigger-after-deposit')
    add_condition_btn = (By.ID, 'add-condition-link')
    condition_type_dropdown = (By.CSS_SELECTOR, 'select.condition-type')
    balance_threshold_input = (By.CSS_SELECTOR, "input[name='balance-limit']")
    transaction_source_dropdown = (By.ID, 'source-provider-select')
    operator_dropdown = (By.CSS_SELECTOR, '.condition-operator-select')
    action_type_dropdown = (By.ID, 'action-type-select')
    transfer_amount_input = (By.NAME, 'fixed-amount')
    percentage_input = (By.ID, 'deposit-percentage')
    destination_account_input = (By.ID, 'target-account-id')
    json_schema_editor = (By.CSS_SELECTOR, '.monaco-editor')
    validate_schema_btn = (By.ID, 'btn-verify-json')
    success_message = (By.CSS_SELECTOR, '.alert-success')
    schema_error_message = (By.CSS_SELECTOR, "[data-testid='error-feedback-text']")

    # Test Step 2 (TC_SCRUM158_01): Prepare JSON rule schema (handled in test, not UI)

    # Test Step 3: Submit rule schema to API (handled in test, not UI)

    # Test Step 4: Retrieve from DB (handled in test, not UI)

    # UI interactions for rule creation
    def enter_rule_id(self, rule_id):
        self.driver.find_element(*self.rule_id_input).clear()
        self.driver.find_element(*self.rule_id_input).send_keys(rule_id)

    def enter_rule_name(self, rule_name):
        self.driver.find_element(*self.rule_name_input).clear()
        self.driver.find_element(*self.rule_name_input).send_keys(rule_name)

    def select_trigger_type(self, trigger_type):
        dropdown = self.driver.find_element(*self.trigger_type_dropdown)
        dropdown.click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//option[text()='{trigger_type}']"))).click()

    def set_recurring_interval(self, interval):
        self.driver.find_element(*self.recurring_interval_input).clear()
        self.driver.find_element(*self.recurring_interval_input).send_keys(str(interval))

    def toggle_after_deposit(self):
        self.driver.find_element(*self.after_deposit_toggle).click()

    def add_condition(self):
        self.driver.find_element(*self.add_condition_btn).click()

    def select_condition_type(self, condition_type):
        dropdown = self.driver.find_element(*self.condition_type_dropdown)
        dropdown.click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//option[text()='{condition_type}']"))).click()

    def enter_balance_threshold(self, threshold):
        self.driver.find_element(*self.balance_threshold_input).clear()
        self.driver.find_element(*self.balance_threshold_input).send_keys(str(threshold))

    def select_transaction_source(self, source):
        dropdown = self.driver.find_element(*self.transaction_source_dropdown)
        dropdown.click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//option[text()='{source}']"))).click()

    def select_operator(self, operator):
        dropdown = self.driver.find_element(*self.operator_dropdown)
        dropdown.click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//option[text()='{operator}']"))).click()

    def select_action_type(self, action_type):
        dropdown = self.driver.find_element(*self.action_type_dropdown)
        dropdown.click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//option[text()='{action_type}']"))).click()

    def enter_transfer_amount(self, amount):
        self.driver.find_element(*self.transfer_amount_input).clear()
        self.driver.find_element(*self.transfer_amount_input).send_keys(str(amount))

    def enter_percentage(self, percentage):
        self.driver.find_element(*self.percentage_input).clear()
        self.driver.find_element(*self.percentage_input).send_keys(str(percentage))

    def enter_destination_account(self, account_id):
        self.driver.find_element(*self.destination_account_input).clear()
        self.driver.find_element(*self.destination_account_input).send_keys(account_id)

    def validate_json_schema(self):
        self.driver.find_element(*self.validate_schema_btn).click()
        return self.wait.until(EC.visibility_of_element_located(self.success_message))

    def get_schema_error(self):
        return self.wait.until(EC.visibility_of_element_located(self.schema_error_message)).text
